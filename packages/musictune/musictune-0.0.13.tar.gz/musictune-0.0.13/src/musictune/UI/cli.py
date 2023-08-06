import os
from os.path import expanduser

import numpy as np
import termplotlib as tpl

home = expanduser("~")
os.environ['MPLCONFIGDIR'] = os.path.join(home, '.matplotlib')

from musictune.io.utilities import *


def print_logo():
    print(r"""
         __  __        ____ ___ _____   __                 
        |  \/  | _   _/ ___|_ _/ ___|  / /___  ______  ___ 
        | |\/| || | | \___ \| | |     / __/ / / / __ \/ _ \
        | |  | || |_| |___) | | |___ / /_/ /_/ / / / /  __/
        |_|  |_/| ._,_|____/___\____|\__/\__,_/_/ /_/\___/ 
                |_|                                    """)


def remove_temp(e):
    temp = input(f"\nException occurred: {e}. Do you want to remove temporary files [y]: ")
    return temp == '' or temp == 'y'


def get_session_id(no_of_sessions):
    session_id = 0
    if no_of_sessions > 1:
        while True:
            session_id = input("Multiple sessions found. Enter session number to process[0]: ")
            try:
                if not session_id == '':
                    session_id = int(session_id)
            except:
                print("Invalid session number")
                continue
            break
    return session_id


def cli_pzf2zarr():
    print("You need to enter parameters in this mode; alternatively, you can provide a json file as an argument.")

    param = {}
    while True:
        config_path = input("Enter path to sequence.json (e.g. BlockR.json):")
        if not os.path.isfile(config_path):
            print("Invalid file path.")
            continue
        else:
            project, sample = config_summary(config_path)
            param['config_path'] = config_path
            break

    param['range'] = {}
    range_mod = input("Change the processing range? (y/[n]):")
    if range_mod == 'y':
        while True:
            s = input("\tSessions (range | [all]): ")
            try:
                session_format(s)
                param['range']['sessions'] = s
                break
            except:
                print("\tInvalid input")

        while True:
            l = input("\tLaser wavelength (561,640 | [all]): ")
            try:
                laser_format(l)
                param['range']['lasers'] = l
                break
            except:
                print("\tInvalid input")

        while True:
            d = input("\tBlocks (range | [all]): ")
            try:
                pzf_dir_format(d)
                param['range']['pzf_dirs'] = d
                break
            except:
                print("\tInvalid input")

        while True:
            z_range = input("\tZ-planes (range | [all]): ")
            try:
                z_range_format(z_range)
                param['range']['z_range'] = z_range
                break
            except:
                print("\tInvalid input")
    else:
        param['range']['sessions'] = ""
        param['range']['lasers'] = ""
        param['range']['pzf_dirs'] = ""
        param['range']['z_range'] = ""

    param['lines'] = {}
    line_mod = input("Modify the line merging options? (y/[n]):")
    if line_mod == 'y':
        while True:
            line_weights_file = input("\tEnter path to line_weights.json [default]:")
            if not (os.path.isfile(line_weights_file) or line_weights_file == ""):
                print("\tInvalid file path.")
                continue
            else:
                param['lines']['weights_file'] = line_weights_file
                break

        while True:
            option = input("\tChoose a method to combine lines (single | [merge]):")
            if not option in ["", "merge", "single"]:
                print("\tInvalid choice")
                continue
            elif option == "":
                param['lines']['weights_option'] = "merge"
                break
            else:
                param['lines']['weights_option'] = option
                break

        if option == "single":
            while True:
                line_no = int(input("\tChoose a line number from 0 to 7:"))
                if not 0 <= line_no <= 7:
                    print("\tInvalid line number")
                    continue
                else:
                    param['lines']['single_line_no'] = 0
                    break
        else:
            param['lines']['single_line_no'] = 0
    else:
        param['lines']['weights_file'] = ""
        param['lines']['weights_option'] = "merge"
        param['lines']['single_line_no'] = 0

    param['deconvolve'] = {}
    ds = input("Deconvolve the blocks (y/[n]):")
    if ds == 'y':
        param['deconvolve']['status'] = "True"
        while True:
            overlap = input("\tEnter overlaps between chunks [(64,32,32)]:")
            if overlap == "":
                param['deconvolve']['overlap'] = "(64,32,32)"
                break
            else:
                try:
                    literal_eval(overlap)
                    param['deconvolve']['overlap'] = overlap
                    break
                except:
                    print("\tInvalid overlap value")

        while True:
            psf_path = input("\tPSF file ( filepath | theoretical | [measured] ):")
            if psf_path == "":
                psf_path = 'measured'
                param['deconvolve']['psf_path'] = psf_path
                break
            elif psf_path in ['measured', 'theoretical']:
                param['deconvolve']['psf_path'] = psf_path
                break
            elif os.path.isfile(psf_path):
                param['deconvolve']['psf_path'] = psf_path
                break
            else:
                print("\tInvalid PSF file path")
                continue

        if not psf_path in ['measured', 'theoretical']:
            while True:
                psf_res = input("\tPSF resolution in \mum (e.g. (0.9,0.9,0.9)):")
                try:
                    literal_eval(psf_res)
                    param['deconvolve']['psf_res'] = psf_res
                    break
                except:
                    print("Invalid resolution value")
        else:
            param['deconvolve']['psf_res'] = ""

            while True:
                iterations = input("\tEnter deconvolution iterations ([30]): ")
                if iterations == "":
                    iterations = 30
                    param['deconvolve']['iterations'] = iterations
                    break
                else:
                    try:
                        int(iterations)
                        param['deconvolve']['iterations'] = iterations
                        break
                    except:
                        print("\tInvalid iterations value")
    else:
        param['deconvolve']['status'] = "False"
        param['deconvolve']['overlap'] = "(0,0,0)"
        param['deconvolve']['psf_path'] = ""
        param['deconvolve']['psf_res'] = ""
        param['deconvolve']['iterations'] = "0"

    param['save'] = {}
    project_path = os.path.join('/hpc', os.getenv('USER'), 'zarr')
    while True:
        save_path_mod = input(f"Save directory [{project_path}]: ")
        if save_path_mod != "":
            project_path = save_path_mod

        try:
            if not os.path.exists(project_path):
                os.makedirs(project_path)
            break
        except:
            print("Invalid directory path")

    param['save']['save_dir'] = 'TMP'
    param['save']['chunk_size'] = "(1,512,512)"
    param['save']['xy_chunks'] = "(256,256)"
    param['save']['zchunk_range'] = "200-300"
    param['save']["save_path"] = project_path

    param_path = f'pzf2zarr-{project}-{sample}-{os.path.basename(config_path)}'
    with open(param_path, 'w') as outfile:
        json.dump(param, outfile, indent=4)

    print(f"Saved successfully at {param_path}")
    return param_path


def plot_line_profiles(line_profiles, laser_keys):
    for i, l in enumerate(laser_keys):
        if len(line_profiles.shape) > 1:
            lp = line_profiles[i, :]
        else:
            lp = line_profiles

        fig = tpl.figure()
        fig.plot(np.arange(2048), lp, label=f"Laser:{l}", width=200, height=20)
        fig.show()
