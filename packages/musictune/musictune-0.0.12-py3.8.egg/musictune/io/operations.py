import json
import math
import os
import shutil
from shutil import copyfile

import dask
import dask.array as da
import h5py as h5
import musictune.io.modules as mod
import musictune.io.utilities as util
import numpy as np
import pkg_resources
import skimage.transform as tf
import zarr
from distributed import progress


def pzf2zarr(config_path, save_root, offset, skew, chunk_size, session_range, laser_range, strip_range,
             z_range, notebook=False):
    if notebook:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm

    project_name, sample_name, sequence_name, sessions = util.get_pzf_files(config_path, session_range, laser_range,
                                                                            strip_range, z_range)

    # line weights
    resource_filename = pkg_resources.resource_filename("musictune", 'data/Weights.json')
    f = open(resource_filename, "r")
    weights = json.loads(f.read())
    f.close()

    start_index = weights['ReadCrop']['index']
    crop_length = weights['ReadCrop']['length']
    weight = np.array(weights['Weight'])
    weighted_pixels = dask.delayed(np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels']))

    sessions_zarr = sessions.copy()
    results = []
    all_zarr_files = []
    print("Generating delayed objects")
    for s in tqdm(sessions, desc='Sessions      ', ascii=True, dynamic_ncols=True, leave=True):
        session = sessions[s]
        scale_factor = session['Scale Factor']
        affine_tf = tf.AffineTransform(shear=math.atan((skew / scale_factor) / 1792))
        grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                               session['Y Pixel Size'] * session['Scale Factor'])

        lasers = session['files']
        for las in tqdm(lasers, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=False):
            directories = lasers[las]
            sample_dir = list(directories)[0]

            h5_filepath = os.path.join(os.path.dirname(sample_dir), f'{sequence_name}_{las}.h5')
            coordinate_file = h5.File(copyfile(h5_filepath, os.path.join(save_root, f'{sequence_name}_{las}.h5')), 'r')
            h5_dir = os.path.join(os.path.dirname(sample_dir), 'h5')

            if os.path.exists(h5_dir):
                copy_h5 = os.path.join(save_root, 'h5')
                if os.path.exists(copy_h5):
                    shutil.rmtree(copy_h5)
                shutil.copytree(h5_dir, copy_h5)

            for pzf_dir in tqdm(directories, desc='Directories   ', ascii=True, dynamic_ncols=True, leave=False):
                pzf_files = directories[pzf_dir]

                if pzf_dir == sample_dir:
                    data = mod.decompress(pzf_files[0])
                    sample = mod.merge(data, start_index, crop_length, weighted_pixels).compute()

                sessions_zarr[s]['files'][las][pzf_dir] = []
                zarr_files = sessions_zarr[s]['files'][las][pzf_dir]
                for fn in pzf_files:

                    if skew:
                        delayed_plane = mod.deskew(
                            mod.reposition(mod.merge(mod.decompress(fn), start_index, crop_length, weighted_pixels),
                                           coordinate_file.get(os.path.basename(fn))[:], grid, offset), affine_tf)
                    else:
                        delayed_plane = mod.reposition(
                            mod.merge(mod.decompress(fn), start_index, crop_length, weighted_pixels),
                            coordinate_file.get(os.path.basename(fn))[:], grid)

                    da_plane = da.from_delayed(delayed_plane, shape=sample.shape, dtype='f4')

                    tmp_save_path = os.path.join(save_root, *fn.split(os.sep)[-3:]) + '.zarr'
                    store = zarr.NestedDirectoryStore(tmp_save_path)
                    z_out = zarr.create(shape=da_plane.shape, chunks=chunk_size, dtype=da_plane.dtype, store=store,
                                        overwrite=True)

                    results.append(da.to_zarr(da_plane, z_out, overwrite=True, compressor='None', compute=False))
                    zarr_files.append(tmp_save_path)
                    all_zarr_files.append(tmp_save_path)

    failed = []
    persisted_values = dask.persist(*results)
    print("\nConverting PZF files to zarr")
    progress(persisted_values, notebook=notebook)

    for pv in persisted_values:
        try:
            dask.compute(pv)
        except Exception as e:
            print(f"exception {e}")
            failed.append(pv)

    print(f"\nnumber of failed planes: {len(failed)}")

    try:
        del pv
    except:
        pass

    del persisted_values

    for dv in tqdm(failed, ascii=True, dynamic_ncols=True, leave=False):
        while True:
            try:
                dv.compute()
            except Exception as e:
                print(f"exception {e}, retrying")
                continue
            break

    try:
        del dv
    except:
        pass

    return sessions_zarr, all_zarr_files


