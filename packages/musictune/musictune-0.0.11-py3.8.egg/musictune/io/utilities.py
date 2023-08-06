import glob
import json
import math
import os
from ast import literal_eval
from glob import glob

import dask.array as da
import pkg_resources
import zarr


def read_config(config_path, session_to_process='', lasers_to_process='', pzf_dirs_to_process=''):
    f = open(config_path, "r")
    config = json.loads(f.read())
    f.close()

    root_dir = os.path.dirname(config_path)
    no_of_sessions = len(config['Sessions'])

    project = config['Basename']['Project']
    sample = config['Basename']['Sample']
    sequence = config['Basename']['Sequence']

    stp = range(*(session_format(session_to_process)).indices(no_of_sessions))

    sessions = {}
    idx = 0
    total_blocks = 0
    for s in stp:
        sessions[idx] = {}
        print(f'Imaging session: {s}')
        session = config['Sessions'][s]
        s_id = session['Session']
        s_dir = os.path.join(root_dir, s_id)

        lasers = session['Laser Sequence']
        print(f'\tFound laser sequences: {lasers}')

        ll = laser_format(lasers_to_process)
        ltp = ll if ll else lasers

        sessions[idx]['Files'] = {}
        for l in ltp:
            files = sorted(glob(os.path.join(s_dir, f"*{l}*")))
            pzf_dir = list(filter(os.path.isdir, files))
            print(f'\t{l}: {len(pzf_dir)} Blocks with {len(os.listdir(pzf_dir[0]))} planes')
            sessions[s]['Files'][l] = pzf_dir[pzf_dir_format(pzf_dirs_to_process)]
            total_blocks += len(sessions[s]['Files'][l])

        sessions[idx]['Image Start'] = session['YScan']['Image Start']
        sessions[idx]['Image End'] = session['YScan']['Image End']
        sessions[idx]['Pixel Size'] = session['YScan']['Pixel Size']
        sessions[idx]['Scale Factor'] = session['YScan']['Scale Factor']

        is_reversed = session['ZScan']['Z Increment'] < 0

        img_res_y = 1e6 * session['YScan']['Pixel Size'] * session['YScan']['Scale Factor']
        img_res_z = 1e6 * session['ZScan']['Z Increment']

        sessions[idx]['Image Resolution'] = (abs(img_res_z), 0.23325, img_res_y)
        sessions[idx]['session_id'] = s_id
        sessions[idx]['Reversed'] = is_reversed

        overlap = round(2048 - abs(1e6 * session['XScan']['X Increment']) / 0.23325)
        sessions[idx]['Overlap'] = overlap
        idx += 1

    return project, sample, sequence, sessions, total_blocks


def config_summary(config_path):
    f = open(config_path, "r")
    config = json.loads(f.read())
    f.close()

    project = config['Basename']['Project']
    sample = config['Basename']['Sample']
    root_dir = os.path.dirname(config_path)
    no_of_sessions = len(config['Sessions'])

    for s in range(no_of_sessions):
        session = config['Sessions'][s]

        is_reversed = session['ZScan']['Z Increment'] < 0
        print("Imaged from bottom to img" if is_reversed else "Imaged from img to bottom")

        img_res_y = 1e6 * session['YScan']['Pixel Size'] * session['YScan']['Scale Factor']
        img_res_z = 1e6 * session['ZScan']['Z Increment']

        img_res = (abs(img_res_z), 0.23325, img_res_y)
        print(f"Image resolution: {img_res}")

        overlap = round(2048 - abs(1e6 * session['XScan']['X Increment']) / 0.23325)
        print(f"Overlap between strips: {overlap}")
        print(f'\nImaging session: {s}')
        session = config['Sessions'][s]
        s_id = session['Session']
        s_dir = os.path.join(root_dir, s_id)

        lasers = session['Laser Sequence']
        print(f'\tFound laser sequences: {lasers}')

        for l in lasers:
            files = sorted(glob(os.path.join(s_dir, f"*{l}*")))
            pzf_dir = list(filter(os.path.isdir, files))
            print(f'\t{l}: {len(pzf_dir)} Blocks with {len(os.listdir(pzf_dir[0]))} planes')

    return project, sample


def get_files(directory, z_range=''):
    block = {}
    zr = z_range_format(z_range)
    block['pzf_files'] = sorted(glob(os.path.join(directory, "*.pzf")))[zr]
    return block


def z_range_format(string):
    if string == '':
        return slice(None)
    elif '-' in string:
        return slice(*map(int, string.split('-')))
    else:
        num = int(string)
        return slice(num, num + 1, 1)


def input_format(string):
    if '-' in string:
        return slice(*map(int, string.split('-')))
    else:
        return int(string)


def opt_chunksize(depth, xy_chunks=(256, 256), lower=200, upper=400):
    if depth < lower:
        chunk_d = depth
    else:
        divisor = 1
        chunk_d = depth
        while not (lower <= chunk_d < upper):
            divisor += 1
            chunk_d = math.ceil(depth / divisor)

    return (chunk_d,) + xy_chunks


def session_format(string):
    if string == '':
        return slice(None)
    elif '-' in string:
        return slice(*map(int, string.split('-')))
    else:
        num = int(string)
        return slice(num, num + 1, 1)


