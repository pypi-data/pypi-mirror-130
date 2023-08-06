# Standard library imports
import math
import os

# Third party imports
import dask.array as da
import zarr
# Local application imports
from musictune.deconvolution.deconvolve import deconvolve_parallel
from musictune.pzf2zarr.strip import Strip


class Stack:

    def __init__(self, delayed_stack, laser, resolution):
        self.img = delayed_stack
        self.laser = laser
        self.resolution = resolution

    @classmethod
    def from_pzf(cls, pzf_dir, session, coordinate_file, laser):

        sample_path = pzf_dir[0]
        sample_coordinates = coordinate_file.get(os.path.basename(sample_path))[:]
        sample_strip = Strip(sample_path, session.weights, sample_coordinates, session.grid, session.offset,
                             session.skew, session.affine_tf)
        shape = sample_strip.compute().shape

        delayed_strips = []
        for path in pzf_dir:
            coordinates = coordinate_file.get(os.path.basename(path))[:]
            strip = Strip(path, session.weights, coordinates, session.grid, session.offset, session.skew,
                          session.affine_tf)
            delayed_strips.append(strip.delayed(shape))

        return cls(da.stack(delayed_strips), laser, session.img_res)

    @classmethod
    def from_zarr(cls, path, img_res, laser, chunk_size=None):

        zarr_img = zarr.open(zarr.storage.NestedDirectoryStore(path), mode='r')
        if chunk_size is None:
            chunk_size = zarr_img.chunks
        return cls(da.from_zarr(zarr_img, chunks=chunk_size), laser, resolution=img_res)

    def to_zarr(self, save_path, chunk_size=None, retry=True):
        store = zarr.NestedDirectoryStore(save_path)
        if chunk_size is None:
            chunk_size = self.img.chunk_size

        # reshape image to be multiple of chunk size with zero padding
        shape = tuple(map(lambda x, c: (math.ceil(x / c) * c), self.img.shape, chunk_size))
        z_out = zarr.create(shape=shape, chunks=chunk_size, dtype=self.img.dtype, store=store, overwrite=True,
                            fill_value=0)

        if retry:
            while True:
                try:
                    da.to_zarr(self.img, z_out, overwrite=True)
                except Exception as e:
                    print(f"exception {e}, retrying")
                    continue
                break
        else:
            da.to_zarr(self.img, z_out, overwrite=True)
        return save_path

    def deconvolve(self, chunk_size, overlap, psf_invert, psf_path, psf_res, iterations):
        self.img = self.img.rechunk(chunk_size)
        self.img = deconvolve_parallel(self.img,
                                       img_resolution=self.resolution,
                                       chunk_size=chunk_size,
                                       overlap=overlap,
                                       psf_invert=psf_invert,
                                       psf_path=psf_path,
                                       psf_res=psf_res,
                                       iterations=iterations)