def pzf2zarr_block(config_path, save_root, offset, skew, chunk_size, session_range, laser_range, strip_range,
                   z_range, notebook=False, delayed=False):
    if notebook:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm

    project_name, sample_name, sequence_name, sessions = util.get_pzf_files(config_path, session_range, laser_range,
                                                                            strip_range, z_range)

    # line weights
    resource_filename = pkg_resources.resource_filename("musictune", 'data/Weights.json')
    f = open(resource_filename, "r")
    weights = json.loads(f.read())
    f.close()

    start_index = weights['ReadCrop']['index']
    crop_length = weights['ReadCrop']['length']
    weight = np.array(weights['Weight'])
    weighted_pixels = dask.delayed(np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels']))

    sessions_zarr = sessions.copy()
    all_zarr_files = []
    results = []
    print("Generating delayed objects")
    for s in tqdm(sessions, desc='Sessions      ', ascii=True, dynamic_ncols=True, leave=True):
        session = sessions[s]
        scale_factor = session['Scale Factor']
        affine_tf = tf.AffineTransform(shear=math.atan((skew / scale_factor) / 1792))
        grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                               session['Y Pixel Size'] * session['Scale Factor'])

        lasers = session['files']
        for las in tqdm(lasers, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=False):
            directories = lasers[las]
            sample_dir = list(directories)[0]

            h5_filepath = os.path.join(os.path.dirname(sample_dir), f'{sequence_name}_{las}.h5')
            coordinate_file = h5.File(copyfile(h5_filepath, os.path.join(save_root, f'{sequence_name}_{las}.h5')), 'r')
            h5_dir = os.path.join(os.path.dirname(sample_dir), 'h5')

            if os.path.exists(h5_dir):
                copy_h5 = os.path.join(save_root, 'h5')
                if os.path.exists(copy_h5):
                    shutil.rmtree(copy_h5)
                shutil.copytree(h5_dir, copy_h5)

            sessions_zarr[s]['files'][las] = []
            zarr_files = sessions_zarr[s]['files'][las]
            for pzf_dir in tqdm(directories, desc='Directories   ', ascii=True, dynamic_ncols=True, leave=False):
                pzf_files = directories[pzf_dir]

                if pzf_dir == sample_dir:
                    data = mod.decompress(pzf_files[0])
                    sample = mod.merge(data, start_index, crop_length, weighted_pixels).compute()

                if skew:
                    delayed_planes = [mod.deskew(
                        mod.reposition(mod.merge(mod.decompress(fn), start_index, crop_length, weighted_pixels),
                                       coordinate_file.get(os.path.basename(fn))[:], grid, offset), affine_tf) for fn in
                        pzf_files]
                else:
                    delayed_planes = [
                        mod.reposition(mod.merge(mod.decompress(fn), start_index, crop_length, weighted_pixels),
                                       coordinate_file.get(os.path.basename(fn))[:], grid, offset) for fn in pzf_files]

                delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4') for x in delayed_planes]
                da_block = da.stack(delayed_planes)
                tmp_save_path = os.path.join(save_root, *pzf_dir.split(os.sep)[-2:]) + '.zarr'

                store = zarr.NestedDirectoryStore(tmp_save_path)
                z_out = zarr.create(shape=da_block.shape, chunks=(1,) + chunk_size, dtype=da_block.dtype, store=store,
                                    overwrite=True)
                if delayed:
                    results.append(da.to_zarr(da_block, z_out, overwrite=True, compressor='None', compute=False))
                else:
                    while True:
                        try:
                            da.to_zarr(da_block, z_out, overwrite=True, compressor='None')
                        except Exception as e:
                            print(f"Error occurred: {e}, retrying")
                            continue
                        break

                zarr_files.append(tmp_save_path)
                all_zarr_files.append(tmp_save_path)

    if delayed:
        failed = []
        persisted_values = dask.persist(*results)
        print("\nConverting PZF files to zarr")
        progress(persisted_values, notebook=notebook)

        for pv in persisted_values:
            try:
                dask.compute(pv)
            except Exception as e:
                print(f"exception {e}")
                failed.append(pv)

        print(f"\nnumber of failed planes: {len(failed)}")

        try:
            del pv
        except:
            pass

        del persisted_values

        for dv in tqdm(failed, ascii=True, dynamic_ncols=True, leave=False):
            while True:
                try:
                    dv.compute()
                except Exception as e:
                    print(f"exception {e}, retrying")
                    continue
                break

        try:
            del dv
        except:
            pass

    return sessions_zarr, all_zarr_files


