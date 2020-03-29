# nacitani dat pomoci webovych sluzeb OGC
import owslib
from owslib.csw import CatalogueServiceWeb as WCS
from owslib.wms import WebMapService as WMS
from owslib.fes import PropertyIsEqualTo, BBox, PropertyIsLike

# vumop = WCS("https://metadata.vumop.cz/csw?service=CSW&request=GetCapabilities")
# vumop.getrecords2()
# print(vumop.results)

cenia = WCS("http://geoportal.gov.cz/php/micka/csw/index.php")
cenia.getrecords2()
print(cenia.results)

for rec in cenia.records:
    print(cenia.records[rec].title)
print("_" * 45)

# filtrovani seznamu
from owslib.fes import PropertyIsLike, BBox, And, PropertyIsEqualTo
wms_query = PropertyIsEqualTo('csw:AnyText', 'WMS')
praha_query = BBox([14.22, 49.94, 14.71, 50.18])
praha_and_wms = And([praha_query, wms_query])
cenia.getrecords2([praha_and_wms], esn='full')
print(cenia.results)
print("_" * 45)

for recid in cenia.records:
    record = cenia.records[recid]
    print(u'{}: {} {} {} {}'.format(record.title, record.bbox.minx, record.bbox.miny,
                                    record.bbox.maxx, record.bbox.maxy))
print("_" * 45)

zm_query = PropertyIsEqualTo('csw:AnyText', '%ZM10%')
cenia.getrecords2([zm_query], esn='full')
zm10 = cenia.records['CZ-CUZK-WMS-ZM10-P']
print(zm10.type)
print(zm10.type.title)
print(u'{}\n{}'.format(zm10.title, zm10.abstract))
url = zm10.references[0]['url']
print("_" * 45)

# Pripojeni k WMS
wms = WMS(url, version="1.3.0")
print(wms.items())

# Stahovani dat
img = wms.getmap(
    layers=["GR_ZM10"],
    size=[800, 600],
    srs="EPSG:5514",
    bbox=[-950003, -1250003, -399990, -899996],
    format="image/png")

with open('data/wms_download.png', 'wb') as out:
    out.write(img.read())
# ev. pridat txt soubor s georeferenci







print("_" * 20, "end", "_" * 20)