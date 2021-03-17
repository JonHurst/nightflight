#!/usr/bin/python3

import math
import datetime

import astral
import astral.sun

from airport_nvecs import airfields

def recursive_bisect(nvec1, nvec2, depth):
    assert(depth >= 0)
    added = [nvec1[N] + nvec2[N] for N in range(3)]
    mag = math.sqrt(sum([X**2 for X in added]))
    if mag == 0: #nvec1 and nvec2 on exact opposite sides of earth
        if nvec1[0] or nvec1[1]:
            #not poles: use bisector in equitorial plane
            nvec_bisector = (nvec1[1], -nvec1[0], 0)
        else:
            #poles: use a suitable equitorial nvec
            nvec_bisector = (1, 0, 0)
    else:
        nvec_bisector = tuple([X / mag for X in added])
    if(depth > 0):
        a = recursive_bisect(nvec1, nvec_bisector, depth - 1)
        b = recursive_bisect(nvec_bisector, nvec2, depth - 1)
        return a + b[1:]
    else:
        return [nvec1, nvec_bisector, nvec2]


def to_latlong(nvec):
    lat = math.atan2(nvec[2], math.sqrt(nvec[0]**2 + nvec[1]**2))
    long = math.atan2(nvec[1], nvec[0])
    lat *= 180 / math.pi
    long *= 180 / math.pi
    return (lat, long)


def night_p(nvec, dt):
    l = astral.LocationInfo("", "", "UTC", *to_latlong(nvec))
    try:
        sunrise, sunset = astral.sun.daylight(l.observer, dt.date())
        #replace with timezone naive versions
        sunrise = sunrise.replace(tzinfo=None)
        sunset = sunset.replace(tzinfo=None);
        if(sunset > sunrise): #..dark..sr..light..ss..dark
            if (dt >= sunrise - datetime.timedelta(minutes=30) and
                dt <= sunset + datetime.timedelta(minutes=30)):
                return False
        else: #..light..ss..dark..sr..light
            if(dt <= sunset + datetime.timedelta(minutes=30) or
               dt >= sunrise - datetime.timedelta(minutes=30)):
                return False
    except ValueError as e: #daylight raises value error if no sunrise/sunset
        #summer in northern hemisphere, assume midday sun
        if nvec[2] > 0 and dt.month >=4 and dt.month <=8:
            return False
        #and for summer in southern hemisphere southern hemisphere...
        if nvec[2] < 0 and dt.month in (10, 11, 12 , 1, 2):
            return False
    return True


def night_duration(_from, _to, _start, _end, seclength=10):
    flight_duration = (_end - _start).total_seconds() / 60
    min_sections = flight_duration / seclength
    depth = math.ceil(math.log(min_sections) / math.log(2)) - 1
    nvecs = recursive_bisect(_from, _to, depth)
    time_d = (_end - _start) / (len(nvecs) - 1)
    time = _start
    last_nstatus = night_p(nvecs[0], time)
    night_acc = 0.0
    for nvec in nvecs[1:]:
        time += time_d
        nstatus = night_p(nvec, time)
        if nstatus:
            if last_nstatus:
                night_acc += time_d.total_seconds() / 60
            else: # day to night
                night_acc += time_d.total_seconds() / 120
        else: #night to day
            if last_nstatus:
                night_acc += time_d.total_seconds() / 120
        last_nstatus = nstatus
    return round(night_acc)


def test():
    _from = airfields["BSL"]
    _to = airfields["BRS"]
    _start = datetime.datetime(202, 12, 20, 15, 31)
    _end = _start + datetime.timedelta(minutes=116)
    for c in range(1000):
        duration = night_duration(_from, _to, _start, _end)
    print(duration)

if __name__ == "__main__":
    test()
