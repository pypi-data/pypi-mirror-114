from setuptools import find_packages, setup
from distutils.core import Extension
from glob import glob

module = Extension("blendlib",
                    define_macros = [("MAJOR_VERSION", "1"),
                                     ("MINOR_VERSION", "0")],
                    include_dirs = ["/library"],
                    libraries = ["library/blendlib"],
                    library_dirs = ["/library"],
                    sources = ["library/blendlib.c"])

setup(
    name="photoblend",
    version="1.2.2",
    url="https://github.com/aausek/PhotoBlend",
    description="Photoblend is a custom PyQt5 & C++ image editor app with blending mode features, filters and other"
                "manipulation options to render unique and creative images.",
    license="MIT",
    author="Team Senioritis",
    install_requires=["wheel", "PySide2", "Pillow", "numpy", "wsl", "imagefilters"],
    packages=find_packages(include=["library", "library.*", ""]),
    include_package_data=True,
    data_files=["library/blendlib.so","assets/icon.png", "assets/blue.jpg", "assets/red.jpg",
                "assets/desert.jpg", "assets/fractal2.jpg", "assets/white.jpg", "assets/colorful.png", "assets/ring.png"],
    ext_modules=[module],
    entry_points={"console_scripts": ["photoblend=library.main:main"]},
)