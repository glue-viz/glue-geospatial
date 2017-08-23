Experimental glue plugin for satellite imagery
==============================================

|Build Status| |Build status|

Requirements
------------

Note that this plugin requires `glue <http://glueviz.org/>`__ to be
installed - see `this
page <http://glueviz.org/en/latest/installation.html>`__ for
instructions on installing glue.

In addition, this plugin requires the
`rasterio <https://mapbox.github.io/rasterio/>`__ and
`pyproj <https://github.com/jswhit/pyproj>`__ packages to be
installed.

Installing
----------

If you are using conda, you can easily install the
plugin and all the required dependencies with::

    conda install -c glueviz glue-geospatial

Alternatively, if you don't use conda, be sure to install the above
dependencies then install the plugin with::

    pip install glue-geospatial

This will auto-register the plugin with Glue.

Using
-----

At the moment, this plugin provides a reader based on rasterio. You can
give glue any file that can be read by rasterio. For example, if
``mydata.tif`` is a GeoTIFF file, you can do::

    glue mydata.tif

and you can also load files from inside glue.

Testing
-------

To run the tests, do::

    py.test glue_geospatial

at the root of the repository. This requires the
`pytest <http://pytest.org>`__ module to be installed.

.. |Build Status| image:: https://travis-ci.org/glue-viz/glue-geospatial.svg
   :target: https://travis-ci.org/glue-viz/glue-geospatial?branch=master
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/l2raw1i7avo013rv/branch/master?svg=true
   :target: https://ci.appveyor.com/project/glue-viz/glue-geospatial/branch/master
