from setuptools import setup, find_packages
from codecs import open
from pathlib import Path

from minislurm.minislurm_client import version


here = Path(__file__).parent.absolute()

# Get the long description from the README file
with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="minislurm",
    version=version,
    author="S.V. Matsievskiy",
    author_email="matsievskiysv@gmail.com",
    maintainer="S.V. Matsievskiy",
    maintainer_email="matsievskiysv@gmail.com",
    url="https://gitlab.com/matsievskiysv/minislurm",
    description="Single machine resource manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="AGPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
    ],
    keywords="job queue",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    install_requires=["docopt"],
    entry_points={
        'console_scripts': ['minislurm_server = minislurm.minislurm_server:main',
                            'minislurm_client = minislurm.minislurm_client:main']
    }
)
