# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:39:15 2021

@author: jakeb
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cov19DashJacobBeeson",
    version="0.0.1",
    author="Jacob Beeson",
    author_email="jtb215@exeter.ac.uk",
    description="A a simple personalised covid information dashboard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JacobBeeson/Cov19Dashboard.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
