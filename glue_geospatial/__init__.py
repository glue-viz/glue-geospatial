from ._version import __version__

__all__ = ['__version__', 'setup']


def setup():
    from .data_factory import geospatial_reader  # noqa