def pzf2zarr_deconv(config_path, save_root, offset, skew, chunk_size, session_range, laser_range, strip_range, z_range,
                    notebook=False):
    if notebook:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm

    project_name, sample_name, sequence_name, sessions = util.get_pzf_files(config_path, session_range, laser_range,
                                                                            strip_range, z_range)

    # line weights
    resource_filename = pkg_resources.resource_filename("musictune", 'data/Weights.json')
    f = open(resource_filename, "r")
    weights = json.loads(f.read())
    f.close()

    start_index = weights['ReadCrop']['index']
    crop_length = weights['ReadCrop']['length']
    weight = np.array(weights['Weight'])
    weighted_pixels = dask.delayed(np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels']))

    sessions_zarr = sessions.copy()
    all_zarr_files = []
    print("Generating delayed objects")
    for s in tqdm(sessions, desc='Sessions      ', ascii=True, dynamic_ncols=True, leave=True):
        session = sessions[s]
        scale_factor = session['Scale Factor']
        affine_tf = tf.AffineTransform(shear=math.atan((skew / scale_factor) / 1792))
        grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                               session['Y Pixel Size'] * session['Scale Factor'])

        lasers = session['files']
        for las in tqdm(lasers, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=False):
            directories = lasers[las]
            sample_dir = list(directories)[0]

            h5_filepath = os.path.join(os.path.dirname(sample_dir), f'{sequence_name}_{las}.h5')
            coordinate_file = h5.File(copyfile(h5_filepath, os.path.join(save_root, f'{sequence_name}_{las}.h5')), 'r')
            h5_dir = os.path.join(os.path.dirname(sample_dir), 'h5')

            if os.path.exists(h5_dir):
                copy_h5 = os.path.join(save_root, 'h5')
                if os.path.exists(copy_h5):
                    shutil.rmtree(copy_h5)
                shutil.copytree(h5_dir, copy_h5)

            sessions_zarr[s]['files'][las] = []
            zarr_files = sessions_zarr[s]['files'][las]
            for pzf_dir in tqdm(directories, desc='Directories   ', ascii=True, dynamic_ncols=True, leave=False):
                pzf_files = directories[pzf_dir]

                if pzf_dir == sample_dir:
                    data = mod.decompress(pzf_files[0])
                    sample = mod.merge(data, start_index, crop_length, weighted_pixels).compute()

                if skew:
                    delayed_planes = [mod.deskew(
                        mod.reposition(mod.merge(mod.decompress(fn), start_index, crop_length, weighted_pixels),
                                       coordinate_file.get(os.path.basename(fn))[:], grid, offset), affine_tf) for fn in
                        pzf_files]
                else:
                    delayed_planes = [
                        mod.reposition(mod.merge(mod.decompress(fn), start_index, crop_length, weighted_pixels),
                                       coordinate_file.get(os.path.basename(fn))[:], grid, offset) for fn in pzf_files]

                delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4') for x in delayed_planes]
                da_block = da.stack(delayed_planes)
                tmp_save_path = os.path.join(save_root, *pzf_dir.split(os.sep)[-2:]) + '.zarr'

                store = zarr.NestedDirectoryStore(tmp_save_path)
                z_out = zarr.create(shape=da_block.shape, chunks=(1,) + chunk_size, dtype=da_block.dtype, store=store,
                                    overwrite=True)
                while True:
                    try:
                        da.to_zarr(da_block, z_out, overwrite=True, compressor='None')
                    except Exception as e:
                        print(f"Error occurred: {e}, retrying")
                        continue
                    break

                zarr_files.append(tmp_save_path)
                all_zarr_files.append(tmp_save_path)

    return sessions_zarr, all_zarr_files


