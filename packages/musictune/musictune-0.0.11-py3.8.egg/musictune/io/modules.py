import dask
import dask.array as da
import numpy as np
import skimage.transform as tf

from . import PZF_Zstd


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
def merge(img, start_index, crop_length, weighted_pixels):
    img_cropped = img[:, start_index:start_index + crop_length, :]
    merged = np.sum(np.expand_dims(weighted_pixels.T, 2) * img_cropped, 1)
    return merged


@dask.delayed
def reposition(img, sample_positions, grid, y_offset=300):
    grid_img = np.zeros_like(img)
    x_length = sample_positions.shape[0]
    sample_idx = 0

    print(sample_positions[0], sample_positions[-1])

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


def subsample_xy(z, g, level, dtype='uint16'):
    d = da.from_zarr(z)
    if d.shape[2] % 2:
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        d = d[:, :, :, :-1]

    dn = (d[:, :, ::2, ::2] + d[:, :, 1::2, ::2] + d[:, :, ::2, 1::2] + d[:, :, 1::2, 1::2]) / 4

    zn = g.empty(str(level), shape=dn.shape, chunks=(1, 1, 256, 256), dtype=dtype)
    dn.to_zarr(zn)
    return zn, dn.shape


def subsample_zarr(z, g, level, dtype='uint16'):
    d = da.from_zarr(z)
    if d.shape[1] % 2:
        d = d[:, :-1, :, :]

    if d.shape[2] % 2:
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        d = d[:, :, :, :-1]

    dn = (d[:, ::2, ::2, ::2] + d[:, ::2, 1::2, ::2] + d[:, ::2, ::2, 1::2] + d[:, ::2, 1::2, 1::2]
          + d[:, 1::2, ::2, ::2] + d[:, 1::2, 1::2, ::2] + d[:, 1::2, ::2, 1::2] + d[:, 1::2, 1::2, 1::2]) / 8

    zn = g.empty(str(level), shape=dn.shape, chunks=(1, 1, 256, 256), dtype=dtype)
    dn.to_zarr(zn)
    return zn, dn.shape
