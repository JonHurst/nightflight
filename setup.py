#!/usr/bin/python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nightflight",
    version="0.9.1",
    author="Jon Hurst",
    author_email="jon.a@hursts.org.uk",
    description="Calculate night flying hours",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JonHurst/nightflight",
    packages=setuptools.find_packages(),
    install_requires=['astral>=2.2'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_data={"nightflight": ["airports.txt.bz2"]},
    python_requires='>=3.11',
)
