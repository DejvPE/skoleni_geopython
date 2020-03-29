# Modul OGR, nacteni dat, vytvoreni bufferu a ulozeni
import os
from osgeo import ogr

cesta = r"C:\Users\Skoleni-01\Desktop\data"

# Nacteni data source 
ds = ogr.Open(os.path.join(cesta, "chko.shp"))
if not ds:
    raise Exception("File not found")
print(ds)

print(dir(ds))  # vycet vsech atributu a metod
print("pocet vrstev: ", ds.GetLayerCount())

# Nacteni layer
layer = ds.GetLayer()

if not layer:
    raise Exception("Layer not avaliable")
print(layer)

# Zjisteni geometrie
print(layer.GetGeomType())  # jen cislo
print(layer.GetGeomType() == ogr.wkbPolygon)
print(layer.schema)
print(layer.schema[1])  # atributova pole
print(layer.schema[4])  # atributova pole

# prochazeni features
feature_count = layer.GetFeatureCount()
for i in list(range(feature_count)):
    feature = layer.GetNextFeature()
    print(feature.GetField("NAZEV"))

print(layer.GetFeature(54).GetField("NAZEV"))

# vytvoreni buferu kolem jednoho prvku
cr = layer.GetFeature(54)
geom = cr.GetGeometryRef()
print(geom.GetEnvelope())

centroid = geom.Centroid()
print(centroid)
print(centroid.GetPoint())

buff = centroid.Buffer(100)

# kontrola pruniku
print(geom.Intersects(buff))

# print(help(centroid))

print("____end____")


# ogr uklada na disk az po zavolani fce .Destroy() !!!

import fiona
for x in fiona.supported_drivers:
    print(x)
len(fiona.supported_drivers)