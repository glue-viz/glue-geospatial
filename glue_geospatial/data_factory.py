import numpy as np

import rasterio

from glue.core import Data
from glue.config import data_factory


def is_geospatial(filename):
    try:
        with rasterio.open(filename) as src:
            src.read()
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

    data = Data()

    with rasterio.open(filename) as src:
        for iband, band in enumerate(src.read()):
            # TODO: determine the proper labels for each band

            # NB: We have to flip the raw data in the up-down direction
            # as Glue plots using the matplotlib imshow argument `origin='lower'`
            # and otherwise the data comes up outside down.
            # WARNING: This may cause issues with other (non-matplotlib) image
            # viewers
            data.add_component(component=np.flipud(band.astype(float)),
                               label='Band {0}'.format(iband))

    return data
