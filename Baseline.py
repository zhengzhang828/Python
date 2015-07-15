import tests.PIDTest as pt
import tests.MockHSC as MockHSC
import daq.HSCDaq as HSCDaq
import numpy as np
import time
import math
import matplotlib.pyplot as plt
import pdb

class Baseline(object):
    channelID = None
    baselinePressure = None
    
    def __init__(self):
        self.pidTest = pt.PIDTest()
        
    def setRate(self, rate):
        self.pidTest.setRateAndInfuse(rate)

    def pumpStop(self):
        self.pidTest.formulationPumpStop()

    def getPressure(self,channelID):
        voltagePressure = self.pidTest.getPressure(channelID)
        psiPressure = 200*voltagePressure
        return psiPressure

    def testBaselinePressureCorrect(self,baselinePressure,channelID):
        self.setRate(0)
        baselinePressureList = []
        for i in xrange(5):
            time.sleep(1)
            pressure = self.getPressure(channelID)
            print "pressure", pressure
            baselinePressureList.append(pressure)
        baselinePressureMean = np.mean(baselinePressureList)
        difference = math.fabs(baselinePressureMean - baselinePressure)
        print"difference",difference
        if difference > 2: 
            self.pumpStop()
            return True
        else:
            return False
    
    def collectChannelPressure(self, maxRate, sleep, rateIncrease, targetPressure, rate,baselinePressure,channelID):
        pressureList = [baselinePressure]
        rateList = [rate]
        percentMaxPressure = 0.0
        currentFlowRate = rate
        target = baselinePressure + targetPressure
        previousPressure = baselinePressure

        while(percentMaxPressure < 0.98):
            time.sleep(1)
            currentPressure = self.getPressure(channelID)
            pressureDifference = currentPressure - previousPressure
            rateList.append(currentFlowRate)
            pressureList.append(currentPressure)
            print "current pressure",currentPressure
            if (pressureDifference < 1):
                currentFlowRate += rateIncrease
                if (currentFlowRate < maxRate):
                    self.setRate(currentFlowRate)
                    print "current rate",currentFlowRate
                else:
                    break
            percentMaxPressure = currentPressure / target
            previousPressure = currentPressure

        if percentMaxPressure>0.98:
            time.sleep(60)
            
        return pressureList,rateList
    
    def plotPressureList(self,pressureList,rateList,baselinePressure):
        y1 = [x-baselinePressure for x in pressureList]
        x1 = rateList
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.scatter(x1,y1,s=10,c="b",marker="s",label='Pressure')
        plt.legend(loc='upper left')
        plt.title('Pressure data target 30 psi')
        plt.xlabel('ul/min')
        plt.ylabel('Psi')
        plt.show()
        
    def pressureTesting(self, maxPressure, sleep, rate,baselinePressure,rateIncrease,target, channelID):
        if self.testBaselinePressureCorrect(baselinePressure,channelID):
            print"baseline pressure not right"
        else:
            self.setRate(rate)
            start = time.time()
            pressureList,rateList = self.collectChannelPressure(maxRate, sleep, rateIncrease,target, rate,baselinePressure,channelID)
            end = time.time()
            timeSec = end - start
            print "The time is:",timeSec
            self.pumpStop()
            self.plotPressureList(pressureList,rateList,baselinePressure)
            return 

if __name__=='__main__':
    maxRate = 180
    sleep = 1
    startRate = 5 
    targetPressure = 20
    baselinePressure = 88 
    channelID = 7
    rateIncrease = 3
    baseline = Baseline()
    start = time.time()
    pressureData = baseline.pressureTesting(maxRate,sleep,startRate,baselinePressure,rateIncrease,targetPressure,channelID)
    end = time.time()
    print "Total time is: ",end-start
