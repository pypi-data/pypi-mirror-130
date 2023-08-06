# Standard library imports
import argparse
import ast
import json
import os

default_params = {
    'cluster': {
        'n_workers': 16,
        'threads_per_worker': 4,
        'memory_limit': "16GB"
    },
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

    parser.add_argument("--n_workers", type=int, default=params['cluster']['n_workers'],
                        help=f"Number of workers in local cluster [{params['cluster']['n_workers']}]")
    parser.add_argument("--threads_per_worker", type=int, default=params['cluster']['threads_per_worker'],
                        help=f"Number of threads per worker in local cluster  [{params['cluster']['threads_per_worker']}]")
    parser.add_argument("--memory_limit", default=params['cluster']['memory_limit'],
                        help=f"Memory limit per worker in local cluster  [{params['cluster']['memory_limit']}]")

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
