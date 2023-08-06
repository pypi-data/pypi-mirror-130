# Third party imports
import dask
import numpy as np
import dask.array as da
import skimage.transform as tf

# Local application imports
from musictune.pzf2zarr import PZF_Zstd


class Strip:

    def __init__(self, path, weights, coordinates, grid, offset, skew, affine_tf):
        self.path = path
        self.weights = weights
        self.coordinates = coordinates
        self.grid = grid
        self.offset = offset
        self.skew = skew
        self.affine_tf = affine_tf

    def delayed(self, shape, dtype='f4'):
        return da.from_delayed(self.convert(), shape=shape, dtype=dtype)

    def compute(self):
        return self.convert().compute()

    def to_zarr(self):
        pass

    def convert(self):
        if self.skew:
            delayed_plane = deskew(reposition(merge(decompress(
                self.path), self.weights), self.coordinates, self.grid, self.offset), self.affine_tf)
        else:
            delayed_plane = reposition(merge(decompress(
                self.path), self.weights), self.coordinates, self.grid, self.offset)

        return delayed_plane


@dask.delayed
def decompress(path):
    with open(path, 'rb') as f:
        data_string = f.read()
    img, header = PZF_Zstd.loads(data_string)
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
def reposition(img, coordinates, grid, y_offset):
    grid_img = np.zeros_like(img)
    x_length = coordinates.shape[0]
    sample_idx = 0

    if coordinates[-1] < coordinates[0]:
        grid += y_offset
        coordinates = np.flip(coordinates)
        img = np.flip(img, 1)

    for i in range(x_length):
        if grid[i] <= coordinates[0]:
            grid_img[:, i] = img[:, 0]
        elif grid[i] >= coordinates[-1]:
            grid_img[:, i] = img[:, -1]
        else:
            while not (coordinates[sample_idx] <= grid[i] <= coordinates[sample_idx + 1]):
                sample_idx += 1

            right = coordinates[sample_idx + 1] - grid[i]
            left = grid[i] - coordinates[sample_idx]
            grid_img[:, i] = ((right * img[:, sample_idx]) + (left * img[:, sample_idx + 1])) / (right + left)
    return grid_img


@dask.delayed
def deskew(img, affine_tf):
    return tf.warp(img, inverse_map=affine_tf, preserve_range=True)
