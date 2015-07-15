import time
import tests.MockHSC as MockHSC
import HSCSystem
from instrument import Instrument
from daq.PID import PID
from daq.SETled import SETled
import daq.HSCDaq
import matplotlib.pyplot as plt
from serial import Serial
from config.HSCConfig import HSCConfig
from flow.pump.Pump import HarvardUltraPump
import logging
from config import hscConfig
from log.HSCLogger import HSCLogger
logging.setLoggerClass(HSCLogger)
log = logging.getLogger('hsc')
log.configure(hscConfig.Logging)
log.info(str(time.time()) + ":" + time.asctime() + "starting up.")
import pdb

class PIDTest(object):
    
    def __init__(self):    

        self.mockHSC = MockHSC.MockHSC()
        self.hsc = self.mockHSC.hsc
        self.mockHSC.realDaq()
        self.daq = self.hsc.daq
        self.mockHSC.realFlow()
        self.ultraPump = self.hsc.flow.formulationPump
        self.pid = daq.PID.PID()
        self.dv = self.daq.dataProc
        self.daq.configureAcquisition(300,50)
        self.daq.startCapture()
        self.inAuto = True 
    
    def formulationPumpStop(self):
        self.ultraPump.stop()

    def startCapture(self):
        self.daq.startCapture()

    def stopCapture(self):
        self.daq.stopCapture()

    
    def timeSinceStart(self):
        return time.time() - self.startCaptureTime

    def setVoltage(self, voltage):
        self.hsc.daq.channels[0].ledPost.setVoltage(voltage)
        return voltage

    def getVoltage(self):
        curVoltage = self.dv.voltageData[0][-1]
        return curVoltage
    
    #Add channel id number variable to getPressure() method
    def getPressure(self,i):
        #pdb.set_trace()
        self.daq.updateBoard()
        voltageData = self.dv.voltageData[i]
        if voltageData:
            curPressure = self.dv.voltageData[i][-1]
        else:
            curPressure = False
        return curPressure

    def setRateAndInfuse(self,rate, time=0.02):
        self.ultraPump.setDispenseVolume(rate, time)

    def pidPlot(self, Kp, Ki, Kd, setPoint, max, min, sleep, l, isTest, offValue, feedbackFunction, actuationFunction):
        count = 0
        pid = self.pid
        self.daq.updateBoard()
        pid.setLastInput(feedbackFunction) 
        pid.setPID(Kp, Ki, Kd, max, min, setPoint,sleep=0.02)
        pid.setMode("auto", offValue, feedbackFunction)         #"Manual"

        for i in xrange(1,400):
            count = count + 1
            time.sleep(sleep)
            if isTest:
                self.daq.updateBoard()
                outv = pid.pidCompute(setPoint,offValue, feedbackFunction, actuationFunction)        
        self.ultraPump.stop()

    def testPumpPressurePID(self):

        AUTOMATIC = 1
        MANUAL = 0
        Kp = 300.00
        Ki = 1000.00
        Kd = 10
        setPoint = 0.50     
        max = 200
        min = 0
        sleep = 0.02
        l = 100
        isTest = True
        offValue = 40

        self.pidPlot(Kp, Ki, Kd, setPoint, max, min, sleep, l, isTest, offValue, self.getPressure, self.setRateAndInfuse)

if __name__=='__main__':
    p = PIDTest()
    p.testPumpPressurePID()
































