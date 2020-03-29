# prace s rastrovymi daty - rasterio / vypocet ndvi
import rasterio
from pprint import pprint

green = rasterio.open('data/B03-2018-05-06.tiff')

# print metadata
print("Bounds:", green.bounds)
for x in dir(green):
    print(x)
print("_" * 60)
print(green.count)
pprint(green.meta)
print("_" * 60)

# vypocet ndvi
with rasterio.open('data/B04-2018-05-06.tiff') as vis:
    vis_data = vis.read().astype(float)[0]  # pasmo 0 (band)

with rasterio.open('data/B08-2018-05-06.tiff') as nir:
    nir_data = nir.read().astype(float)[0]

ndvi = (nir_data - vis_data) / (nir_data + vis_data)
print(ndvi)

# zapis dat
# nadefinovat metadata (ev. jde kopirovat pomoci from copy import copy
# kwargs = red.meta
# kwargs.update(dtype=rasterio.float32, count=1, compress='lzw')
kwargs = {
    "count": 1,
    "driver": "GTiff",
    "crs": "+init=epsg:4326",
    "dtype": "float32",
    "width": ndvi.shape[1],
    "height": ndvi.shape[0],
    "nodata": -9999,
    "transform": (0.00017964690780272554, 0.0, 14.513969421386719, 0.0, -0.00011842547881016553, 48.866521538507754),
    "compress": "lzw"
}
with rasterio.open('data/ndvi.tif', 'w', **kwargs) as dst:
    dst.write_band(1, ndvi.astype(rasterio.float32))  # pasma u zapisu cislovana od 1

# vypocet ndwi (water index)
with rasterio.open('data/B12-2018-05-06.tiff') as swir:
    swir_data = swir.read().astype(float)[0]  # pasmo 0 (band)

ndwi = (nir_data - swir_data) / (nir_data + swir_data)

with rasterio.open('data/ndwi.tif', 'w', **kwargs) as dst:
    dst.write_band(1, ndwi.astype(rasterio.float32))  # pasma u zapisu cislovana od 1
print("_" * 60)

# Reklasicikace rastru
with rasterio.open('data/ndvi.tif') as ndvi:
    water = ndvi.read()

limit = 0.1

water[water < -1*limit] = -9999
water[water > limit] = -9999
water[(water >= -1.0*limit) & (water <= 0.1)] = 1

kwargs = ndvi.meta
kwargs.update(dtype=rasterio.int32, count=1, compress='lzw', nodata=-9999)
with rasterio.open('data/water.tif', 'w', **kwargs) as dst:
    dst.write_band(1, water[0].astype(rasterio.int32))
print("~" * 60)


# rozdeleni vypoctu podle oken / bloku rastru
from rasterio.windows import Window

with rasterio.open('data/B04-2018-05-06.tiff') as red:
    w = red.read(1, window=Window(0, 0, 512, 256))

print(w.shape)

# nastaveni, aby nacitana okna odpovidala blokum, podle kterych jsou ulozena data

