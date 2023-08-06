# This file is placed in the Public Domain.

import os
import shutil

from setuptools import setup
from setuptools.command.install import install

p = "/usr/local/share/botd/botd.service"
d = "/etc/systemd/system/botd.service"

def read():
    return open("README.rst", "r").read()

setup(
    name="botd",
    version="49",
    url="https://github.com/bthate/botd",
    author="Bart Thate",
    author_email="bthate@dds.nl",
    description="24/7 channel daemon",
    long_description=read(),
    license="Public Domain",
    zip_safe=True,
    include_package_data=True,
    py_modules=["ob", "trm"],
    packages=["bot"],
    data_files=[
        (
            "share/botd/",
            [
                "files/bot.1.md",
                "files/botctl.8.md",
                "files/botd.8.md",
                "files/botd.service",
                "files/botd",
            ],
        ),
    ],
    scripts=["bin/bot", "bin/botcmd", "bin/botctl", "bin/botd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
