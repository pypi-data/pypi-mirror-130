# Standard library imports
from glob import glob
import random
import math
import os

# Third party imports
from distributed import progress
import h5py
import dask.array as da
import numpy as np
import pkg_resources
from tqdm.auto import tqdm
import zarr
# Local application imports
from musictune.UI import cli
import musictune.pzf2zarr.utilities as util

line_file_path = pkg_resources.resource_filename("musictune", 'data/line_profile.h5')
colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}
max_val = 65535


class Channel:

    def __init__(self, img, laser, resolution, overlap, nblocks):
        self.img = img
        self.laser = laser
        self.resolution = resolution
        self.overlap = overlap
        self.nblocks = nblocks

    @classmethod
    def from_stacks(cls, delayed_stacks, overlap):
        da_stack = [d.img for d in delayed_stacks]
        laser = delayed_stacks[0].laser
        resolution = delayed_stacks[0].resolution
        return cls(da.concatenate(da_stack, axis=1), laser, resolution, overlap, len(delayed_stacks))

    @classmethod
    def from_zarr(cls, zarr_files, overlap, laser, resolution):
        da_stacks = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(zz), mode='r')) for zz in zarr_files]
        return cls(da.concatenate(da_stacks, axis=1), laser, resolution, overlap, len(zarr_files))

    @classmethod
    def from_dir(cls, saved_dir, lasers, resolution, overlap, nblocks, is_blocks=True):
        zarr_files = sorted(glob(os.path.join(saved_dir, "*.zarr")))
        blocks = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(zz), mode='r')) for zz in zarr_files]
        return cls(da.concatenate(blocks, axis=1) if is_blocks else da.concatenate(blocks, axis=0), lasers, resolution,
                   overlap, nblocks)

    def line_correction(self, cutoff, option='default', clip=10):
        if os.path.exists(option):
            line_profile = read_line_profile(option, self.laser)
        elif option == 'measure':
            line_profile = measure_line_profile(self.img)
        else:
            line_profile = get_default_profile(self.laser)

        print('\nLine profiles\n')
        cli.plot_line_profiles(line_profile, [self.laser])
        print('\n')

        adjustment = np.minimum(1 / line_profile, clip)

        first = adjustment[:-self.overlap]
        last = adjustment[self.overlap:]
        mid = adjustment[self.overlap:-self.overlap]

        dip = np.ones((self.overlap,), dtype='f4')
        dip[-cutoff:] = 0
        dip[cutoff:-cutoff] = np.linspace(1, 0, self.overlap - 2 * cutoff)
        dip *= adjustment[-self.overlap:]

        rise = np.ones((self.overlap,), dtype='f4')
        rise[:cutoff] = 0
        rise[cutoff:-cutoff] = np.linspace(0, 1, self.overlap - 2 * cutoff)
        rise *= adjustment[:self.overlap]

        al = np.concatenate([first, dip, rise] + [mid, dip, rise] * (self.nblocks - 2) + [last], axis=0)
        al = da.from_array(np.expand_dims(al, axis=(0, -1)), chunks=(1, 2048, 1))
        self.img = self.img * al

    def combine_stacks(self):
        blocks = []
        current = self.img[:, :2048, :]
        following = self.img[:, 2048:2 * 2048, :]

        blocks.append(current[:, :-self.overlap, :])
        blocks.append(current[:, -self.overlap:, :] + following[:, :self.overlap, :])

        for idx in range(1, self.nblocks - 1):
            current = following
            following = self.img[:, (idx + 1) * 2048:(idx + 2) * 2048, :]
            blocks.append(current[:, self.overlap:-self.overlap, :])
            blocks.append(current[:, -self.overlap:, :] + following[:, :self.overlap, :])

        blocks.append(following[:, self.overlap:, :])
        self.img = da.concatenate(blocks, axis=1)

    def x_downscale(self, scale_factor):
        x_limit = math.floor(self.img.shape[1] / scale_factor) * scale_factor
        img_downscaled = self.img[:, :x_limit:scale_factor, :]

        for i in range(1, scale_factor):
            img_downscaled += self.img[:, i:x_limit:scale_factor, :]

        self.img = img_downscaled
        self.resolution = (self.resolution[0], self.resolution[1] * scale_factor, self.resolution[2])

    def check_saturation(self):
        print("\nComputing maximum intensity value.")
        dmv = self.img.max().persist()
        progress(dmv)
        mv = dmv.compute()
        del dmv
        print("")

        if mv > max_val:
            intensity_scale_factor = max_val / mv
            print("\x1b[1;31;40m" + f"Rescaling {self.laser} by {intensity_scale_factor}!" + "\x1b[0m")
            self.img = self.img * intensity_scale_factor

    def channel_prop(self):
        return {"active": "true",
                "coefficient": 1,
                "color": colours[self.laser],
                "family": "linear",
                "inverted": "false",
                "label": 'Laser ' + self.laser,
                "window":
                    {
                        "end": 2000,
                        "max": max_val,
                        "min": 0,
                        "start": 10
                    }
                }

    def to_zarr_planes(self, save_root, session_name, nplanes=None, tmp_chunks=(1, 2048, 512)):
        save_path = util.set_dir(save_root, session_name, self.laser + '_planes')

        (z, x, y) = self.img.shape

        if not nplanes:
            nplanes = math.ceil(3e9 / (x * y))

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for zz in tqdm(range(0, z, nplanes), desc='Groups        ', ascii=True, dynamic_ncols=True, leave=True):
            tmp_save_path = os.path.join(save_path, f"{zz:04d}.zarr")
            store = zarr.NestedDirectoryStore(tmp_save_path)

            plane = self.img[zz:zz + nplanes, :, :]
            z_out = zarr.create(shape=plane.shape, chunks=tmp_chunks, dtype='f4', store=store, overwrite=True)

            while True:
                try:
                    plane.to_zarr(z_out)
                except Exception as e:
                    print(f"Error occurred: {e}, retrying")
                    continue
                break
        return Channel.from_dir(save_path, self.laser, self.resolution, self.overlap, self.nblocks, is_blocks=False)


def read_line_profile(filepath, laser):
    line_profile = h5py.File(filepath, 'r')
    profile = line_profile.get(laser)

    if profile:
        profile /= np.max(np.array(profile))
    else:
        print(f'Line profile not found for laser {laser}, using the default profile.')
        profile = get_default_profile(laser)
    return profile


def measure_line_profile(img, sample_size=10):
    print('\nComputing line profile...')
    (z, x, y) = img.shape

    n_blocks = int(x / 2048)
    z_samples = random.sample(range(z), np.minimum(sample_size, z))
    x_samples = random.sample(range(n_blocks), np.minimum(sample_size, n_blocks))

    sampled_lines = []
    for zz in z_samples:
        for xx in x_samples:
            sampled_lines.append(da.mean(img[zz:zz + 1, xx * 2048:(xx + 1) * 2048, :], axis=(0, 2)))

    sampled_lines = da.stack(sampled_lines)
    line_medians = np.median(sampled_lines, axis=0).compute()

    return (line_medians + 1e-10) / np.max(line_medians)


def get_default_profile(laser):
    line_profile = h5py.File(line_file_path, 'r')
    profile = np.array(line_profile.get(laser))
    profile /= np.max(profile)
    return profile
