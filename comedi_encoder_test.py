import comedi as c
import sys, time

dev = c.comedi_open('/dev/comedi0')
print dev

maxdata = c.comedi_get_maxdata(dev, 0, 0)
print "Max Data: %d" % maxdata

subdev = c.comedi_find_subdevice_by_type(dev, c.COMEDI_SUBD_COUNTER, 0)
print "Subdevice: %d" % subdev

print "Locked? %d" % c.comedi_lock(dev, subdev)

nChannels = c.comedi_get_n_channels(dev, subdev)
print "Num Channels: %d" % nChannels

crange = c.comedi_get_range(dev, 0, 0, 0)
print "Range: %s" % str(crange)

params = c.chanlist(1)
params[0] = 0

# configure the encoder
instr = c.comedi_insn_struct()
instr.insn = c.INSN_CONFIG
instr.n = 1
instr.data = params
instr.subdev = 5
# instr.chanspec = c.cr_pack(0,0,c.AREF_OTHER)
instr.chanspec = c.cr_pack(0,0,0)

ret=c.comedi_do_insn(dev,instr);
print ret

# Encoder read instruction */
instr.insn=c.INSN_READ
instr.n=1
instr.data=params
instr.subdev=5
#instr.chanspec=c.cr_pack(0,0,AREF_OTHER);
instr.chanspec=c.cr_pack(0,0,0);

#read the damn data
for i in range(5):
    ret=c.comedi_do_insn(dev, instr);
    print params[0]
    time.sleep(1)

#device, subdevice, channel, range, aref, data (for a read)

print "Closing %s" % str(dev)
c.comedi_close(dev)
