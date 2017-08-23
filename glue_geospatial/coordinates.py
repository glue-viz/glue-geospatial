from pyproj import Proj
import numpy as np
from astropy.wcs import WCS
from glue.core.coordinates import Coordinates
from astropy.visualization.wcsaxes.transforms import CurvedTransform
from astropy import units as u
from affine import Affine

__all__ = ['GeospatialLonLatCoordinates']


class GeospatialPixel2LonLat(CurvedTransform):

    def __init__(self, coords):
        super(GeospatialPixel2LonLat, self).__init__()
        self.coords = coords

    @property
    def input_dims(self):
        return 2

    def transform(self, pixel):
        if pixel.shape[1] != self.input_dims:
            raise ValueError("pixel.shape[1] != 2")
        if pixel.shape[0] == 0:
            return np.zeros((0, 2))
        else:
            return np.asarray(self.coords.pixel2world(pixel[:, 0], pixel[:, 1])).transpose()

    transform_non_affine = transform

    def inverted(self):
        return GeospatialLonLat2Pixel(self.coords)


class GeospatialLonLat2Pixel(CurvedTransform):

    def __init__(self, coords):
        super(GeospatialLonLat2Pixel, self).__init__()
        self.coords = coords

    @property
    def input_dims(self):
        return 2

    def transform(self, world):
        if world.shape[1] != self.input_dims:
            raise ValueError("world.shape[1] != 2")
        if world.shape[0] == 0:
            return np.zeros((0, 2))
        else:
            return np.asarray(self.coords.world2pixel(world[:, 0], world[:, 1])).transpose()

    transform_non_affine = transform

    def inverted(self):
        return GeospatialPixel2LonLat(self.coords)


class GeospatialLonLatCoordinates(Coordinates):

    def __init__(self, raster_reader=None, affine=None, crs_dict=None, flipud=True):

        if raster_reader is None:

            if affine is None or crs_dict is None:
                raise ValueError("Either raster_reader or affine/crs_dict should be given")

        else:

            if affine is not None or crs_dict is not None:
                raise ValueError("Either raster_reader or affine/crs_dict should be given")

            affine = raster_reader.affine

            if flipud:
                M = raster_reader.shape[0]
                affine = Affine(affine.a, -affine.b, affine.c + affine.b * M,
                                affine.d, -affine.e, affine.f + affine.e * M)
            else:
                affine = raster_reader.affine

            crs_dict = raster_reader.crs.to_dict()

        self.affine = affine
        self.iaffine = ~self.affine
        self.crs_dict = crs_dict
        self.proj = Proj(**crs_dict)
        self.axis_labels = ['Latitude', 'Longitude']

    def axis_label(self, axis):
        return self.axis_labels[axis]

    def pixel2world(self, *pixel):
        x, y = self.affine * pixel
        world = self.proj(x, y, inverse=True)
        return world[0], world[1]

    def world2pixel(self, *world):
        x, y = self.proj(world[0], world[1])
        return self.iaffine * (x, y)

    @property
    def wcsaxes_dict(self):
        """
        Dictionary to initialize WCSAxes
        """
        wcsaxes_dict = {}
        wcsaxes_dict['transform'] = GeospatialPixel2LonLat(self)
        wcsaxes_dict['coord_meta'] = {}
        wcsaxes_dict['coord_meta']['name'] = ['Longitude', 'Latitude']
        wcsaxes_dict['coord_meta']['type'] = ['scalar', 'scalar']
        wcsaxes_dict['coord_meta']['wrap'] = [None, None]
        wcsaxes_dict['coord_meta']['unit'] = [u.deg, u.deg]
        return wcsaxes_dict

    def dependent_axes(self, axis):
        return (0, 1)

    def __gluestate__(self, context):
        return dict(affine=list(self.affine)[:6], crs_dict=self.crs_dict)

    @classmethod
    def __setgluestate__(cls, rec, context):
        return cls(affine=Affine(*rec['affine']), crs_dict=rec['crs_dict'])


class MatrixCoordinates(Coordinates):

    def __init__(self, matrix, axis_labels):
        self.matrix = np.array(matrix)
        self.matrix_invert = np.linalg.inv(matrix)
        self.axis_labels = axis_labels

    def axis_label(self, axis):
        return self.axis_labels[axis]

    def pixel2world(self, *args):
        args = np.broadcast_arrays(*(args + ([1],)))
        shape_orig = args[0].shape
        args = [arg.ravel() for arg in args]
        result = np.matmul(self.matrix, args)[:-1]
        return [arg.reshape(shape_orig) for arg in result]

    def world2pixel(self, *args):
        args = np.broadcast_arrays(*(args + ([1],)))
        shape_orig = args[0].shape
        args = [arg.ravel() for arg in args]
        result = np.matmul(self.matrix_invert, args)[:-1]
        return [arg.reshape(shape_orig) for arg in result]

    @property
    def wcs(self):
        # We provide a wcs property since this can then be used by glue to
        # display world coordinates. In this case, the transformation matrix is
        # in the same order as the WCS convention so we don't need to swap
        # anything.
        wcs = WCS(naxis=self.matrix.shape[0] - 1)
        wcs.wcs.cd = self.matrix[:-1, :-1]
        wcs.wcs.crpix = np.zeros(wcs.naxis)
        wcs.wcs.crval = self.matrix[:-1, -1]
        wcs.wcs.ctype = self.axis_labels[::-1]
        return wcs
