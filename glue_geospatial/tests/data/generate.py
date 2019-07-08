# Script used to generate simplegeo.tif

import numpy as np
import rasterio
from rasterio.transform import from_origin

x = np.linspace(-4.0, 4.0, 24)
y = np.linspace(-3.0, 3.0, 18)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-2 * np.log(2) * ((X - 0.5) ** 2 + (Y - 0.5) ** 2) / 1 ** 2)
Z2 = np.exp(-3 * np.log(2) * ((X + 0.5) ** 2 + (Y + 0.5) ** 2) / 2.5 ** 2)
Z = 10.0 * (Z2 - Z1)

res = (x[-1] - x[0]) / 2400.0
transform = from_origin(x[0] - res / 2, y[-1] + res / 2, res, res)

new_dataset = rasterio.open(
    'simplegeo.tif',
    'w',
    driver='GTiff',
    height=Z.shape[0],
    width=Z.shape[1],
    count=1,
    dtype=Z.dtype,
    crs='+proj=latlong',
    transform=transform,
)

new_dataset.write(Z, 1)
new_dataset.close()
