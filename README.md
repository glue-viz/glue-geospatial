Experimental glue plugin for satellite imagery
==============================================

[![Build Status](https://travis-ci.org/glue-viz/glue-geospatial.svg)](https://travis-ci.org/glue-viz/glue-geospatial?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/l2raw1i7avo013rv/branch/master?svg=true)](https://ci.appveyor.com/project/glue-viz/glue-geospatial/branch/master)

Requirements
------------

Note that this plugin requires [glue](http://glueviz.org/) to be installed -
see [this page](http://glueviz.org/en/latest/installation.html) for
instructions on installing glue.

In addition, this plugin requires the [rasterio](https://mapbox.github.io/rasterio/) package to be installed (which in turn depends on [GDAL](http://www.gdal.org)). If you are using conda, you can easily install all required dependencies with:

    conda install -c conda-forge rasterio

Installing the plugin
---------------------

To install the latest developer version of the plugin from the git
repository, you can do:

    pip install https://github.com/glue-viz/glue-geospatial/archive/master.zip

This will auto-register the plugin with Glue.

Using
-----

At the moment, this plugin provides a reader based on rasterio. You can give
glue any file that can be read by rasterio, e.g.:

    glue mydata.tif

and you can also load files from inside glue.

Testing
-------

To run the tests, do:

    py.test glue_geospatial

at the root of the repository. This requires the [pytest](http://pytest.org)
module to be installed.
