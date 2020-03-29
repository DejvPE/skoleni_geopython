#!/usr/bin/env python3

# import grass.script as gscript // zastarala knihovna
import sys
from grass.pygrass.modules import Module


def main():
    #gscript.run_command('g.region', raster='dmt', flags='p')
    #gscript.run_command('r.univar', map='dmt')
    Module('g.region', raster='dmt', flags="p")
    print("-" * 60, "\n")
    Module("g.message", message="=" * 60)
    Module("r.univar", map="dmt")


if __name__ == '__main__':
    main()
