import os
import re

from setuptools import find_packages, setup

package = dict()

with open("r18ripper.py", "r") as f:
    lines = f.readlines()
    for line in lines:
        match = re.match(r"(__\w+?__)\s*=\s*(.+)$", line)
        if match:
            package[match.group(1)] = eval(match.group(2))

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

with open("requirements.txt") as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name=package["__title__"],
    version=package["__version__"],
    author=package["__author__"],
    py_modules=["r18ripper"],
    keywords=["r18", "r18.com", "webrip", "porn"],
    description=package["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities"
    ],
    entry_points = dict(
        console_scripts=[
            "r18-ripper = r18ripper:main"
        ],              
    ),
)