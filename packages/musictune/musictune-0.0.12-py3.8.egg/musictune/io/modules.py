# Standard library imports
import json
import math
import os
import random

# Third party imports
import dask
import dask.array as da
import h5py
import numpy as np
import skimage.transform as tf
import zarr
from tqdm.auto import tqdm

# Local application imports
import musictune.UI.cli as cli
import musictune.io.modules as mod
import musictune.io.params as paramio
import musictune.io.utilities as util
from . import PZF_Zstd, params


@dask.delayed
def decompress(pzf_filepath):
    with open(pzf_filepath, 'rb') as f:
        datastring = f.read()

    img, header = PZF_Zstd.loads(datastring)
    return img


@dask.delayed
def single_line(img, line_no=4):
    return img[:, :, line_no:line_no + 1, :]


@dask.delayed
def merge(img, line_weights):
    start_index = line_weights['Start']
    crop_length = line_weights['Length']
    weights = line_weights['Weights']
    img_cropped = img[:, start_index:start_index + crop_length, :]
    merged = np.sum(np.expand_dims(weights.T, 2) * img_cropped, 1)
    return merged


@dask.delayed
def reposition(img, sample_positions, grid, y_offset):
    grid_img = np.zeros_like(img)
    x_length = sample_positions.shape[0]
    sample_idx = 0

    if sample_positions[-1] < sample_positions[0]:
        grid += y_offset
        sample_positions = np.flip(sample_positions)
        img = np.flip(img, 1)

    for i in range(x_length):

        if grid[i] <= sample_positions[0]:
            grid_img[:, i] = img[:, 0]
        elif grid[i] >= sample_positions[-1]:
            grid_img[:, i] = img[:, -1]
        else:
            while not (sample_positions[sample_idx] <= grid[i] <= sample_positions[sample_idx + 1]):
                sample_idx += 1

            right = sample_positions[sample_idx + 1] - grid[i]
            left = grid[i] - sample_positions[sample_idx]
            grid_img[:, i] = ((right * img[:, sample_idx]) + (left * img[:, sample_idx + 1])) / (right + left)

    return grid_img


@dask.delayed
def deskew(img, affine_tf):
    return tf.warp(img, inverse_map=affine_tf, preserve_range=True)


def compute_delayed_plane(fn, skew, yscale_factor, line_weights, coordinate_file, grid, offset):
    if skew:
        affine_tf = tf.AffineTransform(shear=math.atan((skew / yscale_factor) / 1792))

        delayed_plane = mod.deskew(
            mod.reposition(
                mod.merge(mod.decompress(fn), line_weights),
                coordinate_file.get(os.path.basename(fn))[:], grid, offset),
            affine_tf)
    else:
        delayed_plane = mod.reposition(
            mod.merge(mod.decompress(fn), line_weights),
            coordinate_file.get(os.path.basename(fn))[:], grid, offset)
    return delayed_plane


def convert_pzf(fn, skew, yscale_factor, line_weights, coordinate_file, grid, offset, shape):
    delayed_plane = compute_delayed_plane(fn, skew, yscale_factor, line_weights, coordinate_file,
                                          grid, offset)

    return da.from_delayed(delayed_plane, shape=shape, dtype='f4')


def subsample_xy(z, g, level, chunks, dtype='uint16'):
    d = da.from_zarr(z).astype('uint32')
    if d.shape[2] % 2:
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        d = d[:, :, :, :-1]

    dn = (d[:, :, ::2, ::2] + d[:, :, 1::2, ::2] + d[:, :, ::2, 1::2] + d[:, :, 1::2, 1::2]) / 4

    zn = g.empty(str(level), shape=dn.shape, chunks=chunks, dtype=dtype)
    dn.to_zarr(zn, overwrite=True)

    return zn, dn.shape


def subsample_zarr(z, g, level, chunks, dtype='uint16'):
    d = da.from_zarr(z).astype('uint32')
    if d.shape[1] % 2:
        d = d[:, :-1, :, :]

    if d.shape[2] % 2:
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        d = d[:, :, :, :-1]

    dn = (d[:, ::2, ::2, ::2] + d[:, ::2, 1::2, ::2] + d[:, ::2, ::2, 1::2] + d[:, ::2, 1::2, 1::2]
          + d[:, 1::2, ::2, ::2] + d[:, 1::2, 1::2, ::2] + d[:, 1::2, ::2, 1::2] + d[:, 1::2, 1::2, 1::2]) / 8

    zn = g.empty(str(level), shape=dn.shape, chunks=chunks, dtype=dtype)
    dn.to_zarr(zn, overwrite=True)
    return zn, dn.shape


