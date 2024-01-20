from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from pycomm3 import CIPDriver
from pycomm3.cip.data_types import UINT, STRING, Struct
from pycomm3.logger import configure_default_logger as data_logger

class SR_1000(QObject):
    
    def __init__(self, barcode_ip):
        self.ip_addr = barcode_ip
        
        