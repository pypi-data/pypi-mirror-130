import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musictune",
    version="0.0.13",
    author="vibujithan",
    author_email="author@example.com",
    description="Parallel image processing package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vibujithan/musictune",
    project_urls={
        "Bug Tracker": "https://github.com/vibujithan/musictune/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={
        "console_scripts": ['tune-pzf2zarr = musictune.scripts.pzf2zarr:main',
                            'tune-cluster = musictune.scripts.start_cluster:main',
                            # 'tune-stitchzarr = musictune.scripts.stitching:main',
                            # 'tune-scout = musictune.scripts.scout:main',
                            'tune-block = musictune.scripts.block:main',
                            'tune-scout = musictune.pzf2zarr.scripts.scout:main',
                            'tune-scout-fast = musictune.scripts.scout_fast:main',
                            'tune-block-fast = musictune.scripts.block_fast:main',
                            'tune-zarr2tif = musictune.scripts.zarr2tif:main']
    },
    python_requires=">=3.6",
    package_data={
        "musictune": ["data/**", "data/PSF/**"],
        "": ["examples/**"]
    }
)
