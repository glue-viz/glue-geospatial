#!/usr/bin/env python

from __future__ import print_function

from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
glue_satellite=glue_satellite:setup
"""

try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md') as infile:
        LONG_DESCRIPTION = infile.read()

with open('glue_satellite/version.py') as infile:
    exec(infile.read())

setup(name='glue-satellite',
      version=__version__,
      description='Experimental glue plugin for satellite imagery',
      long_description=LONG_DESCRIPTION,
      url="https://github.com/glue-viz/glue-satellite",
      author='',
      author_email='',
      packages = find_packages(),
      package_data={},
      entry_points=entry_points
    )
