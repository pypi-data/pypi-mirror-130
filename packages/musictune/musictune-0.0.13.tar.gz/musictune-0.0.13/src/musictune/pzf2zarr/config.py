# Standard library imports
import json
import math
import os

# Third party imports
from glob import glob
import numpy as np
import pkg_resources
import skimage.transform as tf

# Local application imports
import musictune.pzf2zarr.utilities as util

weights_filename = pkg_resources.resource_filename("musictune", 'data/Weights.json')


class Config:

    def __init__(self, config_path):
        f = open(config_path, "r")
        self.config = json.loads(f.read())
        f.close()

        self.directory = os.path.dirname(config_path)

    def summary(self):
        print(f"Project: {self.config['Basename']['Project']}")
        print(f"Sample: {self.config['Basename']['Sample']}")
        print(f"Sequence: {self.config['Basename']['Sequence']}")

        no_of_sessions = len(self.config['Sessions'])

        for s in range(no_of_sessions):
            print(f'\nImaging session: {s}')
            session = self.config['Sessions'][s]

            is_reversed = session['ZScan']['Z Increment'] < 0
            print("Imaged from bottom to top" if is_reversed else "Imaged from top to bottom")

            img_res_y = 1e6 * session['YScan']['Pixel Size'] * session['YScan']['Scale Factor']
            img_res_z = 1e6 * session['ZScan']['Z Increment']

            print(f"Y resolution: {abs(img_res_y)} \u03BCm")
            print(f"Z resolution: {abs(img_res_z)} \u03BCm")

            s_id = session['Session']
            s_dir = os.path.join(self.directory, s_id)

            lasers = session['Laser Sequence']
            print(f'\tFound laser sequences: {lasers}')

            for l in lasers:
                files = sorted(glob(os.path.join(s_dir, f"*{l}*")))
                pzf_dir = list(filter(os.path.isdir, files))
                print(f'\t{l}: {len(pzf_dir)} Blocks with {len(os.listdir(pzf_dir[0]))} planes')

    def nsessions(self):
        return len(self.config['Sessions'])

    def id(self):
        return f"{self.config['Basename']['Project']}-{self.config['Basename']['Sample']}-{self.config['Basename']['Sequence']}"

    def sequence(self):
        return f"{self.config['Basename']['Sequence']}"

    def get_session(self, session_id):
        return SessionConfig(self.config['Sessions'][session_id], self.directory)


class SessionConfig:
    def __init__(self, session_config, directory):
        self.name = session_config['Session']
        self.directory = os.path.join(directory, self.name)
        self.lasers = session_config['Laser Sequence']
        self.img_start = session_config['YScan']['Image Start']
        self.img_end = session_config['YScan']['Image End']
        self.y_pixel = session_config['YScan']['Pixel Size']
        self.scale_factor = session_config['YScan']['Scale Factor']
        self.reversed = session_config['ZScan']['Z Increment'] < 0
        self.z_res = abs(1e6 * session_config['ZScan']['Z Increment'])
        self.y_res = 1e6 * session_config['YScan']['Pixel Size'] * session_config['YScan']['Scale Factor']
        self.x_increment = session_config['XScan']['X Increment']

    def get_pzf_files(self, lasers_range='', stack_range='', z_range=''):
        lr = self.lasers[util.str_format(lasers_range)]
        zr = util.str_format(z_range)
        sr = util.str_format(stack_range)

        files = {}
        for l in lr:
            files[l] = {}
            all_files = sorted(glob(os.path.join(self.directory, f"*{l}*")))
            all_stacks = list(filter(os.path.isdir, all_files))
            stacks = all_stacks[sr]

            for d in stacks:
                files[l][d] = sorted(glob(os.path.join(d, "*.pzf")))[zr]

        return files

    def add_config(self, xpixel, skew, offset):
        self.grid = 1e8 * np.arange(self.img_start, self.img_end, self.y_pixel * self.scale_factor)
        self.offset = offset
        self.skew = skew
        self.weights = get_line_weights()
        self.img_res = (self.z_res, xpixel, self.y_res)
        self.affine_tf = tf.AffineTransform(shear=math.atan((skew / self.scale_factor) / 1792))
        self.overlap = round(2048 - abs(1e6 * self.x_increment) / xpixel)


def get_line_weights():
    f = open(weights_filename, "r")
    weights = json.loads(f.read())
    f.close()

    weight = np.array(weights['Weight'])

    line = {'Start': weights['ReadCrop']['index'],
            'Length': weights['ReadCrop']['length'],
            'Weights': np.expand_dims(weight, 1) * np.array(weights['Weighted Pixels'])}

    return line
