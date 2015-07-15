import unittest
from serial import Serial
from flow.valve.Valve import ValcoValve
from flow.valve.Valve import Valve
from config import hscConfig
from log import hscLog as log
import tests.MockHSC as MockHSC

import time
import sys
import pdb

#TODO: Switch from individual valve TestCases to a TestCase generator

class Valve_Formulation_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mockHSC = MockHSC.MockHSC()
        cls.hsc = cls.mockHSC.hsc
        cls.mockHSC.realFlow()
        cls.vcValve = cls.hsc.flow.formulationValve
        valveConf = hscConfig.FormulationValve
        cls.flowDict = {k:valveConf[k] for k in ('Reservoir','System')}

    @classmethod
    def tearDownClass(cls):
        #cls.comLink.close()
        cls.hsc.flow.shutdown()

    def test_01_setPosition(self):
        #Test of the valve position B
        res = self.vcValve.zz_setPosition('b')
        self.assertEqual("b", res)

    def test_02_setPosition(self):
        #Test of the valve position A
        res = self.vcValve.zz_setPosition('a')
        self.assertEqual("a", res)

    def test_03_setFlow(self):
        #Test the flow System position
        res = self.vcValve.zz_setFlow('System')
        expected = self.flowDict['System']
        self.assertEqual(expected, res)

    def test_04_setFlow(self):
        #Test the flow Reservoir position
        res = self.vcValve.zz_setFlow('Reservoir')
        expected = self.flowDict['Reservoir']
        self.assertEqual(expected, res)

class Valve_InjectionValve_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mockHSC = MockHSC.MockHSC()
        cls.hsc = cls.mockHSC.hsc
        cls.mockHSC.realFlow()
        cls.vcValve = cls.hsc.flow.injectionValve
        valveConf = hscConfig.InjectionValve
        cls.flowDict = {k:valveConf[k] for k in ('Inject','Flow')}

    @classmethod
    def tearDownClass(cls):
        #cls.comLink.close()
        cls.hsc.flow.shutdown()

    def test_01_setPosition(self):
        #Test of the valve position B
        res = self.vcValve.zz_setPosition('b')
        self.assertEqual("b", res)

    def test_02_setPosition(self):
        #Test of the valve position A
        res = self.vcValve.zz_setPosition('a')
        self.assertEqual("a", res)

    def test_03_setFlow(self):
        #Test the flow Flow position
        res = self.vcValve.zz_setFlow('Flow')
        expected = self.flowDict['Flow']
        self.assertEqual(expected, res)

    def test_04_setFlow(self):
        #Test the flow inject position
        res = self.vcValve.zz_setFlow('Inject')
        expected = self.flowDict['Inject']
        self.assertEqual(expected, res)


class Valve_Bypass1Valve_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mockHSC = MockHSC.MockHSC()
        cls.hsc = cls.mockHSC.hsc
        cls.mockHSC.realFlow()
        cls.vcValve = cls.hsc.flow.bypassValves[0]
        valveConf = hscConfig.BypassValves[0]
        cls.flowDict = {k:valveConf[k] for k in ('Bypass','Column')}
        
    @classmethod
    def tearDownClass(cls):
        #cls.comLink.close()
        cls.hsc.flow.shutdown()

    def test_01_setPosition(self):
        #Test of the valve position B
        res = self.vcValve.zz_setPosition('b')
        self.assertEqual("b", res)

    def test_02_setPosition(self):
        #Test of the valve position A
        res = self.vcValve.zz_setPosition('a')
        self.assertEqual("a", res)

    def test_03_setFlow(self):
        #Test the flow Bypass position
        res = self.vcValve.zz_setFlow('Bypass')
        expected = self.flowDict['Bypass']
        self.assertEqual(expected, res)

    def test_04_setFlow(self):
        #Test the flow column position
        res = self.vcValve.zz_setFlow('Column')
        expected = self.flowDict['Column']
        self.assertEqual(expected, res)

class Valve_Bypass2Valve_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        cls.mockHSC = MockHSC.MockHSC()
        cls.hsc = cls.mockHSC.hsc
        cls.mockHSC.realFlow()
        cls.vcValve = cls.hsc.flow.bypassValves[1]
        valveConf = hscConfig.BypassValves[1]
        cls.flowDict = {k:valveConf[k] for k in ('Bypass','Column')}

    @classmethod
    def tearDownClass(cls):
        #cls.comLink.close()
        cls.hsc.flow.shutdown()

    def test_01_setPosition(self):
        #Test of the valve position B
        res = self.vcValve.zz_setPosition('b')
        self.assertEqual("b", res)

    def test_02_setPosition(self):
        #Test of the valve position A
        res = self.vcValve.zz_setPosition('a')
        self.assertEqual("a", res)

    def test_03_setFlow(self):
        #Test the flow Bypass position
        res = self.vcValve.zz_setFlow('Bypass')
        expected = self.flowDict['Bypass']
        self.assertEqual(expected, res)

    def test_04_setFlow(self):
        #Test the flow Column position
        res = self.vcValve.zz_setFlow('Column')
        expected = self.flowDict['Column']
        self.assertEqual(expected, res)

def main():
    unittest.main(argv = sys.argv)

if __name__ == "__main__":
    main()
