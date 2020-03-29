# Školení GeoPython 27.2.2020

https://training.gismentors.eu/geopython-zacatecnik/python/index.html
https://training.gismentors.eu/geopython-zacatecnik/uvod.html

Nastaveni prostredi v OSGeo4W Shell

> py3_env

Editor VIM?

Virtual env - kontejner, kde se baliky instaluji nesystemove
```
python3 -m venv program_venv
Running virtualenv with interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in program_venv/bin/python3
Also creating executable in program_venv/bin/python
Installing setuptools, pip...done.
```

Vykresleni geometrie pomoci Python
https://deparkes.co.uk/2015/03/11/how-to-plot-polygons-in-python/

Zasuvny modul QuickMapServices (obsahuje i mapy.cz)

Rastrovy modul rasterio
https://training.gismentors.eu/geopython-zacatecnik/rastrova_data/rasterio/ndvi.html

Zjistit jak jsou ulozena data v rastru:

`C:\>gdalinfo c:\Users\Skoleni-01\Desktop\data\B03-2018-05-06.tiff`

> Corner Coordinates:
> Upper Left  (  14.5139694,  48.8665215) ( 14d30'50.29"E, 48d51'59.48"N)
> Lower Left  (  14.5139694,  48.6633034) ( 14d30'50.29"E, 48d39'47.89"N)
> Upper Right (  15.0739288,  48.8665215) ( 15d 4'26.14"E, 48d51'59.48"N)
> Lower Right (  15.0739288,  48.6633034) ( 15d 4'26.14"E, 48d39'47.89"N)
> Center      (  14.7939491,  48.7649125) ( 14d47'38.22"E, 48d45'53.68"N)
> <b>Band 1 Block=3117x8 Type=UInt16, ColorInterp=Gray</b>


Převzorkovat data, aby se lepe nacitali bloky:

`gdalwarp -r mode -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 data/B04-2018-05-06.tiff outputs/B04-2018-05-06-256block.tiff`

> gdalinfo outputs/B04-2018-05-06-256block.tiff
> ...
> <b>Band 1 Block=256x256 Type=UInt16, ColorInterp=Gray</b>


`TODO: WFS AOPK - diakritika v nazvu vrstev, pada !!!`
https://gis.nature.cz/arcgis/services/UzemniOchrana/Natura2000/MapServer/WFSServer?service=WFS&request=GetCapabilities&version=1.1.0

_____________________________________________________________________________________________________________
# Školení GeoPython 10.3.2020 - Pluginy do QGISu
```
iface.actionToggleEditing().trigger()
iface.actionDeleteSelected().trigger()
iface.actionToggleEditing().trigger()

Compare with

layer.startEditing()
layer.deleteSelectedFeatures()
layer.commitChanges()
```
.trigger() doopravdy zmáčkne tlačítko - vyskočí potvrzovací okénko k potvrzením editace


Instalace Plugin Builder 3
Instalace Plugin Reloader (při aktualizaci pluginu)

Pomocí Plugin Builder 3 vytvoříme plugin Save view (tool button with docked view)

Je nutné nainstalovat pb_tools. Pomocí toho zkompilujeme plugin.
- spustím OSGeo4W Shell
- spustím: py3_env.bat
- spustím: qt5_env.bat
- nyní již funguje pyrcc5
- spustím: pip install pb_tools
- spustím: cd c:\cesta\k\pluginu
- spustím: pb_tool --help 
- spustím: pb_tool help 
- spustím: pb_tool compile

Defultní složka s QGIS pluginy
C:\Users\Skoleni-01\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins

Nutno přidat do QGISu proměnnou prostředí
QGIS - Nastavení - Systém - Prostředí - Add
- přidám QGIS_PLUGINPATH a cestu k nadřazené složce s pluginy
- v seznamu pluginů bych měl nyní plugin vidět

Upravit UI v Qt Designer
- otevru soubor ve slozce s pluginem - dockwidget_base.ui
- pridam widget Label - Vyber vektorove vrstvy
- pridam widget QgsMapLayerComboBox
- pridam widget Label - Ulozit do
- pridam widget QgsFile
- pridam widget OK Button

Vracím se do QGISu
- pomocí pluginu Plugin Reloader reloadnu plugin SaveView
- vidím s novým UI
- otevru skript save_view.py
- v definovane funkci "run" edituji
- pridam filtr jen na vektorove vrstvy ke combo boxu
- musim pridat importy
- reload modelu v QGISu, mel bych v kombo boxu videt jen vektory
- nastavim ukladani do slozky, ne soubor
- nastavim akci pri stisknuti tlacitka
- musim definovat vlastni funkci, ktera se spusti pri kliku a ulozi 
 


Dokumentace QGIS API: https://qgis.org/pyqgis/3.0/index.html

PyQGIS Cookbook: https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html


## GRASS a Python (odpoledne)

Data: https://training.gismentors.eu/geodata/eu-dem/ (DMT50m)
https://training.gismentors.eu/grass-gis-zacatecnik/
https://training.gismentors.eu/grass-gis-pokrocily/


Spustím GRASS 7.9dev, vytvořím lokaci vumop a spustím mapset PERMANENT
- naimportuji rastr dmt50m
- zkusim pustit g.region (nastavi region)
- spustim r.univar (statistika rastru)
- otevru python editor (ikona pythona)
```
def main():
    gscript.run_command('g.region', raster='dmt', flags='p')
    gscript.run_command('r.univar', map='dmt')
```
GRASS ma dve knihovny do Pythona!!!
- grass.script: vola existujici nastroje GRASSu
- grass.pygrass:
- umi toho vic, vznikla pozdeji, nenahrazuje script
- je vic pythonisticka, pracuje s objekty
- script vicemene jen vola existujici funkce
- pristupuje primo k datum: rastr jako pajtni objekt

Spuštění skriptu přes cmd nebo shell
- musim pustit py3_env.bat
- grass78 - spousti grass
- grass78 --exec python3 C:\cesta\ke\skriptu\rastr_stats.py C:\cesta\k\datum (grass data)
- grass78 --help
- grass78 --text --exec python3 C:\cesta\ke\skriptu\rastr_stats.py C:\cesta\k\datum (grass data)

Skript v GRASSu na vypocet NDVI
- pozor na nasteveni regionu podle vektorove vrstvy - nesedi snap na rastrova data
- lze vyresit, kliknu pravym mysitkem na rastr a dam align region to raster

## Python - přechod na f string parametry
- misto
`expression="{o} = float({n} - {v}) / ({n} + {v})".format(o=ndvi, v=vis, n=nir)`
- je
`expression=f"{ndvi} = float({nir} - {vis}) / ({nir} + {vis})"`

