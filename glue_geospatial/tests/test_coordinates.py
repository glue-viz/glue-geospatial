import pytest

import numpy as np
from numpy.testing import assert_allclose

from ..coordinates import MatrixCoordinates


class TestMatrixCoordinates():

    def setup_method(self, method):
        self.matrix = np.array([[1, 0, 3], [0, 1, 2], [0, 0, 1]])
        self.coords = MatrixCoordinates(self.matrix, ['y', 'x'])

    @pytest.mark.parametrize('ndim', range(4))
    def test_transform_scalar(self, ndim):

        shape = tuple(range(ndim))

        xp1 = np.random.random(shape)
        yp1 = np.random.random(shape)

        # Giving in scalars will return 1-element 1D arrays
        if ndim == 0:
            shape = (1,)

        xw, yw = self.coords.pixel2world(xp1, yp1)
        assert xw.shape == shape
        assert yw.shape == shape

        xp2, yp2 = self.coords.world2pixel(xw, yw)
        assert xp2.shape == shape
        assert yp2.shape == shape

        assert_allclose(xp1, xp2)
        assert_allclose(yp1, yp2)
