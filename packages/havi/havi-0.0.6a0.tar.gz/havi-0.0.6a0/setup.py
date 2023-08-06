# read the contents of your README file
from pathlib import Path

from setuptools import find_packages, setup

from havi import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="havi",
    version=__version__,
    description="perform bayesian inference over physical models",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/bjornaer/havi",
    download_url="https://github.com/bjornaer/havi/archive/refs/tags/v.0.0.6-alpha.tar.gz",
    author="Francisco Grings, Maximiliano Schulkin",
    author_email="max.schulkin@gmail.com",
    keywords = ['physics', 'scatering', 'bayesian', 'inference', 'data', 'science'],
    packages=find_packages(include=["havi"]),
    license="Apache2.0",
    install_requires=["numpy", "torch", "pyro-ppl", "pyro-api", "pandas", "seaborn"],
    classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Physics',

    # Pick your license as you wish
    'License :: OSI Approved :: Apache Software License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
  ],
)
