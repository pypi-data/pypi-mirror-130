# Standard library imports
import math
import os
import shutil
# Third party imports
from glob import glob

import dask
import dask.array as da
import musictune.io.delayed_from_zarr as dfz
# Local application imports
import musictune.io.modules as mod
import musictune.io.utilities as util
import numpy as np
import zarr
from distributed import progress
from musictune.deconvolution.deconvolve import deconvolve_parallel
from tqdm.auto import tqdm


def strips(session, filelist, sequence_name, save_root, offset, skew, line_weights):
    yscale_factor = session['Scale Factor']
    grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                           session['Y Pixel Size'] * yscale_factor)

    files = {}
    results = []
    all_zarr_files = []
    for las in tqdm(filelist, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=True):
        stacks = filelist[las]
        sample_dir = list(stacks)[0]
        coordinate_file = util.copy_h5_files(sample_dir, save_root, sequence_name, las)
        sample = mod.merge(mod.decompress(stacks[0][0]), line_weights).compute()

        files[las] = {}
        for stack in tqdm(stacks, desc='Stacks        ', ascii=True, dynamic_ncols=True, leave=False):

            files[las][stack] = []
            for fn in stacks[stack]:
                da_plane = mod.convert_pzf(fn, skew, yscale_factor, line_weights, coordinate_file,
                                           grid, offset, sample.shape)

                tmp_save_path = os.path.join(save_root, *fn.split(os.sep)[-3:]) + '.zarr'
                store = zarr.NestedDirectoryStore(tmp_save_path)
                z_out = zarr.create(shape=da_plane.shape, chunks=(1, 2048, 2048), dtype=da_plane.dtype,
                                    store=store, overwrite=True)
                results.append(da.to_zarr(da_plane, z_out, overwrite=True, compressor='None', compute=False))
                files[las][stack].append(tmp_save_path)
                all_zarr_files.append(tmp_save_path)

    failed = []
    persisted_values = dask.persist(*results)
    print("\nConverting PZF files to zarr")
    progress(persisted_values)

    for pv in persisted_values:
        try:
            dask.compute(pv)
        except Exception as e:
            print(f"exception {e}")
            failed.append(pv)

    print(f"\nnumber of failed planes: {len(failed)}")

    try:
        del pv
        del persisted_values
    except:
        pass

    for dv in tqdm(failed, ascii=True, dynamic_ncols=True, leave=True):
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

    return files, all_zarr_files


def blocks(lasers, sequence_name, save_root, offset, skew, chunk_size, start_index, crop_length, weighted_pixels, grid,
           affine_tf, delayed=False):
    files = {}
    results = []
    all_zarr_files = []
    for las in tqdm(lasers, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=True):
        directories = lasers[las]
        sample_dir = list(directories)[0]
        files[las] = []

        coordinate_file = util.copy_h5_files(sample_dir, save_root, sequence_name, las)

        for pzf_dir in tqdm(directories, desc='Directories   ', ascii=True, dynamic_ncols=True, leave=False):
            pzf_files = directories[pzf_dir]

            if pzf_dir == sample_dir:
                data = mod.decompress(pzf_files[0])
                sample = mod.merge(data, start_index, crop_length, weighted_pixels).compute()

            delayed_planes = [mod.convert_pzf(fn, skew, start_index, crop_length, weighted_pixels, coordinate_file,
                                              grid, offset, affine_tf, sample.shape) for fn in pzf_files]

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

            files[las].append(tmp_save_path)
            all_zarr_files.append(tmp_save_path)

    if delayed:
        failed = []
        persisted_values = dask.persist(*results)
        print("\nConverting PZF files to zarr")
        progress(persisted_values)

        for pv in persisted_values:
            try:
                dask.compute(pv)
            except Exception as e:
                print(f"exception {e}")
                failed.append(pv)

        print(f"\nnumber of failed planes: {len(failed)}")

        try:
            del pv
            del persisted_values
        except:
            pass

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

    return files, all_zarr_files