def stitch_zarr_plane(sessions_zarr, project_root, tmp_root, xpixel, cutoff, chunk_size, pyramid_levels,
                      notebook=False):
    if notebook:
        from tqdm.auto import tqdm
    else:
        from tqdm import tqdm

    colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}

    for s in sessions_zarr:
        session = sessions_zarr[s]
        zarr_files = session['files']
        channel_props = []
        delayed_lasers = []

        for las, directories in zarr_files.items():
            delayed_blocks = []
            for pzf_dir in directories:
                delayed_planes = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(fn), mode='r')) for fn in
                                  directories[pzf_dir]]
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
        overlap = round(2048 - abs(1e6 * session['X Increment']) / xpixel)
        scale_factor = session['Scale Factor']

        first, dip, rise, mid, last = mod.adjustment_line(overlap, cutoff)
        al = np.concatenate([first, dip, rise] + [mid, dip, rise] * (no_of_blocks - 2) + [last])
        al = da.from_array(np.expand_dims(al, axis=(0, 1, -1)), chunks=(1, 1, 2048, 1))

        adjusted_session = delayed_session * al
        combined = mod.combine_blocks(adjusted_session, overlap, no_of_blocks)

        combined_downscaled = mod.x_downscle_4D(combined, scale_factor)

        (c, z, x, y) = combined_downscaled.shape
        tmp_chunks = (c, 1) + chunk_size
        session_name = session['session_id']
        nplanes = math.ceil(5e8 / (c * x * y))

        tmp_plane_path = os.path.join(tmp_root, 'planes')
        if not os.path.exists(tmp_plane_path):
            os.makedirs(tmp_plane_path)

        for zz in tqdm(range(0, z, nplanes), desc='Planes    ', ascii=True, dynamic_ncols=True, leave=True):
            tmp_save_path = os.path.join(tmp_plane_path, f"{session_name}", f"{zz}.zarr")
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

        print("\nGenerating multi scale images")

        blocks = []
        for zz in range(0, z, nplanes):
            tmp_save_path = os.path.join(tmp_plane_path, f"{session_name}", f"{zz}.zarr")
            zarr_img = zarr.open(zarr.storage.NestedDirectoryStore(tmp_save_path), mode='r')
            blocks.append(da.from_zarr(zarr_img))

        img = da.concatenate(blocks, axis=1)

        print("\nGenerating/overwriting zarr directories")

        save_path = os.path.join(project_root, f"{session_name}.zarr")
        store = zarr.NestedDirectoryStore(save_path)
        zarr_group = zarr.group(store=store, overwrite=True)
        level_0 = zarr_group.empty('0', shape=combined_downscaled.shape, chunks=tmp_chunks, dtype='u2')

        while True:
            try:
                img.to_zarr(level_0, overwrite=True)
            except Exception as e:
                print(f"Error occurred: {e}, retrying")
                continue
            break

        prev_level = level_0
        datasets = [{"path": "0"}]

        for i in tqdm(range(1, pyramid_levels), desc='Levels    ', ascii=True, dynamic_ncols=True, leave=False):
            while True:
                try:
                    prev_level, prev_save = mod.subsample_xy(prev_level, zarr_group, i)
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


