# Standard library imports
import os

# Third party imports
import dask.array as da
from glob import glob
import zarr


def from_files(zarr_files, is_blocks=True):
    delayed_lasers = []
    for las, stacks in zarr_files.items():
        if is_blocks:
            delayed_blocks = [
                da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(fn), mode='r'))
                for fn in stacks]
        else:
            delayed_blocks = []
            for pzf_dir in stacks:
                delayed_planes = [
                    da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(fn), mode='r'))
                    for fn in stacks[pzf_dir]]
                delayed_blocks.append(da.stack(delayed_planes))
        delayed_lasers.append(da.concatenate(delayed_blocks, axis=1))

    return da.stack(delayed_lasers)


def from_dir(saved_dir, is_blocks=True):
    zarr_files = sorted(glob(os.path.join(saved_dir, "*.zarr")))
    blocks = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(zz), mode='r')) for zz in zarr_files]

    return da.concatenate(blocks, axis=2) if is_blocks else da.concatenate(blocks, axis=1)
