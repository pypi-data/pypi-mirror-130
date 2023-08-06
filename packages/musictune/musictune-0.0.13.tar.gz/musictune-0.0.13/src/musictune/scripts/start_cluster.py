import argparse
import os
import subprocess
import time
from os.path import expanduser


def main():
    home = expanduser("~")
    scheduler_path = os.path.join(home, '.tune-scheduler.json')

    parser = argparse.ArgumentParser()
    parser.add_argument("nworkers", type=int, help="number of workers")
    parser.add_argument("--nthreads", type=int, help="threads per workers")
    args = parser.parse_args()

    nworkers = args.nworkers

    if args.nthreads:
        nthreads = args.nthreads
    else:
        nthreads = 4

    sch_file = os.path.join(home, 'scheduler.json')
    if os.path.isfile(sch_file):
        print("A scheduler.json file already exists - removing it")
        os.remove(sch_file)

    os.system('killall -r dask-scheduler')
    os.system('killall -r dask-worker')
    scheduler = subprocess.Popen([f"dask-scheduler --scheduler-file {scheduler_path} --idle-timeout 3600"],
                                 shell=True)
    time.sleep(2)
    workers = []
    for i in range(nworkers):
        workers.append(
            subprocess.Popen(
                [f"dask-worker --nthreads {nthreads} --scheduler-file {scheduler_path} --local-directory $TMP/$USER"],
                shell=True))
        time.sleep(1)


if __name__ == "__main__":
    main()
