import comedi as c

dev = c.comedi_open('/dev/comedi0')
print dev

maxdata = c.comedi_get_maxdata(dev, 0, 0)
print "Max Data: %d" % maxdata

subdev = c.comedi_find_subdevice_by_type(dev, c.COMEDI_SUBD_AO, 0)
print "Subdevice: %d" % subdev

print "Locked? %d" % c.comedi_lock(dev, subdev)

nChannels = c.comedi_get_n_channels(dev, subdev)
print "Num Channels: %d" % nChannels

crange = c.comedi_get_range(dev, 0, 0, 0)
print "Range: %s" % str(crange)

data = maxdata/2

# start with no speed
c.comedi_data_write(dev, subdev, 0, 0, 0, data)

while True:
    usrin = raw_input("Enter a char: ")
    if usrin is 'q':
        break
    elif usrin is 'o':
        data = data + 10 
    elif usrin is 'l':
        data = data - 10

    print 'Writin %d to the motor' % data
    c.comedi_data_write(dev, subdev, 0, 0, 0, data)

print "Writing 0 to the channel: %d" % int(maxdata/2)
c.comedi_data_write(dev, subdev, 0, 0, 0, maxdata/2)

print "Closing %s" % str(dev)
c.comedi_close(dev)
