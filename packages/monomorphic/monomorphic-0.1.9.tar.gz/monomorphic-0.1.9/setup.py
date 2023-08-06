#!/usr/bin/env python
from setuptools import setup

# The name parameter is required if github is going to create dependency graphs
NAME = "monomorphic"
setup(
    name = NAME,
    setup_requires=['pbr'],
    pbr=True,
)
