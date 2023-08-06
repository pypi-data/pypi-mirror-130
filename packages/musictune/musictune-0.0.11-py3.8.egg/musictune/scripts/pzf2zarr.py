import os
import shutil
import time
from os.path import expanduser

from distributed import Client
from musictune.deconvolution.deconvolve import deconvolve_parallel

from musictune.UI.cli import print_logo, cli_pzf2zarr

home = expanduser("~")
os.environ['MPLCONFIGDIR'] = os.path.join(home, '.matplotlib')

import h5py as h5
from musictune.io.modules import *
from musictune.io.utilities import *

scheduler_path = os.path.join(home, '.tune-scheduler.json')

import sys


def main():
    print_logo()

    if len(sys.argv[1:]) > 0:
        param_path = sys.argv[1]
    else:
        param_path = cli_pzf2zarr()

    f = open(param_path, "r")
    param = json.loads(f.read())
    f.close()

    config_path, s, l, d, z_range, weights, option, line_no, deconv_status, overlap, psf_path, psf_res, iterations, tmp_dir, project_path, tmp_chunks, xy_chunks, zchunk_range = parse_params(
        param)

    project, sample, sequence, sessions, total_blocks = read_config(config_path, s, l, d)

    save_root = os.path.join(project_path, sample)
    save_dir = os.path.join(save_root, sequence)

    start_index = weights['ReadCrop']['index']
    crop_length = weights['ReadCrop']['length']
    weight = np.array(weights['Weight'])
    weighted_pixels = np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels'])

    client = Client(scheduler_file=scheduler_path)
    start_time = time.time()

    elapsed_block_time = 0
    processed_blocks = 0

    block_time = time.time()
    for sess in sessions:
        print(f"Processing session: {sess}")
        img_res = sessions[sess]['Image Resolution']
        print(f"Image resolution: {img_res}")
        psf_invert = not sessions[sess]['Reversed']

        lasers = sessions[sess]['Files']
        grid = 1e8 * np.arange(sessions[sess]['Image Start'], sessions[sess]['Image End'],
                               sessions[sess]['Pixel Size'] * sessions[sess]['Scale Factor'])

        for las in lasers:
            print(f"\tProcessing Lasers: {las}")
            directories = lasers[las]
            h5_filepath = os.path.join(os.path.dirname(directories[0]), f'{sequence}_{las}.h5')

            for pzf_dir in directories:
                try:
                    eta = round((total_blocks - processed_blocks) * (elapsed_block_time / processed_blocks))
                except:
                    eta = 'N/A'

                print(f"\n\n\t\tNumber of blocks processed: {processed_blocks}/{total_blocks}")
                print(f"\t\tEstimated time remaining (seconds): {eta}")

                print(f"\n\n\t\tProcessing Block: {pzf_dir}")

                block = get_files(pzf_dir, z_range=z_range)

                sample = decompress(block['pzf_files'][0]).compute()

                delayed_planes = [decompress(fn) for fn in block['pzf_files']]
                delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4') for x in delayed_planes]

                da_line_planes = da.stack(delayed_planes)

                coordinate_file = h5.File(h5_filepath, 'r')
                coordinates = da.from_array(
                    np.expand_dims(
                        np.array([coordinate_file.get(os.path.basename(fn))[:] for fn in block['pzf_files']]),
                        1), chunks=(1, 1, da_line_planes.chunksize[-1]))

                ## Merge lines
                merge_chunk_size = (1, da_line_planes.chunksize[1], 1, da_line_planes.chunksize[3])

                da_planes = da.map_blocks(merge_lines, da_line_planes, weighted_pixels, option=option,
                                          start_index=start_index,
                                          crop_length=crop_length, line_no=line_no, chunks=merge_chunk_size,
                                          dtype='f4').squeeze()

                da_planes_repositioned = da.map_blocks(reposition_lines, da_planes, coordinates, grid, dtype='f4')

                save_path = os.path.join(save_dir, *pzf_dir.split(os.sep)[-2:]) + '.zarr'
                tmp_save_path = tmp_dir + save_path

                shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), da_planes.shape, tmp_chunks))

                store = zarr.NestedDirectoryStore(tmp_save_path)
                z_out = zarr.create(shape=shape, chunks=tmp_chunks, dtype=da_planes.dtype, store=store, overwrite=True,
                                    fill_value=0)

                print(f"\t\tSaving tmp image: {tmp_save_path}")
                da.to_zarr(da_planes_repositioned, z_out)

                chunk_size = opt_chunksize(da_planes.shape[0], xy_chunks, zchunk_range[0], zchunk_range[1])

                dask_img = from_zarr(tmp_save_path, chunk_size=chunk_size)
                print(f"\t\tRechunking image: {dask_img}")

                if deconv_status:
                    print("\t\tDeconvolving")

                    dask_img = deconvolve_parallel(dask_img,
                                                   img_resolution=img_res,
                                                   chunk_size=chunk_size,
                                                   overlap=overlap,
                                                   psf_invert=psf_invert,
                                                   psf_path=psf_path,
                                                   psf_res=psf_res,
                                                   iterations=iterations)

                path = to_zarr(dask_img, prefix='', chunk_size=chunk_size, save_path=save_path)

                print(f"\t\tSaved:{path}")

                shutil.rmtree(tmp_save_path)
                print("\t\tTmp file removed\n")
                elapsed_block_time = time.time() - block_time
                processed_blocks += 1

    elapsed_time = time.time() - start_time
    print("Elapsed total time: ", elapsed_time)

    f = open(config_path, "r")
    config = json.loads(f.read())
    f.close()

    config["ZARR Conversion"] = param
    config["ZARR Conversion"]["elapsed_time"] = elapsed_time
    with open(os.path.join(save_root, sequence + '.json'), 'w') as outfile:
        json.dump(config, outfile, indent=4)

    client.close()


if __name__ == "__main__":
    main()
