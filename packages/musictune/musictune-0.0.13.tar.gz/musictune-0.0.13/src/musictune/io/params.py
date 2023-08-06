# Standard library imports
import argparse
import ast
import json
import os

# Third party imports
import dask
import h5py
import numpy as np
import pkg_resources

default_params = {
    'path': {
        'save': os.path.join('/hpc', os.environ.get('USER'), 'zarr'),
        'tmp': os.path.join('/hpc', os.environ.get('USER'), 'tmp')
    },
    'range': {
        'laser': '',
        'strip': '',
        'plane': ''
    },
    'pzf2zarr': {
        'reverse_offset': 300,
        'skew': 12
    },
    'deconv': {
        'psf': 'measured',
        'iterations': 20,
        'deconv_overlap': (32, 16, 16)
    },
    'stitch': {
        'line_profile': 'default',
        'xpixel': 0.23325,
        'cutoff': 92,
        'chromatic': 'crop'
    },
    'multi_res': {
        'scout_chunks': (1, 1536, 1536),
        'block_chunks': (-1, 256, 256),
        'levels': 3
    }
}

PSF = {
    'measured': {
        'path': pkg_resources.resource_filename("musictune", 'data/PSF/CV_us_640_fine.tif'),
        'resolution': (0.23325, 0.23325, 0.23325)
    },
    'theoretical': {
        'path': pkg_resources.resource_filename("musictune", 'data/PSF/PSF_16bit_full.tif'),
        'resolution': (1, 1, 1)
    }
}
chromatic_offsets = {'405': 0, '488': 44, '561': 68, '640': 80}
weights_filename = pkg_resources.resource_filename("musictune", 'data/Weights.json')
line_file_path = pkg_resources.resource_filename("musictune", 'data/line_profile.h5')


def param_file(param_path):
    '''Load Default Parameters'''
    path = os.path.join(param_path)
    if os.path.exists(path):
        with open(path, 'r') as infile:
            params = json.load(infile)
        # Update parameters that were not in the parameter file
        for group in default_params:
            if group not in params:
                params[group] = default_params[group]
            else:
                try:
                    for key in default_params[group]:
                        if key not in params[group]:
                            params[group][key] = default_params[group][key]
                except:
                    continue
    else:
        params = default_params

    # Write out updated parameters
    with open(path, 'w') as outfile:
        json.dump(params, outfile, indent=4)
    return params


def get_args(params):
    parser = argparse.ArgumentParser()
    parser.add_argument("scout_file", help="Configuration file (scout.json)")
    parser.add_argument("--save_path", default=params['path']['save'],
                        help=f"Directory to save the processed output [{params['path']['save']}]")
    parser.add_argument("--tmp_path", default=params['path']['tmp'],
                        help=f"Temporary path to save intermediate files [{params['path']['tmp']}]")

    parser.add_argument("--laser_range", default=params['range']['laser'],
                        help=f"Laser range [{params['range']['laser']}]")
    parser.add_argument("--strip_range", default=params['range']['strip'],
                        help=f"Strip range [{params['range']['strip']}]")
    parser.add_argument("--z_range", default=params['range']['plane'],
                        help=f"Z plane range [{params['range']['plane']}]")

    parser.add_argument("--offset", type=int, default=params['pzf2zarr']['reverse_offset'],
                        help=f"Offset value for reverse imaging [{params['pzf2zarr']['reverse_offset']}]")
    parser.add_argument("--skew", type=int, default=params['pzf2zarr']['skew'],
                        help=f"Skew value for imaging [{params['pzf2zarr']['skew']}]")

    parser.add_argument("--psf", default=params['deconv']['psf'],
                        help=f"PSF for deconvolution (measured|theoretical) [{params['deconv']['psf']}]")
    parser.add_argument("--iterations", type=int, default=params['deconv']['iterations'],
                        help=f"Number of deconvolution iterations [{params['deconv']['iterations']}]")
    parser.add_argument("--deconv_overlap", type=ast.literal_eval, default=params['deconv']['deconv_overlap'],
                        help=f"Overlap value for deconvolution [{params['deconv']['deconv_overlap']}]")

    parser.add_argument("--line_profile", default=params['stitch']['line_profile'],
                        help=f"Line profile adjustment (default|measure|path) [{params['stitch']['line_profile']}]")
    parser.add_argument("--xpixel", type=float, default=params['stitch']['xpixel'],
                        help=f"resolution of the x pixel [{params['stitch']['xpixel']}]")
    parser.add_argument("--cutoff", type=int, default=params['stitch']['cutoff'],
                        help=f"Cut off value when overlapping [{params['stitch']['cutoff']}]")
    parser.add_argument("--chromatic", default=params['stitch']['chromatic'],
                        help=f"Chromatic correction option (crop|pad) [{params['stitch']['chromatic']}]")

    parser.add_argument("--levels", type=int, default=params['multi_res']['levels'],
                        help=f"Number of pyramid levels [{params['multi_res']['levels']}]")
    parser.add_argument("--scout_chunks", type=ast.literal_eval, default=params['multi_res']['scout_chunks'],
                        help=f"Size of scout chunks [{params['multi_res']['scout_chunks']}]")
    parser.add_argument("--block_chunks", type=ast.literal_eval, default=params['multi_res']['block_chunks'],
                        help=f"Size of block chunks [{params['multi_res']['block_chunks']}]")

    return parser.parse_args()


def get_chromatic_offset():
    return chromatic_offsets


def get_psf(type):
    if type == 'measured':
        return PSF['measured']
    else:
        return PSF['theoretical']


def get_line_weights():
    f = open(weights_filename, "r")
    weights = json.loads(f.read())
    f.close()

    weight = np.array(weights['Weight'])

    line = {'Start': weights['ReadCrop']['index'],
            'Length': weights['ReadCrop']['length'],
            'Weights': dask.delayed(np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels']))}

    return line


def get_line_profile(lasers):
    line_profile = h5py.File(line_file_path, 'r')
    line_profiles = []

    for l in lasers:
        profile = np.array(line_profile.get(l))
        profile /= np.max(profile)
        line_profiles.append(profile)

    return np.stack(line_profiles)
