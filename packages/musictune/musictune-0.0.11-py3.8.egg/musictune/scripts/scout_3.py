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
from distributed import Client
from musictune.UI.cli import print_logo
from tqdm import tqdm

home = os.path.expanduser("~")
scheduler_path = os.path.join(home, '.tune-scheduler.json')


def main():
    print_logo()

    main_start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("scout_file", help="Configuration file (scout.json)")
    parser.add_argument("--project_path", default=os.path.join('/hpc', os.environ.get('USER'), 'zarr'),
                        help="Project directory to save the processed output")
    parser.add_argument("--tmp_dir", default=os.path.join('/hpc', os.environ.get('USER'), 'tmp'),
                        help="Temporary directory to save intermediate files ['/hpc/$USER/tmp]")
    parser.add_argument("--levels", type=int, default=3, help="Number of pyramid levels")
    parser.add_argument("--nplanes", type=int, default=3, help="Number of planes to be processed at one time")
    parser.add_argument("--xpixel", type=float, default=0.23325, help="resolution of the x pixel")
    parser.add_argument("--offset", type=int, default=300, help="Offset value for reverse imaging")
    parser.add_argument("--skew", type=int, default=12, help="Skew value for imaging")
    parser.add_argument("--cutoff", type=int, default=92, help="Cut off value when overlapping")
    args = parser.parse_args()

    # Input parameters
    config_path = args.scout_file
    project_path = args.project_path
    tmp_dir = args.tmp_dir
    pyramid_levels = args.levels
    nplanes = args.nplanes
    xpixel = args.xpixel
    offset = args.offset
    skew = args.skew
    cutoff = args.cutoff

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    project_name, sample_name, sequence_name, sessions, total_blocks = util.get_pzf_files(config_path)
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
        coordinate_file = h5.File(copyfile(h5_filepath, os.path.join(tmp_root, f'{sequence_name}_{las}.h5')), 'r')
        h5_dir = os.path.join(os.path.dirname(directories[0]), 'h5')

        if os.path.exists(h5_dir):
            copy_h5 = os.path.join(tmp_root, 'h5')

            if os.path.exists(copy_h5):
                shutil.rmtree(copy_h5)

            shutil.copytree(h5_dir, copy_h5)

        for pzf_dir in directories:
            block = util.get_files(pzf_dir)

            if pzf_dir == directories[0]:
                data = decompress(block['pzf_files'][0])
                sample = merge(data, start_index, crop_length, weighted_pixels).compute()

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
    (c, z, x, y) = delayed_session.shape
    no_of_blocks = int(x / 2048)

    line_file_path = pkg_resources.resource_filename("musictune", 'img/line_profile.csv')
    line_profile = np.genfromtxt(line_file_path, delimiter=',', dtype='f4')

    adjustment = np.minimum(1 / line_profile, 10)

    overlap = session['Overlap']
    img_resolution = session['Image Resolution']
    scale_factor = int(img_resolution[2] / img_resolution[1])

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

    y_limit = math.floor(x / scale_factor) * scale_factor
    combined_reduced = combined[:, :, :y_limit:scale_factor, :]

    for i in range(1, scale_factor):
        combined_reduced = combined_reduced + combined[:, :, i:y_limit:scale_factor, :]

    (c, z, x, y) = combined_reduced.shape
    tmp_chunks = (c, 1, 2048, 2048)
    session_name = session['session_id']

    for zz in tqdm(range(0, z, nplanes), desc='Planes    ', ascii=True, dynamic_ncols=True, leave=False):
        tmp_save_path = os.path.join(tmp_root, f"{session_name}", f"{zz}.zarr")
        store = zarr.NestedDirectoryStore(tmp_save_path)
        plane = combined_reduced[:, zz:zz + nplanes, :, :]
        z_out = zarr.create(shape=plane.shape, chunks=tmp_chunks, dtype='u2', store=store, overwrite=True)

        while True:
            try:
                plane.to_zarr(z_out)
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break

    print("\nElapsed time for saving planes:", datetime.now() - main_start_time)
    print("\n\nPreparing multi scale images")

    multiscale_time = datetime.now()

    blocks = []
    for zz in range(0, z, nplanes):
        tmp_save_path = os.path.join(tmp_root, f"{session_name}", f"{zz}.zarr")
        zarr_img = zarr.open(zarr.storage.NestedDirectoryStore(tmp_save_path), mode='r')
        blocks.append(da.from_zarr(zarr_img))

    img = da.concatenate(blocks, axis=1)

    save_path = os.path.join(project_path, sample_name, sequence_name, f"{session_name}.zarr")
    store = zarr.NestedDirectoryStore(save_path)
    zarr_group = zarr.group(store=store, overwrite=True)
    level_0 = zarr_group.empty('0', shape=combined_reduced.shape, chunks=tmp_chunks, dtype='u2')

    while True:
        try:
            img.to_zarr(level_0)
        except Exception as e:
            print(f"Error occurred: {e}, retrying")
            continue
        break

    prev_level = level_0
    datasets = [{"path": "0"}]

    for i in tqdm(range(1, pyramid_levels), desc='Levels    ', ascii=True, dynamic_ncols=True, leave=False):
        while True:
            try:
                prev_level, prev_save = subsample_xy(prev_level, zarr_group, i)
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break
        datasets.append({"path": f"{i}"})

    print("\nElapsed time for saving multiscale images:", datetime.now() - multiscale_time)

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

    print("\nElapsed total time:", datetime.now() - main_start_time)


if __name__ == "__main__":
    main()
