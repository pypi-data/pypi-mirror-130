# Standard library imports
import json
import math
import os

# Third party imports
from glob import glob
import dask.array as da
import numpy as np
import zarr
from tqdm.auto import tqdm

# Local application imports
import musictune.pzf2zarr.utilities as util

chromatic_offsets = {'405': 0, '488': 44, '561': 68, '640': 80}


class Session:
    def __init__(self, img, lasers, resolution):
        self.img = img
        self.lasers = lasers
        self.resolution = resolution

    @classmethod
    def from_channels(cls, delayed_channels):
        da_channels = [d.img for d in delayed_channels]
        lasers = [d.laser for d in delayed_channels]
        resolution = delayed_channels[0].resolution
        return cls(da.stack(da_channels), lasers, resolution)

    @classmethod
    def from_dir(cls, saved_dir, lasers, resolution, is_blocks=True):
        zarr_files = sorted(glob(os.path.join(saved_dir, "*.zarr")))
        blocks = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(zz), mode='r')) for zz in zarr_files]
        return cls(da.concatenate(blocks, axis=2) if is_blocks else da.concatenate(blocks, axis=1), lasers, resolution)

    def chromatic_correction(self, z_resolution, merge_option='crop'):
        min_offset = np.min([chromatic_offsets[l] for l in self.lasers])
        new_offsets = [chromatic_offsets[l] - min_offset for l in self.lasers]

        top_shifts = [round(n / z_resolution) for n in new_offsets]
        bottom_shifts = [t - np.max(top_shifts) if t - np.max(top_shifts) != 0 else None for t in top_shifts]

        channels_shifted = []
        for l_id, l in enumerate(self.lasers):
            if merge_option == 'crop':
                channels_shifted.append(self.img[l_id, top_shifts[l_id]:bottom_shifts[l_id], :, :])
            elif merge_option == 'pad':
                padded = []

                if bottom_shifts[l_id]:
                    top_padding = da.from_array(
                        np.zeros((abs(bottom_shifts[l_id]), self.img.shape[2], self.img.shape[3]), dtype='f4'))
                    padded.append(top_padding)
                padded.append(self.img[l_id, :, :, :])

                if top_shifts[l_id]:
                    bottom_padding = da.from_array(
                        np.zeros((abs(top_shifts[l_id]), self.img.shape[2], self.img.shape[3]), dtype='f4'))
                    padded.append(bottom_padding)
                channels_shifted.append(da.concatenate(padded, axis=0))
        self.img = da.stack(channels_shifted)

    def multiscale_save(self, project_root, session_name, chunks, pyramid_levels, channel_props):
        (c, z, x, y) = self.img.shape

        if chunks[0] == -1:
            save_chunks = (c,) + util.opt_chunksize(z, (chunks[1], chunks[2]))
        else:
            save_chunks = (c,) + chunks

        save_path = os.path.join(project_root, f"{session_name}.zarr")
        store = zarr.NestedDirectoryStore(save_path)
        zarr_group = zarr.group(store=store, overwrite=True)
        level_0 = zarr_group.empty('0', shape=self.img.shape, chunks=save_chunks, dtype='u2')

        while True:
            try:
                self.img.to_zarr(level_0, overwrite=True)
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break

        prev_level = level_0
        prev_shape = self.img.shape
        prev_res = self.resolution
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

        return save_path

    def to_zarr_planes(self, save_root, session_name, nplanes=None):
        save_path = util.set_dir(save_root, session_name, 'planes')

        (c, z, x, y) = self.img.shape
        tmp_chunks = (c, 1, 2048, 512)

        if not nplanes:
            nplanes = math.ceil(3e9 / (c * x * y))

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for zz in tqdm(range(0, z, nplanes), desc='Groups        ', ascii=True, dynamic_ncols=True, leave=True):
            tmp_save_path = os.path.join(save_path, f"{zz:04d}.zarr")
            store = zarr.NestedDirectoryStore(tmp_save_path)

            plane = self.img[:, zz:zz + nplanes, :, :]
            z_out = zarr.create(shape=plane.shape, chunks=tmp_chunks, dtype='f4', store=store, overwrite=True)

            while True:
                try:
                    plane.to_zarr(z_out, compressor='None')
                except Exception as e:
                    print(f"Error occurred: {e}, retrying")
                    continue
                break
        return Session.from_dir(save_path, self.lasers, self.resolution, is_blocks=False)


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
