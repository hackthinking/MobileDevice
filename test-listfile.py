from MobileDevice import *

dev = list_devices()[0]
dev.connect()
afc = AFCMediaDirectory(dev)
for name in afc.listdir(u'/'):
    print name

sb = Springboard(dev)

icon = sb.get_iconpngdata(u'com.xiami.spark')
print icon

afc.disconnect()

