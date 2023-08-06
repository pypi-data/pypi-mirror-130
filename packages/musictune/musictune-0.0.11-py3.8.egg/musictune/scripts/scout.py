import argparse
from datetime import datetime

import h5py as h5
from dask.diagnostics import ProgressBar
from distributed import Client
from musictune.UI.cli import print_logo
from musictune.io.modules import *
from musictune.io.utilities import *
from tqdm import tqdm

home = os.path.expanduser("~")
os.environ['MPLCONFIGDIR'] = os.path.join(home, '.matplotlib')
scheduler_path = os.path.join(home, '.tune-scheduler.json')


def intensity_clip(da_img, lp=0.02, up=0.02):
    min_val = np.min(da_img[::5, ::5, ::5]).compute()
    max_val = np.max(da_img[::5, ::5, ::5]).compute()
    print("Image range:", (min_val, max_val))

    bins = np.maximum(10000, math.ceil(max_val - min_val))
    h, bins = da.histogram(da_img[::5, ::5, ::5], bins=bins, range=[min_val, max_val])
    hist = h.compute()

    cumsum = np.cumsum(hist)
    cumsum_percent = cumsum / np.max(cumsum)

    if lp > 0:
        imin = bins[next(i for i, v in enumerate(cumsum_percent) if v > lp)]
    else:
        imin = min_val

    if up < 1:
        imax = bins[next(i for i, v in enumerate(cumsum_percent) if v > 1 - up)]
    else:
        imax = max_val

    print(f'imin={imin}, imax={imax}')

    return imin, imax


def subsample_zarr(z, g, level, dtype='uint16'):
    '''Subsample a zar pyramid level

    Parameters
    ----------
    z : zarr array
        The level to subsample
    g: zarr group
        The zarr file group to save the new level into
    level: str
        The name of the new level in the group
    '''
    d = da.from_zarr(z)
    if d.shape[1] % 2:
        # odd z
        d = d[:, :-1, :, :]

    if d.shape[2] % 2:
        # odd x
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        # odd y
        d = d[:, :, :, :-1]

    dn = (d[:, ::2, ::2, ::2] + d[:, ::2, 1::2, ::2] + d[:, ::2, ::2, 1::2] + d[:, ::2, 1::2, 1::2]
          + d[:, 1::2, ::2, ::2] + d[:, 1::2, 1::2, ::2] + d[:, 1::2, ::2, 1::2] + d[:, 1::2, 1::2, 1::2]) / 8

    zn = g.empty(str(level), shape=dn.shape, chunks=(1, 1, 256, 256), dtype=dtype)
    dn.to_zarr(zn)
    return zn, dn.shape


def subsample_xy(z, g, level, dtype='uint16'):
    '''Subsample a zar pyramid level

    Parameters
    ----------
    z : zarr array
        The level to subsample
    g: zarr group
        The zarr file group to save the new level into
    level: str
        The name of the new level in the group
    '''
    d = da.from_zarr(z)
    if d.shape[2] % 2:
        # odd x
        d = d[:, :, :-1, :]

    if d.shape[3] % 2:
        # odd y
        d = d[:, :, :, :-1]

    dn = (d[:, :, ::2, ::2] + d[:, :, 1::2, ::2] + d[:, :, ::2, 1::2] + d[:, :, 1::2, 1::2]) / 4

    zn = g.empty(str(level), shape=dn.shape, chunks=(1, 1, 256, 256), dtype=dtype)
    dn.to_zarr(zn)
    return zn, dn.shape


def resample(img, scale_factor, y_chunksize=512, dtype='u2'):
    # chunk_size = (1, img.shape[1], y_chunksize)
    # img = img.rechunk(chunk_size)
    chunk_size = img.chunksize
    re_chunks = (chunk_size[0], round(chunk_size[1] / scale_factor), chunk_size[2])
    return da.map_blocks(sum_lines, img, scale_factor, chunks=re_chunks, dtype=dtype)


def sum_lines(img, scale_factor):
    y_shape = img.shape[1]
    y_limit = math.floor(y_shape / scale_factor) * scale_factor
    line = img[:, 0:y_limit:scale_factor, :]

    for i in range(1, scale_factor):
        line += img[:, i:y_limit:scale_factor, :]

    return line


