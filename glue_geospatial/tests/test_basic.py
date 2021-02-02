import os

from numpy.testing import assert_allclose

from glue_geospatial.data_factory import is_geospatial, geospatial_reader

DATA = os.path.join(os.path.dirname(__file__), 'data')


def test_geospatial(tmpdir):

    assert not is_geospatial(os.path.join(DATA, 'plain.tif'))
    assert is_geospatial(os.path.join(DATA, 'simplegeo.tif'))

    data = geospatial_reader(os.path.join(DATA, 'simplegeo.tif'))
    assert data.shape == (18, 24)

    assert_allclose(data.coords.pixel_to_world_values(9, 12),
                    (-3.9716666666666676, 2.9816666666666665))
