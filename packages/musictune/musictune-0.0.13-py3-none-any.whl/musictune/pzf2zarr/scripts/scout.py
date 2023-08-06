# Standard library imports
import os
import shutil
from datetime import datetime

# Local application imports
import musictune.pzf2zarr.params as paramsio
import musictune.pzf2zarr.utilities as util
from musictune.UI import cli
from musictune.pzf2zarr.channel import Channel
from musictune.pzf2zarr.config import Config
from musictune.pzf2zarr.session import Session
from musictune.pzf2zarr.stack import Stack

# Third party imports
from distributed import Client, LocalCluster
from tqdm.auto import tqdm

home = os.path.expanduser("~")
scheduler_path = os.path.join(home, '.tune-scheduler.json')
param_path = os.path.join(home, 'tune-param.json')


def main():
    try:
        main_start_time = datetime.now()
        cli.print_logo()

        params = paramsio.param_file(param_path)
        args = paramsio.get_args(params)

        print('Creating local cluster\n')
        cluster = LocalCluster(n_workers=args.n_workers,
                               threads_per_worker=args.threads_per_worker,
                               memory_limit=args.memory_limit,
                               local_directory=args.tmp_path)
        print(cluster)
        print(f'Dashboard: {cluster.dashboard_link}')

        print("\nRegistering client")
        client = Client(cluster)

        print(f'\nConfig_file: {args.scout_file}')
        config = Config(args.scout_file)
        config_id = config.id()
        config.summary()

        session_id = cli.get_session_id(config.nsessions())
        sconfig = config.get_session(session_id)
        sconfig.add_config(args.xpixel, args.skew, args.offset)
        file_list = sconfig.get_pzf_files(args.laser_range, args.strip_range, args.z_range)

        tmp_root = util.set_dir(args.tmp_path, config_id)
        project_root = util.set_dir(args.save_path, config_id)

        delayed_channels = []
        channel_props = []
        l_bar = tqdm(file_list, desc='Lasers        ', ascii=True, dynamic_ncols=True, leave=False)
        for las in l_bar:
            stacks_dir = file_list[las]

            l_bar.set_postfix({'status': 'Copying h5 files'})
            coordinate_file = util.copy_h5_files(list(stacks_dir)[0], tmp_root, config.sequence(), las)

            delayed_stacks = []
            s_bar = tqdm(stacks_dir, desc='Stacks   ', ascii=True, dynamic_ncols=True, leave=False)
            for s in s_bar:
                s_bar.set_postfix({'status': 'Processing stacks'})
                delayed_stacks.append(Stack.from_pzf(stacks_dir[s], sconfig, coordinate_file, las))

            channel = Channel.from_stacks(delayed_stacks, sconfig.overlap)
            channel.line_correction(args.cutoff, args.line_profile)
            channel.combine_stacks()
            channel.x_downscale(sconfig.scale_factor)
            channel = channel.to_zarr_planes(tmp_root, sconfig.name)
            channel.check_saturation()

            delayed_channels.append(channel)
            channel_props.append(channel.channel_prop())

        session = Session.from_channels(delayed_channels)
        session.chromatic_correction(sconfig.z_res, args.chromatic)
        session.multiscale_save(project_root, sconfig.name, tuple(args.scout_chunks), args.levels, channel_props)

        shutil.rmtree(tmp_root, ignore_errors=True)
        client.close()

        print("\nElapsed total time:", datetime.now() - main_start_time)

    except Exception as e:

        if 'cluster' in locals():
            print('Closing local cluster')
            cluster.close()

        temp = cli.remove_temp(e)
        if temp and 'tmp_root' in locals():
            print('Removing temporary files')
            shutil.rmtree(tmp_root, ignore_errors=True)

    if __name__ == "__main__":
        main()