def create_line_weights(overlap, cutoff, adjustment):
    lw_start, lw_mid, lw_end = np.ones((2048,)), np.ones((2048,)), np.ones((2048,))
    lw_start[-cutoff:] = 0
    lw_start[-overlap + cutoff:-cutoff] = np.linspace(1, 0, overlap - 2 * cutoff)
    lw_start *= adjustment
    lw_mid[:cutoff] = 0
    lw_mid[-cutoff:] = 0
    lw_mid[cutoff:overlap - cutoff] = np.linspace(0, 1, overlap - 2 * cutoff)
    lw_mid[-overlap + cutoff:-cutoff] = np.linspace(1, 0, overlap - 2 * cutoff)
    lw_mid *= adjustment
    lw_end[:cutoff] = 0
    lw_end[cutoff:overlap - cutoff] = np.linspace(0, 1, overlap - 2 * cutoff)
    lw_end *= adjustment

    return np.expand_dims(lw_start[:-overlap], axis=(0, -1)), np.expand_dims(lw_start[-overlap:],
                                                                             axis=(0, -1)), np.expand_dims(
        lw_mid[:overlap], axis=(0, -1)), np.expand_dims(lw_mid[overlap:-overlap], axis=(0, -1)), np.expand_dims(
        lw_end[overlap:], axis=(0, -1))


def find_line_profile(files):
    m_all = []

    for f in files:
        m = np.mean(from_zarr(f)[::10, :, ::10], axis=(0, 2)).compute()
        m_all.append(m)

    m_median = np.median(np.array(m_all), axis=0)
    mean_line_norm = (m_median + 1e-10) / (np.max(m_median))
    return np.minimum(1 / mean_line_norm, 100)


