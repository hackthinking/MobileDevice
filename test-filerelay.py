from MobileDevice import *
#from amdevice import *
#from filerelay import *

dev = list_devices(1)[0]
dev.connect()
fr = FileRelay(dev)

f = open(u'dump.cpio.gz', 'wb')
f.write(fr.get_filesets([
        u'AppleSupport',
        u'Network',
        u'VPN',
        u'WiFi',
        u'UserDatabases',
        u'CrashReporter',
        u'tmp',
        u'SystemConfiguration'
]))
f.close()

fr.disconnect()

