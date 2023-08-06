import argparse
import json
import math
import os
import shutil
from datetime import datetime

import dask
import dask.array as da
import h5py as h5
import musictune.io.PZF_Zstd as PZF_Zstd
import musictune.io.utilities as util
import numpy as np
import pkg_resources
import zarr
from distributed import Client
from musictune.UI.cli import print_logo
from tqdm.auto import tqdm

home = os.path.expanduser("~")
scheduler_path = os.path.join(home, '.tune-scheduler.json')


@dask.delayed
def decompress(pzf_filepath):
    with open(pzf_filepath, 'rb') as f:
        datastring = f.read()

    data, header = PZF_Zstd.loads(datastring)

    return data


@dask.delayed
def merge(data, weights):
    index=weights['ReadCrop']['index']
    length=weights['ReadCrop']['length']
    merged = np.sum(np.expand_dims(weights['Pixels'].T, 2) * data[:, index:index+length, :], 1)

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


def subsample_xy(z, g, level, chunks=(1, 1, 1024, 1024), dtype='uint16'):
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

    zn = g.empty(str(level), shape=dn.shape, chunks=chunks, dtype=dtype, overwrite=True)
    dn.to_zarr(zn)
    return zn, dn.shape


def main():
    print_logo()

    main_start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("scout_file", help="Configuration file (scout.json)")
    parser.add_argument("--project_path", "-p", default=os.path.join('/hpc', os.environ.get('USER'), 'zarr'),
                        help="Project directory to save the processed output ['/hpc/$USER/zarr]")
    parser.add_argument("--tmp_dir", "-t", default=os.path.join('/hpc', os.environ.get('USER'), 'tmp'),
                        help="Temporary directory to save intermediate files ['/hpc/$USER/tmp]")
    parser.add_argument("--levels", "-l", type=int, default=3, help="Number of pyramid levels [3]")
    parser.add_argument("--cutoff", "-c", type=int, default=92, help="Cutoff pixels for overlap [92]")
    parser.add_argument("--nplanes", "-n", type=int, default=3, help="Number of planes to be processed at one time [3]")
    parser.add_argument("--no_convert", help="Skip PZF to Zarr conversion step", action="store_true")
    parser.add_argument("--no_stitch", help="Skip PZF to Zarr conversion and stitching steps", action="store_true")
    args = parser.parse_args()

    # Input parameters
    config_path = args.scout_file
    project_path = args.project_path
    tmp_dir = args.tmp_dir
    pyramid_levels = args.levels
    nplanes = args.nplanes
    cutoff = args.cutoff

    project_name, sample_name, sequence_name, sessions, total_blocks = util.read_config(config_path)

    tmp_root = os.path.join(tmp_dir, f'{project_name}-{sample_name}-{sequence_name}')
    if not os.path.exists(tmp_root):
        os.makedirs(tmp_root)

    session = sessions[0]
    if len(sessions) > 1:
        while True:
            session_id = input("Multiple sessions found. Enter session number to process [0]: ")
            try:
                session = sessions[int(session_id)]
                break
            except:
                print("Invalid session number")
                continue

    resource_filename = pkg_resources.resource_filename("musictune", 'data/Weights.json')
    with open(resource_filename, "r") as f:
        weights = json.load(f)
    weights['Pixels'] = dask.delayed(
        np.expand_dims(np.array(weights['Weight']), 1) * np.array(weights['Weighted Pixels']))

    print("Registering client")
    client = Client(scheduler_file=scheduler_path)

    print("Building computational graph")

    grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                           session['Pixel Size'] * session['Scale Factor'])
    colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}

    channel_props = []
    lasers = session['Files']
    delayed_lasers = []
    for las in lasers:
        directories = lasers[las]
        delayed_blocks = []

        h5_filepath = os.path.join(os.path.dirname(directories[0]), f'{sequence_name}_{las}.h5')
        coordinate_file = h5.File(shutil.copyfile(h5_filepath, os.path.join(tmp_root, f'{sequence_name}_{las}.h5')),'r')

        h5_dir = os.path.join(os.path.dirname(directories[0]), 'h5')
        if os.path.exists(h5_dir):
            copy_h5 = os.path.join(tmp_root, 'h5')
            if os.path.exists(copy_h5):
                shutil.rmtree(copy_h5)
            shutil.copytree(h5_dir, copy_h5)

        for i, pzf_dir in enumerate(directories):
            block = util.get_files(pzf_dir)
            if i == 0:
                sample = merge(decompress(block['pzf_files'][0]), weights).compute()

            delayed_planes = [reposition(merge(decompress(fn), weights),
                                         coordinate_file.get(os.path.basename(fn))[:], grid)
                              for fn in block['pzf_files']]
            delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4')
                              for x in delayed_planes]

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
    (c, z, x, y) = delayed_session.shape
    no_of_blocks = int(x / 2048)

    line_file_path = pkg_resources.resource_filename("musictune", 'data/line_profile.csv')
    line_profile = np.genfromtxt(line_file_path, delimiter=',', dtype='f4')

    adjustment = np.minimum(1 / line_profile, 10)

    overlap = session['Overlap']
    img_resolution = session['Image Resolution']
    scale_factor = int(img_resolution[2] / img_resolution[1])

    first = np.expand_dims(adjustment[:-overlap], axis=(0, 1, -1))
    last = np.expand_dims(adjustment[overlap:], axis=(0, 1, -1))
    mid = np.expand_dims(adjustment[overlap:-overlap], axis=(0, 1, -1))
    dip = np.expand_dims(
        np.concatenate(
            [np.ones(cutoff),
             np.linspace(1, 0, overlap - 2 * cutoff, dtype='f4'),
             np.zeros(cutoff)]
        ), (0, 1, -1)
    )
    rise = 1 - dip
    dip *= adjustment[-overlap:]
    rise *= adjustment[:overlap]

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

    y_limit = math.floor(x / scale_factor) * scale_factor
    combined_reduced = combined[:, :, :y_limit:scale_factor, :]

    for i in range(1, scale_factor):
        combined_reduced = combined_reduced + combined[:, :, i:y_limit:scale_factor, :]

    (c, z, x, y) = combined_reduced.shape
    chunks = (c, 1, 2048, 2048)
    session_name = session['session_id']

    for zz in tqdm(range(0, z, nplanes), desc='Planes    ', dynamic_ncols=True):
        tmp_save_path = os.path.join(tmp_root, f"{session_name}", f"{zz}.zarr")
        store = zarr.NestedDirectoryStore(tmp_save_path)
        plane = combined_reduced[:, zz:zz + nplanes, :, :]
        z_out = zarr.create(shape=plane.shape, chunks=chunks, dtype='u2', store=store, overwrite=True)

        while True:
            try:
                plane.to_zarr(z_out)
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break

    print("\nElapsed time for saving planes: ", datetime.now() - main_start_time)
    print("\n\nPreparing multi scale images")

    multiscale_time = datetime.now()
    chunks = (1, 1, 1024, 1024)

    blocks = []
    for zz in range(0, z, nplanes):
        tmp_save_path = os.path.join(tmp_root, f"{session_name}", f"{zz}.zarr")
        zarr_img = zarr.open(zarr.storage.NestedDirectoryStore(tmp_save_path), mode='r')
        blocks.append(da.from_zarr(zarr_img))

    img = da.concatenate(blocks, axis=1)

    save_path = os.path.join(project_path, sample_name, sequence_name, f"{session_name}.zarr")
    store = zarr.NestedDirectoryStore(save_path)
    zarr_group = zarr.group(store=store, overwrite=True)
    level_0 = zarr_group.empty('0', shape=combined_reduced.shape, chunks=chunks, dtype='u2')

    while True:
        try:
            img.to_zarr(level_0)
        except Exception as e:
            print(f"Error occurred: {e}, retrying")
            continue
        break

    prev_level = level_0
    datasets = [{"path": "0"}]

    for i in tqdm(range(1, pyramid_levels), desc='Levels    ', dynamic_ncols=True):
        while True:
            try:
                prev_level, prev_save = subsample_xy(prev_level, zarr_group, i, chunks=chunks)
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break
        datasets.append({"path": f"{i}"})

    print("\nElapsed time for saving multiscale images: ", datetime.now() - multiscale_time)

    name = f"{project_name}-{sample_name}-{sequence_name}-{session_name}"
    zattrs = {
        "_ARRAY_DIMENSIONS": [
            "c", "z", "y", "x"
        ],
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

    print("\nElapsed total time: ", datetime.now() - main_start_time)


if __name__ == "__main__":
    main()
