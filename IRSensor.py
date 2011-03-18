import comedi as c
import time, sys
from multiprocessing import *

class IRSensor:
    def __init__(self, channel = 0):
        self.value = 0
        self.voltage = 0
        self.distance = 0
        self.channel = channel

    def read(self, comediObject):
        ret, self.value = c.comedi_data_read(comediObject.device, comediObject.subdevice, self.channel, 0, 0)
        self.voltage = c.comedi_to_phys(self.value, comediObject.channelRange, comediObject.maxdata)

class LongIRSensor(IRSensor):
    def __init__(self, channel = 0):
        self.value = 0
        self.voltage = 0
        self.distance = 0
        self.channel = channel

class ComediObject:
    def __init__(self, subdevice = c.COMEDI_SUBD_AI):
        self.device = c.comedi_open('/dev/comedi0')
        self.subdevice = c.comedi_find_subdevice_by_type(self.device, subdevice, 0)
        self.numChannels = c.comedi_get_n_channels(self.device, self.subdevice)
        self.numRanges = c.comedi_get_n_channels(self.device, self.subdevice)
        self.channelRange = c.comedi_get_range(self.device, self.subdevice, 0, 0)
        self.maxdata = c.comedi_get_maxdata(self.device, 0, 0)

class SensorManager:
    def __init__(self, comediObj, numSensors):
        self.comediObject = comediObj
        self.sensorList = []
        self.numSensors = numSensors
        self.pool = Pool(processes=4)

    def addSensors(self):
        for i in range(self.numSensors):
            self.sensorList.append(LongIRSensor(i))

    def startAcquisition(self):
        for sensor in self.sensorList:
            Process(target=sensor.read, args=(comediObj,)).start()
            #self.pool.apply_async(sensor.read, [self.comediObject])


#main

comediObj = ComediObject()

sm = SensorManager(comediObj, 1)
sm.addSensors()
sm.startAcquisition()

while True:
    print sm.sensorList[0].value
    time.sleep(1)

sys.exit()

for i in range(100):
    for chan in range(nChannels):
        ret, rdata = c.comedi_data_read(dev, subdev, chan, 0, 0)
        #print "Read value: %d" % rdata

        voltage = c.comedi_to_phys(rdata, crange, maxdata); 
        #print voltage

        x1 = voltage
        x2 = x1*voltage
        x3 = x2*voltage
        x4 = x3*voltage
        x5 = x4*voltage

        dist = -14.153*x5+110.18*x4-339.89*x3+538.13*x2-479.23*x1+243.35
        print "Chan %d Distance: %f" % (chan, dist)

    print
    time.sleep(1)

print "Closing %s" % str(dev)
c.comedi_close(dev)
