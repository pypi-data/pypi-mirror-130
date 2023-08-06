# -*- coding: utf-8; mode: python -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhgl",
    version="0.0.3",
    author="jintao",
    author_email="jintaos2@zju.edu.cn",
    description="a python like hdl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=None,
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)