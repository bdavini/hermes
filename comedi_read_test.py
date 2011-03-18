import comedi as c
import time

channel = 0

dev = c.comedi_open('/dev/comedi0')
print dev

maxdata = c.comedi_get_maxdata(dev, 0, 0)
print "Max Data: %d" % maxdata

subdev = c.comedi_find_subdevice_by_type(dev, c.COMEDI_SUBD_AI, 0)
print "Subdevice: %d" % subdev

print "Locked? %d" % c.comedi_lock(dev, subdev)

nChannels = c.comedi_get_n_channels(dev, subdev)
print "Num Channels: %d" % nChannels

nRanges = c.comedi_get_n_ranges(dev, subdev, channel)
print "Ranges: %d" % nRanges

crange = c.comedi_get_range(dev, subdev, channel, 0)
print "comedi_get_range: %s" % str(crange)

data = maxdata/2

rdata = 0

nChannels = 2

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
