#!/usr/bin/python3

"""Utility script to process airports.csv file

This file is found at:

  https://ourairports.com/data/

"""

import sys
import math
import csv
import re

#fields
F_LAT = 4
F_LONG = 5
F_ICAO = 1
F_IATA = 13


def to_nvec(lat, long):
    lat *= math.pi / 180
    long *= math.pi /180
    x = math.cos(lat) * math.cos(long)
    y = math.cos(lat) * math.sin(long)
    z = math.sin(lat)
    return (x, y, z)


def main():
    lines = csv.reader(sys.stdin)
    headers = next(lines)
    re_ICAO = re.compile(r"[A-Za-z]{4}")
    re_IATA = re.compile(r"[A-Za-z]{3}")
    for f in lines:
        lat = float(f[F_LAT])
        long = float(f[F_LONG])
        icao, iata = "", ""
        if re_ICAO.match(f[F_ICAO]):
            icao = f[F_ICAO].upper()
        if re_IATA.match(f[F_IATA]):
            iata = f[F_IATA].upper()
        nvec = [f"{round(X * 10000)}" for X in to_nvec(lat, long)]
        if icao or iata:
            print(f"{icao},{iata},{','.join(nvec)}")


if __name__ == "__main__": main()