def no_save(session, filelist, sequence_name, save_root, offset, skew, line_weights):
    yscale_factor = session['Scale Factor']
    grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                           session['Y Pixel Size'] * yscale_factor)

    delayed_lasers = []
    for las in tqdm(filelist, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=True):
        stacks = filelist[las]
        sample_dir = list(stacks)[0]
        coordinate_file = util.copy_h5_files(sample_dir, save_root, sequence_name, las)
        sample = mod.compute_delayed_plane(stacks[sample_dir][0], skew, yscale_factor, line_weights,
                                           coordinate_file, grid, offset).compute()

        delayed_stacks = []
        for stack in tqdm(stacks, desc='Stacks        ', ascii=True, dynamic_ncols=True, leave=False):
            delayed_planes = [mod.convert_pzf(fn, skew, yscale_factor, line_weights, coordinate_file,
                                              grid, offset, sample.shape) for fn in stacks[stack]]
            delayed_stacks.append(da.stack(delayed_planes))
        delayed_lasers.append(da.concatenate(delayed_stacks, axis=1))
    return da.stack(delayed_lasers)


def deconv_blocks(session, filelist, sequence_name, chunks, save_root, offset, skew, line_weights,
                  img_res, deconv_overlap, psf, iterations, tmp_chunk_size=(1, 512, 512), nplanes=None):
    yscale_factor = session['Scale Factor']
    grid = 1e8 * np.arange(session['Image Start'], session['Image End'],
                           session['Y Pixel Size'] * yscale_factor)

    psf_invert = not session['Reversed']
    psf_path = psf['path']
    psf_res = psf['resolution']

    files = {}
    all_zarr_files = []
    l_bar = tqdm(filelist, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=True)
    for las in l_bar:
        stacks = filelist[las]
        sample_dir = list(stacks)[0]

        l_bar.set_postfix({'status': 'Copying h5 files'})
        coordinate_file = util.copy_h5_files(sample_dir, save_root, sequence_name, las)

        l_bar.set_postfix({'status': 'Computing sample'})
        sample = mod.compute_delayed_plane(stacks[sample_dir][0], skew, yscale_factor, line_weights,
                                           coordinate_file, grid, offset).compute()

        files[las] = []
        t_bar = tqdm(stacks, desc='Stacks   ', ascii=True, dynamic_ncols=True, leave=False)
        for stack in t_bar:
            t_bar.set_postfix({'status': 'Processing'})

            delayed_planes = [mod.convert_pzf(fn, skew, yscale_factor, line_weights, coordinate_file,
                                              grid, offset, sample.shape) for fn in stacks[stack]]
            da_stack = da.stack(delayed_planes)

            (z, x, y) = da_stack.shape

            if not nplanes:
                nplanes = math.ceil(5e9 / (x * y))

            tmp_block_dir = os.path.join(save_root, *stack.split(os.sep)[-2:])

            if not os.path.exists(tmp_block_dir):
                os.makedirs(tmp_block_dir)

            for zz in tqdm(range(0, z, nplanes), desc='Sub-stacks', ascii=True, dynamic_ncols=True, leave=False):
                sub_block = da_stack[zz:zz + nplanes, :, :]

                tmp_save_path = os.path.join(tmp_block_dir, f"{zz:04d}.zarr")
                store = zarr.NestedDirectoryStore(tmp_save_path)
                shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), da_stack.shape, tmp_chunk_size))
                z_out = zarr.create(shape=(sub_block.shape[0], shape[1], shape[2]), chunks=tmp_chunk_size,
                                    dtype=sub_block.dtype, store=store, overwrite=True, fill_value=0)

                while True:
                    t_bar.set_postfix({'status': 'Converting pzf sub stacks'})
                    try:
                        da.to_zarr(sub_block, z_out, overwrite=True, compressor='None')
                    except Exception as e:
                        t_bar.set_postfix({'status': f'Error occurred: {e}, retrying'})
                        print(f"exception {e}, retrying")
                        continue
                    break

            zarr_files = sorted(glob(os.path.join(tmp_block_dir, "*.zarr")))
            blocks = [da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(zz), mode='r')) for zz in zarr_files]

            dask_img = da.concatenate(blocks, axis=0)

            tmp_deconv_dir = tmp_block_dir + '_deconv'

            if not os.path.exists(tmp_deconv_dir):
                os.makedirs(tmp_deconv_dir)

            for zz in tqdm(range(0, z, nplanes), desc='Deconv sub-stacks', ascii=True, dynamic_ncols=True,
                           leave=False):
                if zz == 0:
                    img_substack = dask_img[zz:zz + nplanes + deconv_overlap[0], :, :]

                    # creating reflect-padding
                    padding = img_substack[:deconv_overlap[0], :, :]
                    padding = padding[::-1, :, :]

                    dask_substack = da.concatenate([padding, img_substack], axis=0)
                elif zz + nplanes > z:
                    img_substack = dask_img[zz - deconv_overlap[0]:zz + nplanes, :, :]

                    # creating reflect-padding
                    padding = img_substack[-deconv_overlap[0]:, :, :]
                    padding = padding[::-1, :, :]

                    dask_substack = da.concatenate([img_substack, padding], axis=0)

                else:
                    dask_substack = dask_img[zz - deconv_overlap[0]:zz + nplanes + deconv_overlap[0], :, :]

                deconv_save_path = os.path.join(tmp_deconv_dir, f"{zz:04d}.zarr")

                chunk_size = (dask_substack.shape[0], chunks[1], chunks[2])

                t_bar.set_postfix({'status': 'Re-chunking'})
                dask_substack = dask_substack.rechunk(chunk_size)

                if iterations:
                    dask_substack = deconvolve_parallel(dask_substack,
                                                        img_resolution=img_res,
                                                        chunk_size=chunk_size,
                                                        overlap=(0, deconv_overlap[1], deconv_overlap[2]),
                                                        psf_invert=psf_invert,
                                                        psf_path=psf_path,
                                                        psf_res=psf_res,
                                                        iterations=iterations)

                store_save = zarr.NestedDirectoryStore(deconv_save_path)
                zarr_out = zarr.create(dask_substack.shape, chunks=chunk_size, store=store_save, dtype='f4',
                                       overwrite=True)

                while True:
                    t_bar.set_postfix({'status': 'Deconvolving'})
                    try:
                        da.to_zarr(dask_substack, zarr_out, overwrite=True)
                    except Exception as e:
                        t_bar.set_postfix({'status': f'Error occurred: {e}, retrying'})
                        continue
                    break

            blocks = []
            for zz in range(0, z, nplanes):
                deconv_save_path = os.path.join(tmp_deconv_dir, f"{zz:04d}.zarr")
                da_img = da.from_zarr(zarr.open(zarr.storage.NestedDirectoryStore(deconv_save_path), mode='r'))
                blocks.append(da_img[deconv_overlap[0]:-deconv_overlap[0], :, :])

            deconv_stack = da.concatenate(blocks, axis=0)

            if chunks[0] == -1:
                chunk_size = util.opt_chunksize(deconv_stack.shape[0], (chunks[1], chunks[2]))
            else:
                chunk_size = chunks

            deconv_path = tmp_deconv_dir + '.zarr'
            store_save = zarr.NestedDirectoryStore(deconv_path)
            zarr_out = zarr.create(deconv_stack.shape, chunks=chunk_size, store=store_save, dtype='f4', overwrite=True)

            while True:
                t_bar.set_postfix({'status': 'Saving deconvolved'})
                try:
                    da.to_zarr(deconv_stack, zarr_out, overwrite=True)
                except Exception as e:
                    t_bar.set_postfix({'status': f'Error occurred: {e}, retrying'})
                    continue
                break

            t_bar.set_postfix({'status': 'Removing temp files'})
            shutil.rmtree(tmp_block_dir)
            shutil.rmtree(tmp_deconv_dir)

            files[las].append(deconv_path)
            all_zarr_files.append(deconv_path)

    return dfz.from_files(files)
