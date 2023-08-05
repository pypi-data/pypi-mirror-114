"""
This file is part of APAV.

APAV is a python package for performing analysis and visualization on
atom probe tomography data sets.

Copyright (C) 2018 Jesse Smith

APAV is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

APAV is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with APAV.  If not, see <http://www.gnu.org/licenses/>.
"""

import setuptools
import re
from os.path import abspath, dirname

this_path = abspath(dirname(__file__))

version_str = ""
with open("./apav/__init__.py", "r") as file:
    text = file.read()
    matches = re.findall(r"^__version__\s*=\s*\"(.*)\".*", text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError(f"Could not determine APAV version from {len(matches)} matches")
    else:
        version_str = matches[0]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required_pkgs = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        required_pkgs.append(line.strip())

setuptools.setup(
    name="APAV",
    version=version_str,
    author="Jesse Smith",
    author_email="jesseds@protonmail.com",
    description="A Python library for Atom Probe Tomography analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=r"https://gitlab.com/jesseds/apav",
    packages=setuptools.find_packages(),
    keywords=["atom probe", "tomography", "field evaporation", "leap", "apt",
              "materials", "science"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires='>=3.7',
    setup_requires=required_pkgs,
    install_requires=required_pkgs,
    include_package_data=True,
)
