import sys

import napari
from musictune.io.utilities import from_zarr


def main():
    if len(sys.argv[1:]) > 0:
        file_path = sys.argv[1]
    else:
        file_path = input("Provide a .zarr file path:")

    dask_image = from_zarr(file_path)
    print(dask_image)
    viewer = napari.view_image(dask_image[:, 5:, 2500:4500, 2500:4500], channel_axis=0, name=['561', '640'],
                               multiscale=Fase)

    napari.run()


if __name__ == "__main__":
    main()