def laser_format(string):
    if string == '':
        return 0
    elif ',' in string:
        return string.split(',')
    else:
        return [string]


def pzf_dir_format(string):
    if string == '':
        return slice(None)
    elif '-' in string:
        return slice(*map(int, string.split('-')))
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


def parse_params(param={}):
    if param:
        config_path = param['config_path']

        # directories and range options
        s = param['range']['sessions']
        l = param['range']['lasers']
        d = param['range']['pzf_dirs']

        z_range = str(param['range']['z_range'])

        # Line weights and paramters
        line_weights_file = param['lines']['weights_file']
        if line_weights_file == "":
            resource_filename = pkg_resources.resource_filename("musictune", 'img/Weights.json')
            f = open(resource_filename, "r")
            weights = json.loads(f.read())
            f.close()
        else:
            f = open(line_weights_file, "r")
            weights = json.loads(f.read())
            f.close()

        option = param['lines']['weights_option']
        line_no = param['lines']['single_line_no']

        # Deconvolution parameters
        deconv_status = literal_eval(param['deconvolve']['status'])
        overlap = literal_eval(param['deconvolve']['overlap'])
        psf_path = param['deconvolve']['psf_path']
        psf_res = param['deconvolve']['psf_res']
        iterations = int(param['deconvolve']['iterations'])

        if psf_path == "measured":
            psf_path = pkg_resources.resource_filename("musictune", 'img/PSF/CV_us_640_fine.tif')
            psf_res = (0.23325, 0.23325, 0.23325)
        elif psf_path == "theoretical":
            psf_path = pkg_resources.resource_filename("musictune", 'img/PSF/PSF_16bit_full.tif')
            psf_res = (0.933, 0.933, 0.933)

        project_path = param['save']['save_path']

        td = param['save']['tmp_dir']
        user = os.getenv('USER')
        tmp_dir = os.path.join(os.environ.get(td), user)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        tmp_chunks = literal_eval(param['save']['tmp_chunks'])
        xy_chunks = literal_eval(param['save']['xy_chunks'])
        zchunk_range = [*map(int, param['save']['zchunk_range'].split('-'))]
    else:
        config_path = ''
        s, l, d, z_range = '', '', '', ''

        resource_filename = pkg_resources.resource_filename("musictune", 'img/Weights.json')
        f = open(resource_filename, "r")
        weights = json.loads(f.read())
        f.close()

        option = "merge"
        line_no = 0
        deconv_status = False
        overlap, psf_path, psf_res, iterations = '', '', '', ''

        tmp_dir = os.path.join('/hpc', os.environ.get('USER'), 'tmp')
        # tmp_dir = os.path.join(os.environ.get('TMP'), os.environ.get('USER'))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        project_path = ''
        tmp_chunks = (512, 512, 1)
        xy_chunks = (256, 256)
        zchunk_range = "200-300"
    return config_path, s, l, d, z_range, weights, option, line_no, deconv_status, overlap, psf_path, psf_res, iterations, tmp_dir, project_path, tmp_chunks, xy_chunks, zchunk_range


def stitching_summary(config_path, save_path=''):
    f = open(config_path, "r")
    config = json.loads(f.read())
    f.close()

    if save_path == '':
        zarr_conversion = config['ZARR Conversion']
        project_path = zarr_conversion['save']['save_path']
        save_path = os.path.join(project_path, config['Basename']["Sample"], config['Basename']["Sequence"])

    no_of_sessions = len(config['Sessions'])

    lasers = ['405', '488', '561', '640']

    stitch_groups = {}
    sub_grp = -1

    for s in range(no_of_sessions):

        session = config['Sessions'][s]
        overlap = round(2048 - abs(1e6 * session['XScan']['X Increment']) / 0.23325)
        img_res_y = 1e6 * session['YScan']['Pixel Size'] * session['YScan']['Scale Factor']
        img_res_z = abs(1e6 * session['ZScan']['Z Increment'])
        img_resolution = (img_res_z, 0.23325, img_res_y)

        file_path = os.path.join(save_path, session['Session'])
        for l in lasers:
            zarr_files = sorted(glob(file_path + f'/*{l}*.zarr'))
            base_idx = [int(os.path.basename(z).split('_')[-1][:-5]) for z in zarr_files]

            for b_id, (b, n) in enumerate(zip(base_idx, zarr_files)):
                if b_id == 0:
                    sub_grp += 1
                    stitch_groups[sub_grp] = {}
                    stitch_groups[sub_grp]['overlap'] = overlap
                    stitch_groups[sub_grp]['img_resolution'] = img_resolution
                    stitch_groups[sub_grp]['dimension'] = from_zarr(n).shape
                    stitch_groups[sub_grp]['files'] = [n]
                elif b == base_idx[b_id - 1] + 1 and from_zarr(n).shape == stitch_groups[sub_grp]['dimension']:
                    stitch_groups[sub_grp]['files'].append(n)
                else:
                    sub_grp += 1
                    stitch_groups[sub_grp] = {}
                    stitch_groups[sub_grp]['overlap'] = overlap
                    stitch_groups[sub_grp]['img_resolution'] = img_resolution
                    stitch_groups[sub_grp]['dimension'] = from_zarr(n).shape
                    stitch_groups[sub_grp]['files'] = [n]

    return config['Basename']['Project'], config['Basename']['Sample'], stitch_groups
