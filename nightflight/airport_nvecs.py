import importlib.resources
import bz2

resources = importlib.resources.files("nightflight")
airport_data_bz2 = resources.joinpath("airports.txt.bz2").read_bytes()
airport_data = bz2.decompress(airport_data_bz2).decode()
airfields = {}
for airport in airport_data.splitlines():
    fields = airport.split(",")
    nvec = tuple(int(X) / 10000 for X in fields[2:])
    airfields[fields[0]] = nvec
    airfields[fields[1]] = nvec
