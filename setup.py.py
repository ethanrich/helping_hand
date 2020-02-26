import setuptools
from distutils.core import setup
from pathlib import Path

with (Path(__file__).parent / "readme.md").open("r") as f:
    long_description = f.read()

setup(
    name="helping_hand",
    version="0.0.1",
    description="Control stimulation on one hand with EMG of other",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ethan Rich",
    author_email="robert.guggenberger@uni-tuebingen.de",
    url="https://github.com/ethanrich/helping_hand.git",
    download_url="https://github.com/ethanrich/helping_hand.git",
    license="MIT",
    packages=["helping_hand"],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries",
    ],
)