def main():
    print_logo()

    pbar = ProgressBar()
    pbar.register()

    main_start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("scout_file", help="Configuration file (scout.json)")
    parser.add_argument("--project_path", help="Project directory to save the processed output ['/hpc/$USER/zarr]")
    parser.add_argument("--tmp_dir", help="Temporary directory to save intermediate files ['/hpc/$USER/tmp]")
    parser.add_argument("--levels", type=int,help="Number of pyramid levels [3]")
    parser.add_argument("--no_convert", help="Skip PZF to Zarr conversion step", action="store_true")
    parser.add_argument("--no_stitch", help="Skip PZF to Zarr conversion and stitching steps", action="store_true")
    args = parser.parse_args()

    # Input parameters
    config_path = args.scout_file

    if args.project_path:
        project_path = args.project_path
    else:
        project_path = os.path.join('/hpc', os.environ.get('USER'), 'zarr')

    if args.tmp_dir:
        tmp_dir = args.tmp_dir
    else:
        tmp_dir = os.path.join('/hpc', os.environ.get('USER'), 'tmp')

    if args.levels:
        pyramid_levels = args.levels
    else:
        pyramid_levels = 3

    # Default parameters
    option = "merge"
    line_no = 0

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    project, sample, sequence, sessions, total_blocks = read_config(config_path)

    tmp_root = os.path.join(tmp_dir, f'{project}-{sample}-{sequence}')

    resource_filename = pkg_resources.resource_filename("musictune", 'img/Weights.json')
    f = open(resource_filename, "r")
    weights = json.loads(f.read())
    f.close()

    start_index = weights['ReadCrop']['index']
    crop_length = weights['ReadCrop']['length']
    weight = np.array(weights['Weight'])
    weighted_pixels = np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels'])

    client = Client(scheduler_file=scheduler_path)

    if not (args.no_convert):
        print("\n-----------PZF to ZARR-----------\n")
        start_time = datetime.now()

        for sess in tqdm(sessions, desc='Sessions  ', ascii=True, dynamic_ncols=True):

            lasers = sessions[sess]['Files']
            grid = 1e8 * np.arange(sessions[sess]['Image Start'], sessions[sess]['Image End'],
                                   sessions[sess]['Pixel Size'] * sessions[sess]['Scale Factor'])

            for las in tqdm(lasers, desc='Lasers    ', dynamic_ncols=True, ascii=True, leave=False):
                directories = lasers[las]
                h5_filepath = os.path.join(os.path.dirname(directories[0]), f'{sequence}_{las}.h5')
                coordinate_file = h5.File(h5_filepath, 'r')

                for pzf_dir in tqdm(directories, desc='PZF Blocks', ascii=True, dynamic_ncols=True, leave=False):
                    block = get_files(pzf_dir)

                    if pzf_dir == directories[0]:
                        sample = decompress(block['pzf_files'][0]).compute()

                    delayed_planes = [decompress(fn) for fn in block['pzf_files']]
                    delayed_planes = [da.from_delayed(x, shape=sample.shape, dtype='f4') for x in delayed_planes]

                    da_line_planes = da.stack(delayed_planes)

                    ## Merge lines
                    merge_chunk_size = (1, da_line_planes.chunksize[1], 1, da_line_planes.chunksize[3])

                    da_planes = da.map_blocks(merge_lines, da_line_planes, weighted_pixels, option=option,
                                              start_index=start_index,
                                              crop_length=crop_length, line_no=line_no, chunks=merge_chunk_size,
                                              dtype='f4').squeeze()

                    if len(da_planes.shape) == 2:
                        da_planes = da.stack([da_planes])

                    coordinates = da.from_array(
                        np.expand_dims(
                            np.array([coordinate_file.get(os.path.basename(fn))[:] for fn in block['pzf_files']]),
                            1), chunks=(1, 1, da_line_planes.chunksize[-1]))

                    da_planes_repositioned = da.map_blocks(reposition_lines, da_planes, coordinates, grid, dtype='f4')

                    tmp_save_path = os.path.join(tmp_root, *pzf_dir.split(os.sep)[-2:]) + '.zarr'

                    tmp_chunks = (1, 2048, 512)
                    shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), da_planes.shape, tmp_chunks))

                    store = zarr.NestedDirectoryStore(tmp_save_path)
                    z_out = zarr.create(shape=shape, chunks=tmp_chunks, dtype=da_planes.dtype, store=store,
                                        overwrite=True,
                                        fill_value=0)
                    da.to_zarr(da_planes_repositioned, z_out, compute=False)

        print("Elapsed time for conversion: ", datetime.now() - start_time)

    if not args.no_stitch:
        print("\n----------Stitching groups----------\n")
        start_time = datetime.now()

        project, sample, stitch_groups = stitching_summary(config_path, tmp_root)
        print(f"Stitch groups found = {len(stitch_groups)} ")
        for g in stitch_groups:
            print(
                f"Group {g}: {stitch_groups[g]['files'][0]} to {os.path.basename(stitch_groups[g]['files'][-1])} ({len(stitch_groups[g]['files'])} blocks)")

        line_file_path = "measure"
        # line_file_path = pkg_resources.resource_filename("musictune", 'img/line_profile.csv')
        # line_profile = np.genfromtxt(line_file_path, delimiter=',')
        # adjustment = np.minimum(1 / line_profile, 5)
        cutoff = 92
        save_dtype = 'u2'

        for s in tqdm(stitch_groups, desc='Group     ', ascii=True, dynamic_ncols=True):
            # print(f'Stitch group: {s}')

            files = stitch_groups[s]['files']
            overlap = stitch_groups[s]['overlap']
            img_resolution = stitch_groups[s]['img_resolution']
            # print(stitch_groups[s])

            scale_factor = int(img_resolution[2] / img_resolution[1])
            # print(f'Scaling factor of x: {scale_factor}')

            if line_file_path == 'measure':
                adjustment = find_line_profile(files)

            first, dip, rise, mid, last = create_line_weights(overlap, cutoff, adjustment)

            blocks = []

            current = from_zarr(files[0])
            following = from_zarr(files[1])

            blocks.append(resample(current[:, :-overlap, :] * first, scale_factor))
            blocks.append(resample(current[:, -overlap:, :] * dip + following[:, :overlap, :] * rise, scale_factor))

            for idx in tqdm(range(1, len(files) - 1), desc='Files     ', ascii=True, dynamic_ncols=True, leave=False):
                current = following
                following = from_zarr(files[idx + 1])

                blocks.append(resample(current[:, overlap:-overlap, :] * mid, scale_factor))
                blocks.append(resample(current[:, -overlap:, :] * dip + following[:, :overlap, :] * rise, scale_factor))

            current = following
            blocks.append(resample(current[:, overlap:, :] * last, scale_factor))

            combined = da.concatenate(blocks, axis=1)
            save_chunks = (1, 512, 512)

            dir_name = os.path.dirname(files[0])
            start_block = os.path.basename(files[0])[:-5]
            end_block = os.path.basename(files[-1]).split('_')[-1]
            save_path = f'{dir_name}_{start_block}_to_{end_block}'
            # print(save_path)

            shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), combined.shape, save_chunks))

            store_save = zarr.NestedDirectoryStore(save_path)
            zarr_out = zarr.create(shape, chunks=save_chunks, store=store_save, dtype=save_dtype, fill_value=0,
                                   overwrite=True)

            da.to_zarr(combined, zarr_out)
            print(f'Shape of the stitched image: {combined.shape}')

        print("Elapsed time for stitching:", datetime.now() - start_time)

    print("\n----------Combining channels----------\n")
    start_time = datetime.now()

    channels = []
    channel_props = []
    colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}

    for sess in tqdm(sessions, desc='Sessions  ', ascii=True, dynamic_ncols=True):
        img_res = sessions[sess]['Image Resolution']
        session_name = sessions[sess]['session_id']

        groups = sorted(glob(tmp_root + f'/*{session_name}*.zarr'))
        # print(f"Groups found: {groups}")
        for idx, f in tqdm(enumerate(groups), desc='Groups', ascii=True, dynamic_ncols=True, leave=False):
            img = from_zarr(f)
            channels.append(img)

            base_name = os.path.basename(f)

            if '_561_' in base_name:
                laser = '561'
            elif '_640_' in base_name:
                laser = '640'
            elif '_488_' in base_name:
                laser = '488'
            else:
                laser = '405'

            ch_min, ch_max = intensity_clip(img)

            channel_props.append({"active": "true",
                                  "coefficient": 1,
                                  "color": colours[laser],
                                  "family": "linear",
                                  "inverted": "false",
                                  "label": 'Laser ' + laser,
                                  "window":
                                      {
                                          "end": ch_max,
                                          "max": 65535,
                                          "min": 0,
                                          "start": ch_min
                                      }
                                  })
        da_4d = da.stack(channels)
        # print(f'Shape: {da_4d.shape}')

        save_path = os.path.join(project_path, sample, sequence, f'{session_name}.zarr')

        store = zarr.NestedDirectoryStore(save_path)
        zarr_group = zarr.group(store=store, overwrite=True)

        level_0 = zarr_group.empty('0', shape=da_4d.shape, chunks=da_4d.chunksize, dtype='u2')
        da_4d.to_zarr(level_0)

        prev_level = level_0
        prev_shape = da_4d.shape
        prev_res = img_res

        datasets = [{"path": "0"}]

        for i in tqdm(range(1, pyramid_levels), desc='Levels    ', ascii=True, dynamic_ncols=True, leave=False):
            if prev_res[0] >= 2 * prev_res[1] or prev_shape[1] == 1:
                prev_level, prev_shape = subsample_xy(prev_level, zarr_group, i)
                prev_res = (prev_res[0], 2 * prev_res[1], 2 * prev_res[2])
            else:
                prev_level, prev_shape = subsample_zarr(prev_level, zarr_group, i)
                prev_res = (2 * prev_res[0], 2 * prev_res[1], 2 * prev_res[2])
            datasets.append({"path": "{}".format(i)})

        name = f"{project}-{sample}-{sequence}-{session_name}"
        zattrs = {
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

        print("Elapsed time for assembly:", datetime.now() - start_time)

        print("\nRemoving temporary files")

    # shutil.rmtree(tmp_root)
    client.close()

    print("\nElapsed total time:", datetime.now() - main_start_time)


if __name__ == "__main__":
    main()
