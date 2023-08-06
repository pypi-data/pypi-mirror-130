import argparse
import json
import math
import os
import shutil
from datetime import datetime
from shutil import copyfile

import dask
import dask.array as da
import h5py as h5
import musictune.io.utilities as util
import numpy as np
import pkg_resources
import zarr
from dask.distributed import progress
from distributed import Client
from musictune.UI.cli import print_logo
from musictune.io import PZF_Zstd
from tqdm import tqdm

home = os.path.expanduser("~")
scheduler_path = os.path.join(home, '.tune-scheduler.json')


@dask.delayed
def decompress(pzf_filepath):
    with open(pzf_filepath, 'rb') as f:
        datastring = f.read()

    data, header = PZF_Zstd.loads(datastring)

    return data


@dask.delayed
def merge(data, start_index, crop_length, weighted_pixels):
    data_cropped = data[:, start_index:start_index + crop_length, :]
    merged = np.sum(np.expand_dims(weighted_pixels.T, 2) * data_cropped, 1)

    return merged


@dask.delayed
def reposition(merged, sample_positions, grid):
    grid_img = np.zeros_like(merged)
    x_length = sample_positions.shape[0]
    sample_idx = 0

    if sample_positions[-1] < sample_positions[0]:
        sample_positions = np.flip(sample_positions)
        merged = np.flip(merged, 1)

    for i in range(x_length):

        if grid[i] < sample_positions[0]:
            grid_img[:, i] = merged[:, 0]
        elif grid[i] > sample_positions[-1]:
            grid_img[:, i] = merged[:, -1]
        else:
            while not (sample_positions[sample_idx] <= grid[i] <= sample_positions[sample_idx + 1]):
                sample_idx += 1

            right = sample_positions[sample_idx + 1] - grid[i]
            left = grid[i] - sample_positions[sample_idx]
            grid_img[:, i] = ((right * merged[:, sample_idx]) + (left * merged[:, sample_idx + 1])) / (right + left)

    return grid_img


def subsample_xy(z, g, level, dtype='uint16'):
    '''Subsample a zar pyramid level

    Parameters
    ----------
    z : zarr array
        The level to subsample
    g: zarr group
        The zarr file group to save the new level into
    level: str
        The name of the new level in the group
    '''
    d = da.from_zarr(z)
    if d.shape[2] % 2:
        # odd x
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        # odd y
        d = d[:, :, :, :-1]

    dn = (d[:, :, ::2, ::2] + d[:, :, 1::2, ::2] + d[:, :, ::2, 1::2] + d[:, :, 1::2, 1::2]) / 4

    zn = g.empty(str(level), shape=dn.shape, chunks=(1, 1, 256, 256), dtype=dtype)
    dn.to_zarr(zn)
    return zn, dn.shape


