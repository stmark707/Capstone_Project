from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from datetime import datetime
from pycomm3 import CIPDriver
from pycomm3.cip.data_types import UINT, STRING
from pycomm3.logger import configure_default_logger as data_logger

time_string = datetime.now()
the_month = time_string.month
the_day = time_string.day
the_year = time_string.year


class SR_1000(QObject):
    
    successful_read = pyqtSignal(bool, name='Barcode data Available')
    barcode_string = pyqtSignal(str, name="Scanned barcode")
    
    
    def __init__(self, barcode_ip):
        self.ip_addr = barcode_ip
        self.title = str(the_month) + '_' + str(the_day) + '_' + str(the_year) + '_' + 'Barcode_logger'
        self.filepath = ('barcode_logger' + '/' + self.title)
        self.data_logger(filename=self.filepath)
        
        self.barcode_scanner = CIPDriver(self.ip_addr)
        
        self.barcode_class_id = b'\x69'
        self.barcode_instance_id = b'\x01'
        
        self.service_data_start = b'\xFF\xFF'
        self.read_status_attribute_id = b'\x64'
        
        self.service_data_result = UINT[2].encode([200,0])
        self.check_read_status = UINT[None] 
        
        self.sr_1000_service_dict = {
                                        "get_attribute_single": b'\x0E',
                                        "get_attribute_all": b'\x01',
                                        "set_attribute": b'\x10',
                                        "start_read": b'\x4B',
                                        "stop_read" : b'\x4C',
                                        "acquire_read": b'\x55',
                                        "reset_error": b'\x53',
                                        "clear_reset_and_error_bits": b'\x5A',
                                        "get_member": b'\x18',
                                        "device_reset" : b'\x05'
                            
                                    }
        
        self.start_scan = "Start Scanning"
        self.grab_barcode = "Result Data"
        self.stop_scan  = "Stop Scanning"
        
        self.barcode_read_status = []
        self.barcode_string = ''
        
        
        