def read_line_profile(filepath, lasers):
    line_profile = h5py.File(filepath, 'r')
    line_profiles = []

    for l in lasers:
        profile = line_profile.get(l)

        if  profile:
            profile /= np.max(np.array(profile))
            line_profiles.append(profile)
        else:
            print(f'Line profile not found for laser {l}, using the default profile.')
            line_profiles.append(paramio.get_line_profile(l)[0])
    return np.stack(line_profiles)


def line_adjustment(delayed_session, laser_keys, overlap, cutoff, option='default', clip=10):
    if os.path.exists(option):
        line_profiles = read_line_profile(option, laser_keys)
    elif option == 'measure':
        line_profiles = measure_line_profile(delayed_session)
    else:
        line_profiles = paramio.get_line_profile(laser_keys)

    print('\nLine profiles\n')
    cli.plot_line_profiles(line_profiles, laser_keys)
    print('\n')

    adjustment = np.minimum(1 / line_profiles, clip)

    c = len(laser_keys)
    first = adjustment[:, :-overlap]
    last = adjustment[:, overlap:]
    mid = adjustment[:, overlap:-overlap]

    dip = np.ones((c, overlap), dtype='f4')
    dip[:, -cutoff:] = 0
    dip[:, cutoff:-cutoff] = np.linspace(1, 0, overlap - 2 * cutoff)
    dip *= adjustment[:, -overlap:]

    rise = np.ones((c, overlap), dtype='f4')
    rise[:, :cutoff] = 0
    rise[:, cutoff:-cutoff] = np.linspace(0, 1, overlap - 2 * cutoff)
    rise *= adjustment[:, :overlap]

    return first, dip, rise, mid, last


def combine_blocks(adjusted_session, overlap, no_of_blocks):
    blocks = []

    current = adjusted_session[:, :, :2048, :]
    following = adjusted_session[:, :, 2048:2 * 2048, :]

    blocks.append(current[:, :, :-overlap, :])
    blocks.append(current[:, :, -overlap:, :] + following[:, :, :overlap, :])

    for idx in range(1, no_of_blocks - 1):
        current = following
        following = adjusted_session[:, :, (idx + 1) * 2048:(idx + 2) * 2048, :]

        blocks.append(current[:, :, overlap:-overlap, :])
        blocks.append(current[:, :, -overlap:, :] + following[:, :, :overlap, :])

    blocks.append(following[:, :, overlap:, :])

    return da.concatenate(blocks, axis=2)


def x_downscale_4D(img, scale_factor):
    x_limit = math.floor(img.shape[2] / scale_factor) * scale_factor
    img_downscaled = img[:, :, :x_limit:scale_factor, :]

    for i in range(1, scale_factor):
        img_downscaled += img[:, :, i:x_limit:scale_factor, :]

    return img_downscaled


def downscale_save_zarr(block, tmp_save_path, scale_factor):
    block_reduced = x_downscale_4D(block, scale_factor)

    store = zarr.NestedDirectoryStore(tmp_save_path)
    z_out = zarr.create(shape=block_reduced.shape, dtype='f4', store=store, overwrite=True)

    while True:
        try:
            block_reduced.to_zarr(z_out, compressor='None', overwrite=True)
        except Exception as e:
            print(f"Error occurred: {e}, retrying")
            continue
        break


def downscale_save_delayed(block, tmp_save_path, scale_factor):
    block_reduced = x_downscale_4D(block, scale_factor)

    store = zarr.NestedDirectoryStore(tmp_save_path)
    z_out = zarr.create(shape=block_reduced.shape, dtype='f4', store=store, overwrite=True)

    return block_reduced.to_zarr(z_out, compressor='None', overwrite=True, compute=False)


