from pyproj import Proj
from glue.core.coordinates import Coordinates
from affine import Affine

__all__ = ['GeospatialLonLatCoordinates']


class GeospatialLonLatCoordinates(Coordinates):

    def __init__(self, raster_reader=None, affine=None, crs_dict=None, flipud=True):

        if raster_reader is None:

            if affine is None or crs_dict is None:
                raise ValueError("Either raster_reader or affine/crs_dict should be given")

        else:

            if affine is not None or crs_dict is not None:
                raise ValueError("Either raster_reader or affine/crs_dict should be given")

            affine = raster_reader.transform

            if flipud:
                M = raster_reader.shape[0]
                affine = Affine(affine.a, -affine.b, affine.c + affine.b * M,
                                affine.d, -affine.e, affine.f + affine.e * M)
            else:
                affine = raster_reader.transform

            crs_dict = raster_reader.crs.to_dict()

        self.affine = affine
        self.iaffine = ~self.affine
        self.crs_dict = crs_dict
        self.proj = Proj(**crs_dict)

        super().__init__(n_dim=2)

    @property
    def world_axis_names(self):
        return ['Longitude', 'Latitude']

    @property
    def world_axis_units(self):
        return ['deg', 'deg']

    def pixel_to_world_values(self, *pixel):
        x, y = self.affine * pixel
        world = self.proj(x, y, inverse=True)
        return world[0], world[1]

    def world_to_pixel_values(self, *world):
        x, y = self.proj(world[0], world[1])
        return self.iaffine * (x, y)

    def __gluestate__(self, context):
        return dict(affine=list(self.affine)[:6], crs_dict=self.crs_dict)

    @classmethod
    def __setgluestate__(cls, rec, context):
        return cls(affine=Affine(*rec['affine']), crs_dict=rec['crs_dict'])
