#!/usr/bin/env python3
import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="wattaged",
    version="0.1.0",
    packages=["wattaged"],
    description="wattaged is a utility that logs the consummed electricity and allows you to quickly compute the consummed kWh",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sam1902/wattaged",
    author="Samuel Prevost",
    author_email="samuel.prevost@pm.me",
    licence="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=["pandas"],
    entry_points={"console_scripts": ["wattage = wattaged.__main__:main"]},
)

print("wattage CLI is now installed, but to make it work, you still need to install the daemon. To do so, run the following and follow the instructions:")
print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/sam1902/wattaged/HEAD/install.sh)"')
