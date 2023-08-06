import argparse
import os
import shutil
from datetime import datetime

import musictune.io.operations as ops
import musictune.io.utilities as util
from distributed import Client
from musictune.UI.cli import print_logo

home = os.path.expanduser("~")
scheduler_path = os.path.join(home, '.tune-scheduler.json')


def main():
    print_logo()

    main_start_time = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("scout_file", help="Configuration file (scout.json)")
    parser.add_argument("--project_path", default=os.path.join('/hpc', os.environ.get('USER'), 'zarr'),
                        help="Project directory to save the processed output ['/hpc/$USER/zarr]")
    parser.add_argument("--tmp_dir", default=os.path.join('/hpc', os.environ.get('USER'), 'tmp'),
                        help="Temporary directory to save intermediate files ['/hpc/$USER/tmp]")
    parser.add_argument("--levels", type=int, default=3, help="Number of pyramid levels [3]")
    parser.add_argument("--nplanes", type=int, default=3, help="Number of planes to be processed at one time [3]")
    parser.add_argument("--xpixel", type=float, default=0.23325, help="resolution of the x pixel [0.23325]")
    parser.add_argument("--offset", type=int, default=300, help="Offset value for reverse imaging [300]")
    parser.add_argument("--skew", type=int, default=12, help="Skew value for imaging [12]")
    parser.add_argument("--cutoff", type=int, default=92, help="Cut off value when overlapping [92]")
    parser.add_argument("--laser_range", default='', help="Laser range [all]")
    parser.add_argument("--strip_range", default='', help="Strip range [all]")
    parser.add_argument("--z_range", default='', help="Z plane range [all]")
    parser.add_argument("--delayed", help="Force saving of PZF blocks to be not delayed but instant",
                        action="store_true")
    args = parser.parse_args()

    # Input parameters
    config_path = args.scout_file
    project_path = args.project_path
    tmp_dir = args.tmp_dir
    pyramid_levels = args.levels
    nplanes = args.nplanes
    xpixel = args.xpixel
    offset = args.offset
    skew = args.skew
    cutoff = args.cutoff
    laser_range = args.laser_range
    strip_range = args.strip_range
    z_range = args.z_range
    chunk_size = (2048, 512)

    project_name, sample_name, sequence_name, no_of_sessions = util.config_summary(config_path)

    tmp_root = os.path.join(tmp_dir, f'{project_name}-{sample_name}-{sequence_name}')
    if not os.path.exists(tmp_root):
        os.makedirs(tmp_root)

    project_root = os.path.join(project_path, f'{project_name}-{sample_name}-{sequence_name}')
    if not os.path.exists(project_root):
        os.makedirs(project_root)

    tmp_zarr_path = os.path.join(tmp_root, 'zarr')
    if not os.path.exists(tmp_zarr_path):
        os.makedirs(tmp_zarr_path)

    session_id = 0
    if no_of_sessions > 1:
        while True:
            session_id = input("Multiple sessions found. Enter session number to process[0]: ")
            try:
                if not session_id == '':
                    session_id = int(session_id)
            except:
                print("Invlid session number")
                continue
            break

    print("Registering client")
    client = Client(scheduler_file=scheduler_path)

    pzf_time = datetime.now()
    sessions_zarr, all_zarr_files = ops.pzf2zarr_block(config_path, tmp_root, offset, skew, chunk_size, str(session_id),
                                                       laser_range,
                                                       strip_range, z_range, delayed=args.delayed)
    print("\nElapsed time for pzf to zarr conversion:", datetime.now() - pzf_time)

    stitch_time = datetime.now()
    ops.stitch_zarr(sessions_zarr, project_root, tmp_root, xpixel, cutoff, chunk_size, pyramid_levels, from_blocks=True,
                    delayed_save=False)
    print("\nElapsed time for stitching and multi-scale image generation:", datetime.now() - stitch_time)

    print("\nElapsed total time:", datetime.now() - main_start_time)

    print("\nRemoving temporary files")
    shutil.rmtree(tmp_root, ignore_errors=True)
    client.close()


if __name__ == "__main__":
    main()
