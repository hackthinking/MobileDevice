#!/usr/bin/python
# coding: utf-8

# Copyright (c) 2013 Mountainstorm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from amdevice import *
from plistservice import *
from afc import *
import pprint


class InstallationProxy(PlistService):
	def __init__(self, amdevice):
		PlistService.__init__(
			self, 
			amdevice, 
			[AMSVC_INSTALLATION_PROXY], 
			kCFPropertyListXMLFormat_v1_0
		)

	if platform.system() == u'Darwin':
		def lookup_applications(self, options=None):
			retval = []
			self._sendmsg({
				u'Command': u'Browse',
				u'ClientOptions': {
					u'ApplicationType': u'Any'
				}
			})
			# I've no idea why we get it in multiple responses .. but we do
			while True:
				reply = self._recvmsg()
				if (    reply is None 
					or (    u'Status' in reply 
						and reply[u'Status'] == u'Complete')):
					break # done
				for app in reply[u'CurrentList']:
					retval.append(app)
			return retval
	else:
		def lookup_applications(self, options=None):
			retval = []
			cflist = CFDictionaryRef()
			AMDeviceLookupApplications(self.dev.dev, options, byref(cflist))
			applist = CFTypeTo(cflist)
			for id, info in applist.items():
				retval.append(info)
			return retval

	def install_application(self, path, options=None, progress=None):
		u'''Install an application from the /PublicStaging directory'''
		self._install_or_upgrade(True, path, options, progress)

	def upgrade_application(self, path, options=None, progress=None):
		u'''Upgrade an application from the /PublicStaging directory'''
		self._install_or_upgrade(False, path, options, progress)

	def _install_or_upgrade(self, install, path, options=None, progress=None):
		def callback(cfdict, arg):
			info = CFTypeTo(cfdict)
			pprint.pprint(info)

		cfpath = CFTypeFrom(path)
		if options is not None:
			cfoptions = CFTypeFrom(options)
		else:
			cfoptions = CFTypeFrom({
				u'PackageType': u'Developer'
			})
		cb = AMDeviceProgressCallback(callback)
		if progress is not None:
			cb = AMDeviceProgressCallback(progress)

		if install:
			err = AMDeviceInstallApplication(self.s, cfpath, cfoptions, cb, None)
		else:
			err = AMDeviceUpgradeApplication(self.s, cfpath, cfoptions, cb, None)
		CFRelease(cfpath)
		CFRelease(cfoptions)
		if err != MDERR_OK:
			raise RuntimeError(u'Unable to install application', err)
		
	def uninstall_application(self, appid, options=None):
		u'''Uninstall the application'''
		def callback(cfdict, arg):
			info = CFTypeTo(cfdict)
			pprint.pprint(info)

		cfappid = CFTypeFrom(appid)
		cb = AMDeviceProgressCallback(callback)
		AMDeviceUninstallApplication(self.s, cfappid, options, cb, None)

	# TODO: archive, restore, etc



def register_argparse_install(cmdargs):
	import argparse
	import sys
	import pprint
	import afcmediadirectory

	# AMDSetLogLevel(0xff)
	# AMDSetLogLevel(0x0)

	def cmd_install(args, dev):
		path = args.path.decode(u'utf-8')
		print path
		afc = afcmediadirectory.AFCMediaDirectory(dev)
		pxy = InstallationProxy(dev)
		pprint.pprint(afc.transfer_application(path))
		pprint.pprint(pxy.install_application(path))
		pxy.disconnect()
		afc.disconnect()

	def cmd_browse(args, dev):
		pxy = InstallationProxy(dev)
		pprint.pprint(pxy.lookup_applications())
		pxy.disconnect()

	def cmd_listapps(args, dev):
		pxy = InstallationProxy(dev)
		apps = {}
		maxappid = 0
		for app in pxy.lookup_applications():
			appid = app[u'CFBundleIdentifier'].decode(u'utf-8')
			apps[appid] = app[u'Path'].decode(u'utf-8')
			if len(appid) > maxappid:
				maxappid = len(appid)
		pxy.disconnect()
		for appid in sorted(apps.keys()):
			apppath = apps[appid]
			print(appid.ljust(maxappid) + u' ' + apppath)

	def cmd_uninstall(args, dev):
		appid = args.appid.decode(u'utf-8')
		pxy = InstallationProxy(dev)
		pprint.pprint(pxy.uninstall_application(appid))
		pxy.disconnect()

	installparser = cmdargs.add_parser(
		u'install', 
		help=u'installation proxy commands'
	)
	installcmd = installparser.add_subparsers()

	# install command
	instcmd = installcmd.add_parser(
		u'install',
		help=u'install applications on the device'
	)
	instcmd.add_argument(
		u'path',
		help=u'applications path'
	)
	instcmd.set_defaults(func=cmd_install)

	# browse command
	browsecmd = installcmd.add_parser(
		u'browse',
		help=u'list all information about applications on the device'
	)
	browsecmd.set_defaults(func=cmd_browse)

	# listappid command
	listappscmd = installcmd.add_parser(
		u'listapps',
		help=u'lists all application ids'
	)
	listappscmd.set_defaults(func=cmd_listapps)

	# uninstall command
	uninstallcmd = installcmd.add_parser(
		u'uninstall',
		help=u'uninstall the application'
	)
	uninstallcmd.add_argument(
		u'appid',
		help=u'the application id'
	)
	uninstallcmd.set_defaults(func=cmd_uninstall)