def main():
    print_logo()

    main_start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("scout_file", help="Configuration file (scout.json)")
    parser.add_argument("--project_path", help="Project directory to save the processed output ['/hpc/$USER/zarr]")
    parser.add_argument("--save_dir", help="Temporary directory to save intermediate files ['/hpc/$USER/tmp]")
    parser.add_argument("--levels", type=int, help="Number of pyramid levels [3]")
    parser.add_argument("--no_convert", help="Skip PZF to Zarr conversion step", action="store_true")
    parser.add_argument("--no_stitch", help="Skip PZF to Zarr conversion and stitching steps", action="store_true")
    args = parser.parse_args()

    # Input parameters
    config_path = args.scout_file

    if args.project_path:
        project_path = args.project_path
    else:
        project_path = os.path.join('/hpc', os.environ.get('USER'), 'zarr')

    if args.tmp_dir:
        tmp_dir = args.tmp_dir
    else:
        tmp_dir = os.path.join('/hpc', os.environ.get('USER'), 'tmp')

    if args.levels:
        pyramid_levels = args.levels
    else:
        pyramid_levels = 3

    # Default parameters
    cutoff = 92

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    project_name, sample_name, sequence_name, sessions, total_blocks = util.read_config(config_path)
    tmp_root = os.path.join(tmp_dir, f'{project_name}-{sample_name}-{sequence_name}')

    if not os.path.exists(tmp_root):
        os.makedirs(tmp_root)

    if len(sessions) > 1:

        while True:
            session_id = input("Multiple sessions found. Enter session number to process[0]:")
            try:
                session = sessions[int(session_id)]
                break
            except:
                print("Invalid session number")
                continue
    else:
        session = sessions[0]

    resource_filename = pkg_resources.resource_filename("musictune", 'img/Weights.json')
    f = open(resource_filename, "r")
    weights = json.loads(f.read())
    f.close()

    start_index = weights['ReadCrop']['index']
    crop_length = weights['ReadCrop']['length']
    weight = np.array(weights['Weight'])
    weighted_pixels = dask.delayed(np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels']))

    print("Registering client")
    client = Client(scheduler_file=scheduler_path)

    grid = dask.delayed(1e8 * np.arange(session['Image Start'], session['Image End'],
                                        session['Pixel Size'] * session['Scale Factor']))
    colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}

    print("Building computational graph")
    channel_props = []
    lasers = session['Files']
    delayed_lasers = []
    for las in lasers:
        directories = lasers[las]
        delayed_blocks = []
        h5_filepath = os.path.join(os.path.dirname(directories[0]), f'{sequence_name}_{las}.h5')
        coordinate_file = h5.File(copyfile(h5_filepath, os.path.join(tmp_root, f'{sequence_name}_{las}.h5')), 'r')
        for pzf_dir in directories:
            block = util.get_files(pzf_dir)

            if pzf_dir == directories[0]:
                data = decompress(block['pzf_files'][0])
                merged = merge(data, start_index, crop_length, weighted_pixels)
                sample = reposition(merged, coordinate_file.get(os.path.basename(block['pzf_files'][0]))[:],
                                    grid).compute()

            delayed_planes = [reposition(merge(decompress(fn), start_index, crop_length, weighted_pixels),
                                         coordinate_file.get(os.path.basename(fn))[:], grid) for fn in
                              block['pzf_files']]
            delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4') for x in delayed_planes]

            delayed_blocks.append(da.stack(delayed_planes))
        delayed_lasers.append(da.concatenate(delayed_blocks, axis=1))

        channel_props.append({"active": "true",
                              "coefficient": 1,
                              "color": colours[las],
                              "family": "linear",
                              "inverted": "false",
                              "label": 'Laser ' + las,
                              "window":
                                  {
                                      "end": 2000,
                                      "max": 65535,
                                      "min": 0,
                                      "start": 100
                                  }
                              })

    delayed_session = da.stack(delayed_lasers)

    line_file_path = pkg_resources.resource_filename("musictune", 'img/line_profile.csv')
    line_profile = np.genfromtxt(line_file_path, delimiter=',', dtype='f4')

    adjustment = np.minimum(1 / line_profile, 10)

    overlap = session['Overlap']
    img_resolution = session['Image Resolution']
    scale_factor = int(img_resolution[2] / img_resolution[1])

    (c, z, x, y) = delayed_session.shape
    no_of_blocks = int(x / 2048)

    first = adjustment[:-overlap]
    last = adjustment[overlap:]
    mid = adjustment[overlap:-overlap]

    dip = np.ones((overlap,), dtype='f4')
    dip[-cutoff:] = 0
    dip[cutoff:-cutoff] = np.linspace(1, 0, overlap - 2 * cutoff)
    dip *= adjustment[-overlap:]

    rise = np.ones((overlap,), dtype='f4')
    rise[:cutoff] = 0
    rise[cutoff:-cutoff] = np.linspace(0, 1, overlap - 2 * cutoff)
    rise *= adjustment[:overlap]

    first = np.expand_dims(first, axis=(0, 1, -1))
    last = np.expand_dims(last, axis=(0, 1, -1))
    mid = np.expand_dims(mid, axis=(0, 1, -1))
    dip = np.expand_dims(dip, axis=(0, 1, -1))
    rise = np.expand_dims(rise, axis=(0, 1, -1))

    blocks = []

    current = delayed_session[:, :, :2048, :]
    following = delayed_session[:, :, 2048:2 * 2048, :]

    blocks.append(current[:, :, :-overlap, :] * first)
    blocks.append(current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise)

    for idx in range(1, no_of_blocks - 1):
        current = following
        following = delayed_session[:, :, (idx + 1) * 2048:(idx + 2) * 2048, :]

        blocks.append(current[:, :, overlap:-overlap, :] * mid)
        blocks.append(current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise)

    blocks.append(following[:, :, overlap:, :] * last)

    combined = da.concatenate(blocks, axis=2)

    x_limit = math.floor(x / scale_factor) * scale_factor
    combined_reduced = combined[:, :, :x_limit:scale_factor, :]

    for i in range(1, scale_factor):
        combined_reduced += combined[:, :, i:x_limit:scale_factor, :]

    session_name = session['session_id']

    save_path = os.path.join(project_path, sample_name, sequence_name, f"{session_name}.zarr")
    store = zarr.NestedDirectoryStore(save_path)
    zarr_group = zarr.group(store=store, overwrite=True)

    level_0 = zarr_group.empty('0', shape=combined_reduced.shape, chunks=(1, 1, 256, 256), dtype='u2')
    combined_reduced.to_zarr(level_0)

    prev_level = level_0
    datasets = [{"path": "0"}]

    for i in tqdm(range(1, pyramid_levels), desc='Levels    ', ascii=True, dynamic_ncols=True, leave=False):
        prev_level, prev_shape = subsample_xy(prev_level, zarr_group, i)
        datasets.append({"path": f"{i}"})

    name = f"{project_name}-{sample_name}-{sequence_name}-{session_name}"
    zattrs = {
        "multiscales": [
            {
                "version": "0.3",
                "name": name,
                "datasets": datasets,
                "axes": [
                    "c", "z", "y", "x"
                ],
                "type": "uniform",
                "metadata": {
                    "method": "subsample_zarr"
                }
            }
        ],
        "omero":
            {
                "id": 1,
                "name": name,
                "channels": channel_props,
                "rdefs": {
                    "defaultT": 0,
                    "defaultZ": 0,
                    "model": "color"
                }
            }
    }

    with open(os.path.join(save_path, '.zattrs'), 'w') as outfile:
        json.dump(zattrs, outfile, indent=4)

    print("\nRemoving temporary files")
    shutil.rmtree(tmp_root, ignore_errors=True)
    client.close()

    print("\nElapsed total time:", datetime.now() - main_start_time)


if __name__ == "__main__":
    main()