def stitch_zarr(sessions_zarr, project_root, tmp_root, xpixel, cutoff, chunk_size, pyramid_levels, notebook=False,
                from_blocks=False, delayed_save=False):
    if notebook:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm

    colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}

    for s in sessions_zarr:
        session = sessions_zarr[s]
        zarr_files = session['files']
        channel_props = []
        delayed_lasers = []

        for las, directories in zarr_files.items():

            if from_blocks:
                delayed_blocks = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(fn), mode='r')) for fn in
                                  directories]
            else:
                delayed_blocks = []
                for pzf_dir in directories:
                    delayed_planes = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(fn), mode='r')) for fn in
                                      directories[pzf_dir]]
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
        overlap = round(2048 - abs(1e6 * session['X Increment']) / xpixel)
        scale_factor = session['Scale Factor']
        session_name = session['session_id']

        first, dip, rise, mid, last = mod.adjustment_line(overlap, cutoff)
        first = np.expand_dims(first, axis=(0, 1, -1))
        last = np.expand_dims(last, axis=(0, 1, -1))
        mid = np.expand_dims(mid, axis=(0, 1, -1))
        dip = np.expand_dims(dip, axis=(0, 1, -1))
        rise = np.expand_dims(rise, axis=(0, 1, -1))

        tmp_block_path = os.path.join(tmp_root, 'blocks')
        if not os.path.exists(tmp_block_path):
            os.makedirs(tmp_block_path)

        if delayed_save:
            block_id = 0
            block_results = []
            current = delayed_session[:, :, :2048, :]
            following = delayed_session[:, :, 2048:2 * 2048, :]

            block_results.append(mod.downscale_save_delayed(current[:, :, :-overlap, :] * first,
                                                            os.path.join(tmp_block_path, f"{session_name}",
                                                                         f"{block_id}.zarr"),
                                                            scale_factor))
            block_id += 1
            block_results.append(
                mod.downscale_save_delayed(current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise,
                                           os.path.join(tmp_block_path, f"{session_name}", f"{block_id}.zarr"),
                                           scale_factor))
            block_id += 1

            for idx in tqdm(range(1, no_of_blocks - 1), desc='Blocks  ', ascii=True, dynamic_ncols=True, leave=True):
                current = following
                following = delayed_session[:, :, (idx + 1) * 2048:(idx + 2) * 2048, :]

                block_results.append(mod.downscale_save_delayed(current[:, :, overlap:-overlap, :] * mid,
                                                                os.path.join(tmp_block_path, f"{session_name}",
                                                                             f"{block_id}.zarr"),
                                                                scale_factor))
                block_id += 1
                block_results.append(
                    mod.downscale_save_delayed(current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise,
                                               os.path.join(tmp_block_path, f"{session_name}", f"{block_id}.zarr"),
                                               scale_factor))
                block_id += 1

            block_results.append(mod.downscale_save_delayed(following[:, :, overlap:, :] * last,
                                                            os.path.join(tmp_block_path, f"{session_name}",
                                                                         f"{block_id}.zarr"), scale_factor))
            failed = []
            persisted_values = dask.persist(*block_results)
            print("\nConverting PZF blocks to zarr")
            progress(persisted_values, notebook=notebook)

            for pv in persisted_values:
                try:
                    dask.compute(pv)
                except Exception as e:
                    print(f"exception {e}")
                    failed.append(pv)

            print(f"\nnumber of failed planes: {len(failed)}")

            try:
                del pv
            except:
                pass

            del persisted_values

            for dv in tqdm(failed, ascii=True, dynamic_ncols=True, leave=False):
                while True:
                    try:
                        dv.compute()
                    except Exception as e:
                        print(f"exception {e}, retrying")
                        continue
                    break

            try:
                del dv
            except:
                pass
        else:
            block_id = 0

            current = delayed_session[:, :, :2048, :]
            following = delayed_session[:, :, 2048:2 * 2048, :]

            a = current[:, :, :-overlap, :] * first
            b = current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise
            mod.downscale_save_zarr(da.concatenate([a, b], axis=2),
                                    os.path.join(tmp_block_path, f"{session_name}", f"{block_id}.zarr"), scale_factor)
            block_id += 1

            for idx in tqdm(range(1, no_of_blocks - 1), desc='Blocks  ', ascii=True, dynamic_ncols=True, leave=True):
                current = following
                following = delayed_session[:, :, (idx + 1) * 2048:(idx + 2) * 2048, :]

                a = current[:, :, overlap:-overlap, :] * mid
                b = current[:, :, -overlap:, :] * dip + following[:, :, :overlap, :] * rise
                mod.downscale_save_zarr(da.concatenate([a, b], axis=2),
                                        os.path.join(tmp_block_path, f"{session_name}", f"{block_id}.zarr"),
                                        scale_factor)
                block_id += 1

            mod.downscale_save_zarr(following[:, :, overlap:, :] * last,
                                    os.path.join(tmp_block_path, f"{session_name}", f"{block_id}.zarr"), scale_factor)

        print("\n\nPreparing multi scale images")

        blocks = []
        for bb in range(block_id + 1):
            tmp_save_path = os.path.join(tmp_block_path, f"{session_name}", f"{bb}.zarr")
            zarr_img = zarr.open(zarr.storage.NestedDirectoryStore(tmp_save_path), mode='r')
            blocks.append(da.from_zarr(zarr_img))

        img = da.concatenate(blocks, axis=2)

        print("\nGenerating/overwriting zarr directories")
        (c, z, x, y) = img.shape
        save_chunks = (c, 1) + chunk_size
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
        datasets = [{"path": "0"}]

        for i in tqdm(range(1, pyramid_levels), desc='Levels    ', ascii=True, dynamic_ncols=True, leave=True):
            while True:
                try:
                    prev_level, prev_save = mod.subsample_xy(prev_level, zarr_group, i)
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
