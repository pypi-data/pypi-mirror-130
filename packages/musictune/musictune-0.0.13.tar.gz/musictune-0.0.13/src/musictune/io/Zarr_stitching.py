# Standard library imports
import math
import os

# Third party imports
import dask.array as da
import numpy as np
import zarr
from tqdm.auto import tqdm

# Local application imports
import musictune.io.modules as mod

def to_planes(delayed_session, tmp_plane_path, overlap, scale_factor, cutoff, laser_keys, z_resolution, merge_option,
              line_profile='default', nplanes=None):
    (c, z, x, y) = delayed_session.shape
    no_of_blocks = int(x / 2048)

    first, dip, rise, mid, last = mod.line_adjustment(delayed_session, laser_keys, overlap, cutoff, option=line_profile)
    al = np.concatenate([first, dip, rise] + [mid, dip, rise] * (no_of_blocks - 2) + [last], axis=1)
    al = da.from_array(np.expand_dims(al, axis=(1, -1)), chunks=(1, 1, 2048, 1))
    adjusted_session = delayed_session * al

    combined = mod.combine_blocks(adjusted_session, overlap, no_of_blocks)

    combined_downscaled = mod.x_downscale_4D(combined, scale_factor)

    combined_downscaled = mod.chromatic_correction(combined_downscaled, laser_keys, z_resolution, merge_option)

    (c, z, x, y) = combined_downscaled.shape
    tmp_chunks = (c, 1, 2048, 512)

    if not nplanes:
        nplanes = math.ceil(3e9 / (c * x * y))

    if not os.path.exists(tmp_plane_path):
        os.makedirs(tmp_plane_path)

    for zz in tqdm(range(0, z, nplanes), desc='Groups        ', ascii=True, dynamic_ncols=True, leave=True):
        tmp_save_path = os.path.join(tmp_plane_path, f"{zz:04d}.zarr")
        store = zarr.NestedDirectoryStore(tmp_save_path)

        plane = combined_downscaled[:, zz:zz + nplanes, :, :]
        z_out = zarr.create(shape=plane.shape, chunks=tmp_chunks, dtype='f4', store=store, overwrite=True)

        while True:
            try:
                plane.to_zarr(z_out, compressor='None')
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break

    return tmp_plane_path


def to_blocks(delayed_session, tmp_block_path, overlap, scale_factor, cutoff):
    (c, z, x, y) = delayed_session.shape
    no_of_blocks = int(x / 2048)

    first, dip, rise, mid, last = mod.adjustment_line(overlap, cutoff)
    first = np.expand_dims(first, axis=(0, 1, -1))
    last = np.expand_dims(last, axis=(0, 1, -1))
    mid = np.expand_dims(mid, axis=(0, 1, -1))
    dip = np.expand_dims(dip, axis=(0, 1, -1))
    rise = np.expand_dims(rise, axis=(0, 1, -1))

    block_id = 0

    current = delayed_session[:, :, :2048, :]
    following = delayed_session[:, :, 2048:2 * 2048, :]

    a = current[:, :, :-overlap, :] * first
    b = current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise
    mod.downscale_save_zarr(da.concatenate([a, b], axis=2),
                            os.path.join(tmp_block_path, f"{block_id:04d}.zarr"), scale_factor)
    block_id += 1

    for idx in tqdm(range(1, no_of_blocks - 1), desc='Blocks        ', ascii=True, dynamic_ncols=True, leave=True):
        current = following
        following = delayed_session[:, :, (idx + 1) * 2048:(idx + 2) * 2048, :]

        a = current[:, :, overlap:-overlap, :] * mid
        b = current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise
        mod.downscale_save_zarr(da.concatenate([a, b], axis=2),
                                os.path.join(tmp_block_path, f"{block_id:04d}.zarr"),
                                scale_factor)
        block_id += 1

    mod.downscale_save_zarr(following[:, :, overlap:, :] * last,
                            os.path.join(tmp_block_path, f"{block_id:04d}.zarr"), scale_factor)

    return tmp_block_path
