#!/usr/bin/python3

"""Utility script to process airports.dat file

This file is found at:

  https://openflights.org/data.html

Pipe it to stdin, get a python file defining airfields dictionary, keyed with
IATA designator giving nvec (ordered triple) on stdout.

"""

import sys
import math
import csv

#fields
F_IATA = 4
F_LAT = 6
F_LONG = 7


def to_nvec(lat, long):
    lat *= math.pi / 180
    long *= math.pi /180
    x = math.cos(lat) * math.cos(long)
    y = math.cos(lat) * math.sin(long)
    z = math.sin(lat)
    return (x, y, z)


def main():
    airfields = {}
    #read file from stdin
    for f in csv.reader(sys.stdin):
        lat = float(f[F_LAT])
        long = float(f[F_LONG])
        airfields[f[F_IATA]] = to_nvec(lat, long)
    #add missing airfields
    airfields["BER"] = to_nvec(52.36667, 13.50333)
    #output date to stdout
    print("airfields = {")
    print(",\n".join([f"'{i}': {airfields[i]}".replace("\\", "\\\\")
                      for i in sorted(airfields)]))
    print("}")

if __name__ == "__main__": main()
