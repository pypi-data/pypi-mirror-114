#!/usr/bin/env python3
import os
import sys
import shutil
import setuptools

# Workaround issue in pip with "pip install -e --user ."
import site
site.ENABLE_USER_SITE = True

with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="trs-interface",
    version="1.3.2",
    author="Patrick Tapping",
    author_email="mail@patricktapping.com",
    description="Library for communicating with the TRSpectrometer interface device.",
    long_description=long_description,
    url="https://gitlab.com/ptapping/trs-interface",
    project_urls={
        "Documentation": "https://trs-interface.readthedocs.io/",
        "Source": "https://gitlab.com/ptapping/trs-interface",
        "Tracker": "https://gitlab.com/ptapping/trs-interface/-/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pyserial",
    ],
)
