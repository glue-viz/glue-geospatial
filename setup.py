#!/usr/bin/env python

from __future__ import print_function

from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
glue_geospatial=glue_geospatial:setup
"""

with open('glue_geospatial/version.py') as infile:
    exec(infile.read())

with open('README.rst') as infile:
    LONG_DESCRIPTION = infile.read()

setup(name='glue-geospatial',
      version=__version__,
      description='Experimental glue plugin for geospatial imagery',
      long_description=LONG_DESCRIPTION,
      url="https://github.com/glue-viz/glue-geospatial",
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      packages=find_packages(),
      package_data={},
      entry_points=entry_points,
      install_requires=['glue-core', 'rasterio', 'pyproj'])
