#!/usr/bin/python3

import unittest
import math
import datetime

import night
from airport_nvecs import airfields

class Test_nvecs(unittest.TestCase):

    def test_polar(self):
        nvecs = night.recursive_bisect((0, 0, 1), (0, 0, -1), 1)
        a = 1 / math.sqrt(2)
        #assumed pole to pole routing goes through Greenwich
        expected = ((0, 0, 1),
                    (a, 0, a),
                    (1, 0, 0),
                    (a, 0, -a),
                    (0, 0, -1))
        for c in range(len(nvecs)):
            self.assertTupleEqual(nvecs[c], expected[c])


    def test_equitorial(self):
        nvecs = night.recursive_bisect((1, 0, 0), (-1, 0, 0), 1)
        #assumed equitorial routing goes west
        a = 1 / math.sqrt(2)
        expected = ((1, 0, 0),
                    (a, -a, 0),
                    (0, -1, 0),
                    (-a, -a, 0),
                    (-1, 0, 0))
        for c in range(len(nvecs)):
            self.assertTupleEqual(nvecs[c], expected[c])


    def test_general(self):
        nvecs = night.recursive_bisect((airfields["BRS"]), airfields["FNC"], 2)
        #print(",\n".join([str(X) for X in nvecs]))
        #checked by plotting
        expected = (
            (0.623412838407546, -0.02960757915593101, 0.781332083153618),
            (0.6515088582562976, -0.05710789453359362, 0.7564885299827854),
            (0.6781957583848142, -0.08448469376968946, 0.730008801198649),
            (0.7034158188760655, -0.11167876479489419, 0.701950168636493),
            (0.7271144923756552, -0.13863129075465633, 0.6723733190728134),
            (0.7492405220698828, -0.1652839772215728, 0.6413422229685708),
            (0.7697460525468421, -0.19157917827783016, 0.6089239961103075),
            (0.7885867333007757, -0.2174600211950129, 0.5751887544483776),
            (0.8057218146558248, -0.24287052944161466, 0.5402094624462576))
        for c in range(len(nvecs)):
            self.assertTupleEqual(nvecs[c], expected[c])


class Test_night_predicate(unittest.TestCase):

    def test_north_pole_midwinter(self):
        self.assertTrue(night.night_p((0, 0, 1), datetime.datetime(2021, 12, 21)))


    def test_north_pole_midsummer(self):
        self.assertFalse(night.night_p((0, 0, 1), datetime.datetime(2021, 6, 21)))


    def test_south_pole_midwinter(self):
        self.assertTrue(night.night_p((0, 0, -1), datetime.datetime(2021, 6, 21)))


    def test_south_pole_midsummer(self):
        self.assertFalse(night.night_p((0, 0, -1), datetime.datetime(2021, 12, 21)))


    def test_bristol(self):
        #sunrise/sunset from BBC Weather app
        self.assertFalse(
            night.night_p(airfields["BRS"], datetime.datetime(2021, 3, 18, 8, 40)))
        self.assertTrue(
            night.night_p(airfields["BRS"], datetime.datetime(2021, 3, 18, 5, 48)))
        self.assertFalse(
            night.night_p(airfields["BRS"], datetime.datetime(2021, 3, 18, 5, 50)))
        self.assertFalse(
            night.night_p(airfields["BRS"], datetime.datetime(2021, 3, 18, 18, 49)))
        self.assertTrue(
            night.night_p(airfields["BRS"], datetime.datetime(2021, 3, 18, 18, 51)))


    def test_kittila(self):
        #sunrise/sunset from timeanddate.com
        self.assertTrue(
            night.night_p(airfields["KTT"], datetime.datetime(2021, 12, 1, 8, 18)))
        self.assertFalse(
            night.night_p(airfields["KTT"], datetime.datetime(2021, 12, 1, 8, 20)))
        self.assertFalse(
            night.night_p(airfields["KTT"], datetime.datetime(2021, 12, 1, 11, 58)))
        self.assertTrue(
            night.night_p(airfields["KTT"], datetime.datetime(2021, 12, 1, 12, 0)))
        #local noon on 14th December -- no sunrise/sunset
        self.assertTrue(
            night.night_p(airfields["KTT"], datetime.datetime(2021, 12, 14, 10, 15)))


    def test_melbourne(self):
        self.assertTrue(
            night.night_p(airfields["MEL"], datetime.datetime(2021, 3, 17, 19, 50)))
        self.assertFalse(
            night.night_p(airfields["MEL"], datetime.datetime(2021, 3, 17, 19, 52)))
        self.assertFalse(
            night.night_p(airfields["MEL"], datetime.datetime(2021, 3, 18, 9, 4)))
        self.assertTrue(
            night.night_p(airfields["MEL"], datetime.datetime(2021, 3, 18, 9, 6)))