def measure_line_profile(delayed_session, sample_size=10):
    print('\nComputing line profile...')
    (c, z, x, y) = delayed_session.shape

    n_blocks = int(x / 2048)
    z_samples = random.sample(range(z), np.minimum(sample_size, z))
    x_samples = random.sample(range(n_blocks), np.minimum(sample_size, n_blocks))

    sampled_lines = []
    for zz in z_samples:
        for xx in x_samples:
            sampled_lines.append(da.mean(delayed_session[:, zz:zz + 1, xx * 2048:(xx + 1) * 2048, :], axis=(1, 3)))

    sampled_lines = da.stack(sampled_lines)
    line_medians = np.median(sampled_lines, axis=0).compute()
    return ((line_medians + 1e-10) / (np.max(line_medians, axis=1)[:, np.newaxis]))


def multiscale_save(img, project_root, session_name, chunks, img_res, pyramid_levels, channel_props):
    (c, z, x, y) = img.shape

    if chunks[0] == -1:
        save_chunks = (c,) + util.opt_chunksize(z, (chunks[1], chunks[2]))
    else:
        save_chunks = (c,) + chunks

    save_path = os.path.join(project_root, f"{session_name}.zarr")
    store = zarr.NestedDirectoryStore(save_path)
    zarr_group = zarr.group(store=store, overwrite=True)
    level_0 = zarr_group.empty('0', shape=img.shape, chunks=save_chunks, dtype='u2')

    while True:
        try:
            img.to_zarr(level_0, overwrite=True)
        except Exception as e:
            print(f"Error occurred: {e}, retrying")
            continue
        break

    prev_level = level_0
    prev_shape = img.shape
    prev_res = img_res
    datasets = [{"path": "0"}]

    for i in tqdm(range(1, pyramid_levels), desc='Levels    ', ascii=True, dynamic_ncols=True, leave=True):
        (c, z, x, y) = prev_shape
        if chunks[0] == 1:
            save_chunks = (c,) + chunks
        else:
            save_chunks = (c,) + util.opt_chunksize(z, (chunks[1], chunks[2]))

        if prev_res[0] > 2 * prev_res[1] or prev_shape[1] == 1:
            while True:
                try:
                    prev_level, prev_shape = subsample_xy(prev_level, zarr_group, i, chunks=save_chunks)
                    prev_res = (prev_res[0], 2 * prev_res[1], 2 * prev_res[2])
                except Exception as e:
                    print(f"Error occurred: {e}, retrying")
                    continue
                break
        else:
            while True:
                try:
                    prev_level, prev_shape = subsample_zarr(prev_level, zarr_group, i, chunks=save_chunks)
                    prev_res = (2 * prev_res[0], 2 * prev_res[1], 2 * prev_res[2])
                except Exception as e:
                    print(f"Error occurred: {e}, retrying")
                    continue
                break
        datasets.append({"path": f"{i}"})

    name = f"{session_name}"
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


def chromatic_correction(delayed_session, laser_keys, z_resolution, merge_option='crop'):
    chromatic_offsets = params.get_chromatic_offset()
    min_offset = np.min([chromatic_offsets[l] for l in laser_keys])
    new_offsets = [chromatic_offsets[l] - min_offset for l in laser_keys]

    top_shifts = [round(n / z_resolution) for n in new_offsets]
    bottom_shifts = [t - np.max(top_shifts) if t - np.max(top_shifts) != 0 else None for t in top_shifts]

    channels_shifted = []
    for l_id, l in enumerate(laser_keys):
        if merge_option == 'crop':
            channels_shifted.append(delayed_session[l_id, top_shifts[l_id]:bottom_shifts[l_id], :, :])
        elif merge_option == 'pad':
            padded = []

            if bottom_shifts[l_id]:
                top_padding = da.from_array(
                    np.zeros((abs(bottom_shifts[l_id]), delayed_session.shape[2], delayed_session.shape[3]),
                             dtype='f4'))
                padded.append(top_padding)

            padded.append(delayed_session[l_id, :, :, :])

            if top_shifts[l_id]:
                bottom_padding = da.from_array(
                    np.zeros((abs(top_shifts[l_id]), delayed_session.shape[2], delayed_session.shape[3]), dtype='f4'))
                padded.append(bottom_padding)

            channels_shifted.append(da.concatenate(padded, axis=0))

    return da.stack(channels_shifted)
