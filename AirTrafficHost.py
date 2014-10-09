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


from ctypes import *
import platform

from CoreFoundation import *


if platform.system() == u'Darwin':
	ATH = CDLL(u'/System/Library/PrivateFrameworks/MobileDevice.framework/AirTrafficHost')
elif platform.system() == u'Windows':
	ATH = CDLL(u'AirTrafficHost.dll')
elif platform.system() == u'CYGWIN_NT-5.1' or platform.system() == u'CYGWIN_NT-6.3-WOW64':
	ATH = CDLL(u'AirTrafficHost.dll')
else:
	raise OSError(u'Platform not supported')

ATHostConnectionCreateWithLibrary = ATH.ATHostConnectionCreateWithLibrary
ATHostConnectionCreateWithLibrary.restype = c_int
ATHostConnectionCreateWithLibrary.argtypes = [CFStringRef, CFStringRef, c_int]

ATHostConnectionSendPowerAssertion = ATH.ATHostConnectionSendPowerAssertion
ATHostConnectionSendPowerAssertion.restype = c_int
ATHostConnectionSendPowerAssertion.argtypes = [c_int, CFBooleanRef]

ATHostConnectionSendSyncRequest = ATH.ATHostConnectionSendSyncRequest
ATHostConnectionSendSyncRequest.restype = c_int
ATHostConnectionSendSyncRequest.argtypes = [c_int, CFMutableArrayRef, CFMutableDictionaryRef, CFMutableDictionaryRef]

ATHostConnectionReadMessage = ATH.ATHostConnectionReadMessage
ATHostConnectionReadMessage.restype = c_void_p
ATHostConnectionReadMessage.argtypes = [c_int]

ATHostConnectionSendHostInfo = ATH.ATHostConnectionSendHostInfo
ATHostConnectionSendHostInfo.restype = c_int
ATHostConnectionSendHostInfo.argtypes = [c_int, CFMutableDictionaryRef]

ATHostConnectionGetGrappaSessionId = ATH.ATHostConnectionGetGrappaSessionId
ATHostConnectionGetGrappaSessionId.restype = c_uint
ATHostConnectionGetGrappaSessionId.argtypes = [c_int]

ATHostConnectionRetain = ATH.ATHostConnectionRetain
ATHostConnectionRetain.restype = c_int
ATHostConnectionRetain.argtypes = [c_int]

ATHostConnectionRelease = ATH.ATHostConnectionRelease
ATHostConnectionRelease.restype = c_void_p
ATHostConnectionRelease.argtypes = [c_int]

ATHostConnectionDestroy = ATH.ATHostConnectionDestroy
ATHostConnectionDestroy.restype = c_int
ATHostConnectionDestroy.argtypes = [c_int]

ATHostConnectionSendMetadataSyncFinished = ATH.ATHostConnectionSendMetadataSyncFinished
ATHostConnectionSendMetadataSyncFinished.restype = c_int
ATHostConnectionSendMetadataSyncFinished.argtypes = [c_int, CFMutableDictionaryRef, CFMutableDictionaryRef]

