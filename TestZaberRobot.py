import unittest
import robot
import struct
import instrument.Instrument as Instrument

import time
from config import hscConfig
from log import hscLog as log

from tests.MockHSC import MockHSC
import sys

#TODO: Switch from individual valve TestCases to a TestCase generator
class Zaber_Robot_TestCase(unittest.TestCase):    
    @classmethod
    def setUpClass(cls):
    	cls.mockHSC = MockHSC()
	cls.mockHSC.realRobot()
	cls.robot = cls.mockHSC.hsc.robot
	cls.pwSys = cls.robot.robot

    @classmethod    
    def tearDownClass(cls):
    	cls.pwSys.shutdown()

    def test_00_home(self):
        wres = self.pwSys.zz_getWellPosition()
        pres = self.pwSys.zz_getPlatePosition()
        expected = ((1,60,0),(1,60,17100))
        self.assertEqual(expected, (wres, pres))
 
    def test_01_goToPlateWell_P3_W6(self):
        self.pwSys.goToPlateWell(3,6)
        wres = self.pwSys.zz_getWellPosition()
        pres = self.pwSys.zz_getPlatePosition()
        expected = ((1,60,472500), (1,60,54100))
        self.assertEqual(expected, (wres, pres))

    def test_02_goToPlateWell_P1_W1(self):
        self.pwSys.goToPlateWell(1,1)
        wres = self.pwSys.zz_getWellPosition()
        pres = self.pwSys.zz_getPlatePosition()
        expected = ((1,60,0), (1,60,17100))
        self.assertEqual(expected, (wres, pres))

def main():
    unittest.main(argv = sys.argv)

if __name__ == "__main__":
    main()

