import time
import ctypes # provides C compatible data types (*MA)
import threading
from ctypes.util import find_library

CFArrayRef = ctypes.c_void_p
CFMutableArrayRef = ctypes.c_void_p
CFIndex = ctypes.c_long

# seems to show the device number... (*MA)
MultitouchSupport = ctypes.CDLL("/System/Library/PrivateFrameworks/MultitouchSupport.framework/MultitouchSupport")

# getting the number of devices? (*MA)
CFArrayGetCount = MultitouchSupport.CFArrayGetCount
CFArrayGetCount.argtypes = [CFArrayRef]
CFArrayGetCount.restype = CFIndex

# gets the device code, I think (*MA)
CFArrayGetValueAtIndex = MultitouchSupport.CFArrayGetValueAtIndex
CFArrayGetValueAtIndex.argtypes = [CFArrayRef, CFIndex]
CFArrayGetValueAtIndex.restype = ctypes.c_void_p

MTDeviceCreateList = MultitouchSupport.MTDeviceCreateList
MTDeviceCreateList.argtypes = []
MTDeviceCreateList.restype = CFMutableArrayRef

class MTPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class MTVector(ctypes.Structure):
    _fields_ = [("position", MTPoint),
                ("velocity", MTPoint)]

class MTData(ctypes.Structure):
    _fields_ = [
      ("frame", ctypes.c_int),
      ("timestamp", ctypes.c_double),
      ("identifier", ctypes.c_int),
      ("state", ctypes.c_int),  # Current state (of unknown meaning).
      ("unknown1", ctypes.c_int),
      ("unknown2", ctypes.c_int),
      ("normalized", MTVector),  # Normalized position and vector of
                                 # the touch (0 to 1).
      ("size", ctypes.c_float),  # The area of the touch.
      ("unknown3", ctypes.c_int),
      # The following three define the ellipsoid of a finger.
      ("angle", ctypes.c_float),
      ("major_axis", ctypes.c_float),
      ("minor_axis", ctypes.c_float),
      ("unknown4", MTVector),
      ("unknown5_1", ctypes.c_int),
      ("unknown5_2", ctypes.c_int),
      ("unknown6", ctypes.c_float),
    ]

MTDataRef = ctypes.POINTER(MTData)

MTContactCallbackFunction = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, 
                     MTDataRef, ctypes.c_int, ctypes.c_double, ctypes.c_int)

MTDeviceRef = ctypes.c_void_p

MTRegisterContactFrameCallback = (MultitouchSupport.MTRegisterContactFrameCallback)
MTRegisterContactFrameCallback.argtypes = [MTDeviceRef, 
                                               MTContactCallbackFunction]
MTRegisterContactFrameCallback.restype = None

### Edited 11/16 1:17 (*MA)
### original is commented out
MTDeviceStart = MultitouchSupport.MTDeviceStart
#MTDeviceStart.argtypes = [MTDeviceRef, ctypes.c_int] # original
MTDeviceStart.argtypes = [MTDeviceRef]
#MTDeviceStart.restype = None

### Edited: 11/16 1:19am (*MA)
### no original, simply adding
### info from http://va.nortd.com/doc/0.4.3/
### _multipad_8h.html#ada4b897ee40b40efbf0b87a337d97e67
### when called, suspends the MTDevice function

MTDeviceStop = MultitouchSupport.MTDeviceStop
MTDeviceStop.argtypes = [MTDeviceRef]

### Added: 11/16 16:30 (*MA)
def initMT():
    global MTPosSet
    # store values in a set
    MTPosSet = set()
    # finds out what device exists on this computer
    devices = MultitouchSupport.MTDeviceCreateList()
    # returns the number of devices. not really necessary
    num_devices = CFArrayGetCount(devices)
    # the device unique number - used to start and stop devices. important
    device = CFArrayGetValueAtIndex(devices, 0)
    # runs the loop for taking trackpad position
    MTRegisterContactFrameCallback(device, my_callback)
    return device # used in main function to start/stop device

### Edited: adds points to a set so values are not lost in Tkinter refresh

@MTContactCallbackFunction
def my_callback(device, data_ptr, n_fingers, timestamp, frame):
    global MTPosSet
    #print threading.current_thread(), device, data_ptr, 
                                                 #n_fingers, timestamp, frame
    for i in xrange(n_fingers):
        data = data_ptr[i]
        d = "x=%.2f, y=%.2f" % (data.normalized.position.x * 100,
                                data.normalized.position.y * 100)
        #print "%d: %s" % (i, d) # printing location on trackpad! (*MA)
        # added: record position on global MTPos so it can be returned!
        # also flipped the y coordinate to fit the Tkinter screen
        MTPosSet.add((round(data.normalized.position.x,4), 
                                1 - round(data.normalized.position.y,4)))
    return 0

### Added: 11/16 17:02 (*MA)
def returnMTPos():
    global MTPosSet
    localMTPosSet = MTPosSet
    MTPosSet = set()
    return localMTPosSet

def clearMTPos():
    global MTPosSet
    MTPosSet = set()

### running the function below...! (*MA)

#devices = MultitouchSupport.MTDeviceCreateList()
#num_devices = CFArrayGetCount(devices)
#print "num_devices =", num_devices
#for i in xrange(num_devices):
#    device = CFArrayGetValueAtIndex(devices, i)
#    print "device #%d: %016x" % (i, device)
#    MTRegisterContactFrameCallback(device, my_callback)
#    MTDeviceStart(device, 0)

#while threading.active_count():
#    # Why sleep instead of join? Ask David Beazley.
#    time.sleep(0.125)
