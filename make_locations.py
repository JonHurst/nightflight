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
    airfields["SZD"] = to_nvec(53.39417, -1.3886)
    airfields["EGCK"] = to_nvec(53.10167, -4.3375)
    airfields["EGCW"] = to_nvec(52.62944, -3.1525)
    airfields["EGCB"] = to_nvec(53.47167, -2.3897)
    airfields["EGBG"] = to_nvec(52.60778, -1.0319)
    airfields["EGTF"] = to_nvec(51.34806, -0.5586)
    airfields["EGBW"] = to_nvec(52.19222, -1.6144)
    airfields["DOC"] = to_nvec(57.87217, -4.0263)
    airfields["Langford L"] = to_nvec(54.623, -6.3)
    #output date to stdout
    print("airfields = {")
    print(",\n".join([f"'{i}': {airfields[i]}".replace("\\", "\\\\")
                      for i in sorted(airfields)]))
    print("}")

if __name__ == "__main__": main()
