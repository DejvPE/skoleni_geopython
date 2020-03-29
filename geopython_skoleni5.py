# Prace s rastrem - gdal (vytvoreni rastru, rasterizace vektoru)

from osgeo import gdal, ogr, osr

# počet pixelů ve směru os x a y, a hodnota pro nodata
pixel_size = 20
NoData_value = -9999

# název výstupního souboru
raster_fn = 'test.tif'

# hraniční souřadnice mřížky
x_min, x_max, y_min, y_max = (0, 100, 0, 100)

# prostorové rozlišení
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)

target_driver = gdal.GetDriverByName('GTiff')
target_ds = target_driver.Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))

band = target_ds.GetRasterBand(1)

import numpy as np
band.WriteArray(np.array([[0, 0, 0, 0, 0],
                [0, 10, 15, 10, 0],
                [0, 15, 25, 15, 0],
                [0, 10, 15, 10, 0],
                [0, 0, 0, 0, 0]]))

outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromEPSG(5514)
target_ds.SetProjection(outRasterSRS.ExportToWkt())  # !!! jiné než u vektorových dat

band.FlushCache()
print("_" * 60)

# Rasterizace vektorovych dat
from osgeo import gdal, ogr, osr

# počet pixelů ve směru os x a y, a hodnota pro nodata
pixel_size = 50
NoData_value = -9999
...
# název výstupního souboru
raster_fn = 'data/chko.tif'

# název vstupního vektorového souboru
vector_fn = 'data/chko.shp'
# otevření zdroje dat (DataSource)
source_ds = ogr.Open(vector_fn)
# načtení první vrstvy z datového zdroje
source_layer = source_ds.GetLayer()

# získat hraniční souřadnice
x_min, x_max, y_min, y_max = source_layer.GetExtent()

# vytvořit data source pro výstupní data
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)
tiff_driver = gdal.GetDriverByName('GTiff')
target_ds = tiff_driver.Create(raster_fn, x_res, y_res, 3, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))

outRasterSRS = osr.SpatialReference()
outRasterSRS.ImportFromEPSG(5514)
target_ds.SetProjection(outRasterSRS.ExportToWkt())  # !!! jiné než u vektorů

gdal.RasterizeLayer(target_ds,
                    [1, 2, 3],
                    source_layer,
                    burn_values=[255, 125, 0],
                    options=['ALL_TOUCHED=TRUE'])  # žádné mezery okolo znaku '='
target_ds.FlushCache()
print("_" * 60)
print("_" * 60)
