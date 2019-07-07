from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'undefined'

__all__ = ['__version__', 'setup']


def setup():
    from .data_factory import geospatial_reader  # noqa
