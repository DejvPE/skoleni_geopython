#!/usr/bin/env python3   - jen pro linux
import os
import sys

os.environ["GISBASE"] = r"C:\OSGeo4W64\apps\grass\grass78"  # nastavit cestu k souborum grassu
sys.path.insert(0, os.path.join(os.environ['GISBASE'], 'etc', 'python'))  # prida cestu k windows path
import grass.script.setup as gsetup  # naimportuje grass knihovnu // zastarala knihovna
from grass.pygrass.modules import Module  # naimportuje grass knihovnu // novejsi a lepsi knihovna

gsetup.init(os.environ['GISBASE'], r'C:\Users\Skoleni-01\Desktop\skoleni_grass\grass_data', 'vumop', 'PERMANENT')
# gsetup init inicializuje sezeni grassu: cesta k souborum grass, cesta ke grass data, lokace, mapset


def main():
    # gscript.run_command('g.region', raster='dmt', flags='p')  # zastarala knihovna
    # gscript.run_command('r.univar', map='dmt')  # zastarala knihovna
    Module('g.region', raster='dmt', flags="p")
    print("-" * 60, "\n")
    Module("g.message", message="=" * 60)
    Module("r.univar", map="dmt")


if __name__ == '__main__':
    main()
