from array import array
from ast import Bytes
import selectors

global deviceList

class treeViewItem:
    deviceAddress: int
    deviceType: str
    deviceSector: int 
    selectors: int
    deviceChannels: array

