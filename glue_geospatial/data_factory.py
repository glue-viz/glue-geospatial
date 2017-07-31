import os

import numpy as np

import rasterio

from glue.core import Data
from glue.config import data_factory

from .coordinates import GeospatialLonLatCoordinates


def is_geospatial(filename):
    try:
        with rasterio.open(filename) as src:
            if src.count > 0:
                return True
        return False
    except:
        return False


@data_factory(
    label='Geospatial data',
    identifier=is_geospatial,
    priority=100,
)
def geospatial_reader(filename):
    """
    Read in geospatial data using the rasterio package

    Parameters
    ----------
    filename: str
        The input file
    """

    data = Data(label=os.path.basename(filename).split('.')[0])

    with rasterio.open(filename) as src:
        tags = src.tags()

        data.coords = GeospatialLonLatCoordinates(src, flipud=True)

        for iband, band in enumerate(src.read()):
            # Grab the 'tag' for the band
            band_tag = tags.get('Band_{0}'.format(iband + 1), '')

            # Use 'Band X - TAG' if the tag is present, if not just 'Band X'
            # Note that X is 1-based
            if band_tag == '':
                label = 'Band {id}'.format(id=iband + 1)
            else:
                label = 'Band {id} - {name}'.format(id=iband + 1,
                                                    name=band_tag)

            # NB: We have to flip the raw data in the up-down direction
            # as Glue plots using the matplotlib imshow argument `origin='lower'`
            # and otherwise the data comes up outside down.
            # WARNING: This may cause issues with other (non-matplotlib) image
            # viewers
            data.add_component(component=np.flipud(band.astype(float)),
                               label=label)

    return data
