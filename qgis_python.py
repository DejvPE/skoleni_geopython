# Skript spoustet primo z editoru v QGISu
# _pyqgis

# nacte vrstvy a vypise nazvy, pokud je vektor tak i pocet prvku
# for layer in QgsProject.instance().mapLayers().values():
#     if layer.type() == QgsMapLayer.VectorLayer:
#         print(layer.name(), layer.featureCount())
#     else:
#         print(layer.name())
# 
# print("_" * 80)

#  u viditelnych vrstev vypise atribut a spocita plochu
# for layer in QgsProject.instance().mapLayers().values():
#     if not QgsProject.instance().layerTreeRoot().findLayer(layer.id()).itemVisibilityChecked():
#         continue
# 
#     if layer.type() != QgsMapLayer.VectorLayer or layer.wkbType() != QgsWkbTypes.MultiPolygon:
#         continue
# 
#     print(layer.name(), layer.featureCount())
#     for feat in layer.getFeatures():
#         geom = feat.geometry()
#         try:
#             nazev = feat['nazev']
#         except KeyError:
#             nazev = 'no name defined'
# 
#         print('{0}: {1} {2:.1f} ha'.format(feat.id(), nazev, geom.area() / 1e4))
# print("_" * 80)

# zmrzliny (? nefunguje, spatna definice promenne url)
# filename = r'c:\users\skoleni-01\desktop\ice_cream.csv'
# uri = 'file:///{}?delimiter=,&xField=lon&yFiled=lat'.format(filename)

# name = os.path.splitext(os.path.basename(filename))[0]
# layer = QgsVectorLayer(uri, name, 'delimitedtext')

#  QgsProject.instance().addMapLayer(layer)

######
# editace dat
shp_file = "/tmp/ice_cream.shp"
layer = QgsVectorLayer(shp_file, "test", "ogr")

QgsProject.instance().addMapLayer(layer)

x = 14.3881100
y = 50.1041200
geom = QgsGeometry.fromPointXY(QgsPointXY(x, y))

p_crs = QgsCoordinateReferenceSystem("EPSG:4326")
trans = QgsCoordinateTransform(
    p_crs, layer.crs(), QgsProject.instance())
geom.transform(trans)

p = geom.asPoint()
offset = 1500
p1 = QgsPointXY(p.x() - offset, p.y() - offset)
p2 = QgsPointXY(p.x() + offset, p.y() + offset)
aoi = QgsRectangle(p1, p2)

layer.selectByRect(aoi)
print (len(layer.selectedFeatures()))

layer.invertSelection()

# primo macka tlacitka
iface.actionToggleEditing().trigger()
iface.actionDeleteSelected().trigger()
iface.actionToggleEditing().trigger()
# mackani jde nahradit timto
# layer.startEditing()
# layer.deleteSelectedFeatures()
# layer.commitChanges()