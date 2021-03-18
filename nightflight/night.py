#!/usr/bin/python3

import math
import datetime

import astral
import astral.sun

from nightflight.airport_nvecs import airfields


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
        #astral gives sunset on the day, and previous sunrise, so adjust if reqd
        if sunrise.date() != dt.date():
            sunrise = astral.sun.sunrise(
                l.observer,
                (dt + datetime.timedelta(days=1)).date())
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
        #and for summer in southern hemisphere southern...
        if nvec[2] < 0 and dt.month in (10, 11, 12 , 1, 2):
            return False
    return True


def night_duration(_from, _to, _start, _end, seclength=32):
    flight_duration = (_end - _start).total_seconds() / 60
    if(flight_duration <= 0): raise ValueError((_start, _end))
    min_sections = flight_duration / seclength
    depth = max(math.ceil(math.log(min_sections) / math.log(2)) - 1, 0)
    nvecs = recursive_bisect(_from, _to, depth)
    time_d = (_end - _start) / (len(nvecs) - 1)
    time_d_mins = time_d.total_seconds() / 60
    time = _start
    last_nvec = nvecs[0]
    last_nstatus = night_p(last_nvec, time)
    night_acc = 0.0
    for nvec in nvecs[1:]:
        time += time_d
        nstatus = night_p(nvec, time)
        if nstatus != last_nstatus:#day to night or night to day
            if seclength > 2:
                night_acc += night_duration(last_nvec, nvec, time - time_d, time, 2)
            else:
                night_acc += time_d_mins / 2
        elif nstatus:#night at current nvec
            night_acc += time_d_mins
        last_nstatus = nstatus
        last_nvec = nvec
    return night_acc
