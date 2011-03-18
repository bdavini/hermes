# comedi_combo_test.py

import comedi as c
import time

channel = 0

comediDevice = c.comedi_open('/dev/comedi0')
print comediDevice

print "***** HANDLING INPUT DEVICE(S) *****"

inputSubdev = c.comedi_find_subdevice_by_type(comediDevice, c.COMEDI_SUBD_AI, 0)
print "input subdevice: %d" % inputSubdev 

inputMaxdata = c.comedi_get_maxdata(comediDevice, inputSubdev, channel)
print "Input max Data: %d" % inputMaxdata

nInputChannels = c.comedi_get_n_channels(comediDevice, inputSubdev)
print "Num input Channels: %d" % nInputChannels

nInputRanges = c.comedi_get_n_ranges(comediDevice, inputSubdev, channel)
print "number Input Ranges: %d" % nInputRanges

inputRange = c.comedi_get_range(comediDevice, inputSubdev, channel, 0)
print "input range: : %s" % str(inputRange)

print "Input locked? %d" % c.comedi_lock(comediDevice, inputSubdev)

print "***** HANDLING OUTPUT DEVICE(S) *****"

outputSubdev = c.comedi_find_subdevice_by_type(comediDevice, c.COMEDI_SUBD_AO, 0)
print "output subdevice: %d" % outputSubdev 

outputMaxdata = c.comedi_get_maxdata(comediDevice, outputSubdev, channel)
print "output max Data: %d" % outputMaxdata 

nOutputChannels = c.comedi_get_n_channels(comediDevice, outputSubdev)
print "Num output Channels: %d" % nOutputChannels

nOutputRanges = c.comedi_get_n_ranges(comediDevice, outputSubdev, channel)
print "number output Ranges: %d" % nOutputRanges

outputRange = c.comedi_get_range(comediDevice, outputSubdev, channel, 0)
print "output range: : %s" % str(outputRange)

print "Output locked? %d" % c.comedi_lock(comediDevice, outputSubdev)


print "***** Done handling DEVICE(S), let's get 'er done! *****"

rdata = 0 # read data
wdata = outputMaxdata/2

theRange = 0
aref = 0


# start the motor at zero speed:
c.comedi_data_write(comediDevice, outputSubdev, channel, theRange, aref, wdata)



while True:
    startTime = time.time()
    ret, rdata = c.comedi_data_read(comediDevice, inputSubdev, channel, theRange, aref)

    voltage = c.comedi_to_phys(rdata, inputRange, inputMaxdata); 
    #print "Voltage: %f" % voltage

    x1 = voltage
    x2 = x1*voltage
    x3 = x2*voltage
    x4 = x3*voltage
    x5 = x4*voltage

    dist = -14.153*x5+110.18*x4-339.89*x3+538.13*x2-479.23*x1+243.35
    #print "Distance: %f" % dist

    if dist > 50:
        wdata = outputMaxdata/2 + 1000
    else:
        wdata = outputMaxdata/2


    #print 'Writing %d to the motor' % wdata
    c.comedi_data_write(comediDevice, outputSubdev, channel, theRange, aref, wdata)
    print time.time() - startTime

    #time.sleep(1)

print "Closing %s" % str(comediDevice)
c.comedi_close(comediDevice)
