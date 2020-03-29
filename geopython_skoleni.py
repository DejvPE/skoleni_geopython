import os
import fiona
from shapely.geometry import shape
from shapely.geometry import mapping
import json

# import shapely
# print(shapely.__file__)


cesta_data = r"C:\Users\Skoleni-01\Desktop\data"

with fiona.open(os.path.join(cesta_data, "chko.shp"), 'r', encoding='utf-8') as chko:
    # print(dir(chko))  # vycet moznych funkci
    # print(help(chko))  # dokumentace k objektu
    # print(chko)
    # print(chko.driver)  # vrati typ objektu (shp)
    # print(chko.crs)
    # print(chko.meta)
    # print(chko.bounds)
    # print(chko.schema)
    # print(chko.schema["geometry"])
    # print(json.dumps(chko.meta, sort_keys=True, indent=4, separators=(',', ': ')))
    # print(len(chko))  # Vrati pocet prvku
    # for prvek in chko:
    #     print(prvek["properties"]["NAZEV"])  # projde vsechny prvky
    # print(chko[10])  # Vrati kontkretni prvek
    # pocet = 0
    # for prvek in chko:
    #     if prvek["properties"]["NAZEV"] == "České středohoří":
    #         pocet += 1
    # print(pocet)
    # Knihovna shapely
    cr = chko[54]
    geom = shape(cr["geometry"])
    # print(geom)  # textova reprezentace objektu
    # print(geom.type)  # vypise typ objektu
    # print(dir(geom))  # vypise vsechny funkce a atributy geometrie
    # print(geom.area)

    # print("centroid: ", mapping(geom.centroid))  # vrati hodnotu centroidu jako bod, mapping prevadi do json
    # print("obvod: ", geom.exterior.length)

    with open(os.path.join(cesta_data, "bod_centroid.geojson", "w")) as out:  # uloyi geojson
        data = {
            "type":"FeatureCollection",
            "features": [
                {
                    "type":"feature",
                    "geometry": mapping(geom.exterior)
                }
            ]
        }


print("____end_____")
print("_" * 60)
