# Standard library imports
import math
import os
import shutil
import json
from shutil import copyfile

# Third party imports
import dask.array as da
import h5py as h5
import pkg_resources
import zarr


def opt_chunksize(depth, xy_chunks=(256, 256), lower=100, upper=200):
    if depth < lower:
        chunk_d = depth
    else:
        divisor = 1
        chunk_d = depth
        while not (lower <= chunk_d < upper):
            divisor += 1
            chunk_d = math.ceil(depth / divisor)

    return (chunk_d,) + xy_chunks


def str_format(string):
    if string == '':
        return slice(None)
    elif '-' in string:
        return slice(*map(int, string.split('-')))
    elif ',' in string:
        return string.split(',')
    else:
        num = int(string)
        return slice(num, num + 1, 1)


def get_save_path(project_name="CV"):
    path = pkg_resources.resource_filename("musictune", 'img/save_path.json')
    f = open(path, "r")
    paths = json.loads(f.read())
    f.close()

    return paths[project_name]


def to_zarr(dask_img, prefix, chunk_size=None, save_path=None, dtype=None):
    if chunk_size is None:
        chunk_size = dask_img.chunksize
    if dtype is None:
        dtype = dask_img.dtype

    shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), dask_img.shape, chunk_size))

    store_save = zarr.NestedDirectoryStore(save_path)
    zarr_out = zarr.create(shape, chunks=chunk_size, store=store_save, dtype=dtype, fill_value=0,
                           overwrite=True)

    da.to_zarr(dask_img, zarr_out)
    return save_path


def from_zarr(file_path, chunk_size=None):
    zarr_img = zarr.open(zarr.storage.NestedDirectoryStore(file_path), mode='r')

    if chunk_size is None:
        chunk_size = zarr_img.chunks

    return da.from_zarr(zarr_img, chunks=chunk_size)


def copy_h5_files(sample_dir, save_root, sequence_name, las):
    h5_filepath = os.path.join(os.path.dirname(sample_dir), f'{sequence_name}_{las}.h5')
    coordinate_file = h5.File(copyfile(h5_filepath, os.path.join(save_root, f'{sequence_name}_{las}.h5')), 'r')
    h5_dir = os.path.join(os.path.dirname(sample_dir), 'h5')

    if os.path.exists(h5_dir):
        copy_h5 = os.path.join(save_root, 'h5')
        if os.path.exists(copy_h5):
            shutil.rmtree(copy_h5)
        shutil.copytree(h5_dir, copy_h5)

    return coordinate_file


def set_dir(root, *paths):
    this_dir = root
    for p in paths:
        this_dir = os.path.join(this_dir, p)
    if not os.path.exists(this_dir):
        os.makedirs(this_dir)
    return this_dir
