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
            data.add_component(component=band.astype(float),
                               label='Band {0}'.format(iband))

    return data
