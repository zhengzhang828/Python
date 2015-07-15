#!/usr/bin/env python

import unittest
from flow.pump.Pump import HarvardUltraPump
import sys
from serial import Serial
import time
from config import hscConfig
import pdb
import profile
from log import hscLog as log
import tests.MockHSC as MockHSC
import time
class Pump_FormulationPump_TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mockHSC = MockHSC.MockHSC()
        cls.hsc = cls.mockHSC.hsc
        cls.mockHSC.realFlow()
        cls.ultraPump = cls.hsc.flow.formulationPump
        conf = hscConfig
        cls.diameter = conf.FormulationPump['syringe_diameter']

    @classmethod
    def tearDownClass(cls):
        cls.ultraPump.setSyringeDiameter(cls.diameter)
        cls.ultraPump.clearInfusedVolume()
        cls.ultraPump.clearWithdrawnVolume()
        cls.hsc.flow.stop()
        cls.hsc.flow.shutdown()

    def test_01_commandMode(self):
        #Test the set Command Mode
        self.ultraPump.setCommandMode('44')
        res = self.ultraPump.getCommandMode()
        self.assertEqual('44', res)
        self.ultraPump.setCommandMode('ultra')
        res = self.ultraPump.getCommandMode()
        self.assertEqual('ultra', res)

    def test_02_pollingModeOff(self):
        self.ultraPump.setPollingMode('off')
        res = self.ultraPump.getPollingMode()
        self.assertEqual('off', res)
    
    def test_03_pollingModeOn(self):
        self.ultraPump.setPollingMode('on')
        res = self.ultraPump.getPollingMode()
        self.assertEqual('on', res)

    def test_04_setVolume(self):
        self.ultraPump.setVolume(10)
        res = self.ultraPump.getCurVolume()
        self.assertEqual(10, res)

    def test_05_aspirateVolume(self):
        res = self.ultraPump.aspirateVolume(0.0001, 500)
        self.assertAlmostEqual(res,0.0001,places=5)

    def test_06_dispenseVolume(self):
        res = self.ultraPump.dispenseVolume(0.0001, 500)
        self.assertAlmostEqual(res,0.0001,places=5)

    def test_07_setSyringeDiameter(self):
        self.ultraPump.setSyringeDiameter(3.1415)
        res = self.ultraPump.getSyringeDiameter()
        self.assertAlmostEqual(res,3.1415,places=5)

    def test_08_longAspirateDispense(self):
        for x in xrange(1):
            res = self.ultraPump.aspirateVolume(0.1,1024)
            self.assertAlmostEqual(res, 0.1, places=5)
            res = self.ultraPump.dispenseVolume(0.1,1024)
            self.assertAlmostEqual(res, 0.1, places=5)

class Pump_ProteinPump_TestCase(unittest.TestCase):
    
    @classmethod
    def setUp(cls):
        cls.mockHSC = MockHSC.MockHSC()
        cls.hsc = cls.mockHSC.hsc
        cls.mockHSC.realFlow()
        cls.ultraPump = cls.hsc.flow.proteinPump
        conf = hscConfig
        cls.diameter = conf.ProteinPump['syringe_diameter']

    def tearDown(cls):
        cls.ultraPump.setSyringeDiameter(cls.diameter)
        cls.ultraPump.clearInfusedVolume()
        cls.ultraPump.clearWithdrawnVolume()
        cls.hsc.flow.stop()
        cls.hsc.flow.shutdown()

    def test_08_setCommandMode(self):
        self.ultraPump.setCommandMode('ultra')
        res = self.ultraPump.getCommandMode()
        self.assertEqual('ultra', res)

    def test_09_setPollingModeOff(self):
        self.ultraPump.setPollingMode('off')
        res = self.ultraPump.getPollingMode()
        self.assertEqual('off', res)

    def test_10_setPollingModeOn(self):
        self.ultraPump.setPollingMode('on')
        res = self.ultraPump.getPollingMode()
        self.assertEqual('on', res)

    def test_11_setVolume(self):
        self.ultraPump.setVolume(10)
        res = self.ultraPump.getCurVolume()
        self.assertEqual(10, res)

    def test_12_aspirateVolume(self):
        res = self.ultraPump.aspirateVolume(0.0001, 200)
        self.assertAlmostEqual(res,0.0001,places=5)

    def test_13_dispenseVolume(self):
        res = self.ultraPump.dispenseVolume(0.0001, 200)
	print res
        #The volume is milliliter and the rate is microliter/min 1ml = 1000ul
        self.assertAlmostEqual(res,0.0001,places=5)
        
    def test_14_setSyringeDiameter(self):
        self.ultraPump.setSyringeDiameter(3.1415)
        res = self.ultraPump.getSyringeDiameter()
        self.assertAlmostEqual(res, 3.1415, places=5)
        
def main():
    unittest.main(argv = sys.argv)

if __name__== '__main__':
    main()
