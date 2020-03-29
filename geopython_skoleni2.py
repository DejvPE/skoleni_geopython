# ukol - otevrit dalnice a chko, prevest na stejny crs, udelat buffer a prunik
import os
import fiona
import json
from shapely.geometry import mapping, shape
from fiona.transform import transform_geom
from shapely.ops import cascaded_union
from shapely.geometry import MultiPolygon
from shapely import speedups


speedups.enable()

cesta = r"C:\Users\Skoleni-01\Desktop\data"

with fiona.open(os.path.join(cesta, "chko.shp"), "r") as pas:
    with fiona.open(os.path.join(cesta, "highways.geojson"), "r") as hws:
        # kontrola souradnicovych systemu
        print(pas.crs)
        print(hws.crs)

        # Nastaveni crs
        # wgs84 = "epsg:4326"
        # toto jtsk nefunguje
        # jtsk = {"init": "epsg:5514", "towgs84": "570.8,85.7,462.8,4.998,1.587,5.261,3.56"}

        # select jen dalnice d8
        d8 = list(filter(lambda hw: hw["properties"]["ref"] == "D8", hws))
        print("dalnic je: " + str(len(d8)))
        buffered_highways = []  # nutne pro plneni geometrii

        # pro buffer je nutno projit cyklem vsechny prvky a obuffrovat je 
        for hw in d8:
            # transformuji
            # geom_transformed = transform_geom(wgs84, jtsk, hw["geometry"])
            # prevadim na shape
            g = shape(hw["geometry"])
            # vytvarim buffer a pripojuji
            buffered_highways.append(g.buffer(0.0001))  # buffer ve stupnich
        print("dalnic s bufferem je: " + str(len(buffered_highways)))

        # prochazim cyklem chko a zjistuji intersect s dalnici
        # intersect se preskakuje, nelze provest transformaci z neznameho duvodu
        # intersections = []  # nutne pro plneni geometrii
        # for chko in pas:
        #     chko_geom = shape(chko["geometry"])
        #     for hw in buffered_highways:
        #         if chko_geom.intersects(hw):
        #             print("intersection")
        #             out_geom = hw.intersection(chko_geom)
        #             intersections.append(out_geom)
        # print(intersections)
        schema = {
                'properties': {
                        'highway': 'str'
                },
                'geometry': 'MultiPolygon'
        }  # predpis vzstupniho souboru

        with fiona.open(os.path.join(cesta, "chko_x_highway.gpkg"),
                        "w", driver="GPKG", schema=schema) as out:
            # vytvorim novy object
            for g in buffered_highways:
                feature = {
                    'type': 'Feature',
                    'properties': {
                        'highway': 'D8'
                    },
                    'geometry': mapping(MultiPolygon([g]))  # prevod na multipoly, poly nedovoli zapsat kvuli schematu
                }
                out.write(feature)



