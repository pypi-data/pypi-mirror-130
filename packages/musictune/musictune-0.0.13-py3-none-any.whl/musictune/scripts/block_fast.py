# Standard library imports
import os
import shutil
from datetime import datetime

# Local application imports
import musictune.io.PZF_conversion as pzfc
import musictune.io.Zarr_stitching as zstitch
import musictune.io.delayed_from_zarr as dz
import musictune.io.modules as mod
import musictune.io.params as paramsio
import musictune.io.utilities as util
from musictune.UI import cli

# Third party imports
from distributed import Client

home = os.path.expanduser("~")
scheduler_path = os.path.join(home, '.tune-scheduler.json')
param_path = os.path.join(home, 'tune-param.json')


def main():
    main_start_time = datetime.now()
    cli.print_logo()

    params = paramsio.param_file(param_path)
    args = paramsio.get_args(params)

    print(f'\nConfig_file: {args.scout_file}')
    print("\nRegistering client")
    client = Client(scheduler_file=scheduler_path)

    project, sample, sequence, no_sessions = util.config_summary(args.scout_file)
    session_id = cli.get_session_id(no_sessions)
    session = util.get_pzf_files(args.scout_file, str(session_id),
                                  args.laser_range, args.strip_range, args.z_range)[0]

    config_id = f"{project}-{sample}-{sequence}"
    tmp_root = util.set_dir(args.tmp_path, config_id)
    project_root = util.set_dir(args.save_path, config_id)

    line_weights = paramsio.get_line_weights()
    filelist = session['files']

    print("\nGenerating delayed objects")
    delayed_session = pzfc.no_save(session, filelist, sequence, tmp_root, args.offset, args.skew, line_weights)

    session_name = session['session_id']
    tmp_plane_path = util.set_dir(tmp_root, session_name, 'planes')
    overlap = round(2048 - abs(1e6 * session['X Increment']) / args.xpixel)
    yscale_factor = session['Scale Factor']
    z_resolution = session['Z Resolution']
    laser_keys = [l for l in filelist]
    saved_path = zstitch.to_planes(delayed_session, tmp_plane_path, overlap, yscale_factor, args.cutoff,
                                   laser_keys, z_resolution, args.chromatic, args.line_profile)
    img = dz.from_dir(saved_path, is_blocks=False)

    channel_props = []
    colours = {'640': "FF0000", '561': "00FF00", '488': "0000FF", '405': "FF00FF"}
    max_val = 65535

    for id, las in enumerate(filelist):
        channel_props.append({"active": "true",
                              "coefficient": 1,
                              "color": colours[las],
                              "family": "linear",
                              "inverted": "false",
                              "label": 'Laser ' + las,
                              "window":
                                  {
                                      "end": 2000,
                                      "max": max_val,
                                      "min": 0,
                                      "start": 10
                                  }
                              })

    print("\nSaving multi scale images.")
    img_res = (session['Z Resolution'], args.xpixel, session['Y Resolution'])
    mod.multiscale_save(img, project_root, session_name, tuple(args.block_chunks), img_res, args.levels, channel_props)
    shutil.rmtree(tmp_root, ignore_errors=True)
    client.close()

    print("\nElapsed total time:", datetime.now() - main_start_time)


if __name__ == "__main__":
    main()
