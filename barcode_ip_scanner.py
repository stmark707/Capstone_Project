from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from gui_class import ControlGui
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
    barcode_connect = pyqtSignal(bool, name='Scanning Status')
    finished_method = pyqtSignal()
    
    def __init__(self, barcode_ip, gui_window: ControlGui):
        super().__init__()
        self.ip_addr = barcode_ip
        self.title = str(the_month) + '_' + str(the_day) + '_' + str(the_year) + '_' + 'Barcode_logger'
        self.filepath = ('barcode_logger' + '/' + self.title)
        data_logger(filename=self.filepath)
        
        self.gui = gui_window
        self.barcode_scanner = CIPDriver(self.ip_addr)
        
        self.barcode_thread = QThread()
        
        
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
                                        "device_reset" : b'\x05',
                                        "read_complete_clear": b'\x5A'
                            
                                    }
        
        self.start_scan = "Start Scanning"
        self.grabs_barcode = "Result Data"
        self.stop_scan  = "Stop Scanning"
        self.reset_read_complete = "Clear Read Complete"
        self.read_success = "Reading Status"
        
        self.currently_scanning = False
        self.read_complete = 0
        
        self.barcode_read_status = []
        self.barcode = ''
        
        self.successful_read.connect(self.gui.change_barcode_status_message)
        self.barcode_string.connect(self.gui.barcode_string)
        self.barcode_connect.connect(self.gui.barcode_comm_status)
    
    @pyqtSlot(bool, name='Scanning Status')
    def start_scanning(self):
        if not self.currently_scanning:
            self.currently_scanning = True
            with self.barcode_scanner:
                reset_read = self.barcode_scanner.generic_message(self.sr_1000_service_dict.get("read_complete_clear"), self.barcode_class_id, self.barcode_instance_id, data_type=None, 
                                                        name= self.reset_read_complete, connected=True, unconnected_send=False)
                start_scan = self.barcode_scanner.generic_message(self.sr_1000_service_dict.get("start_read"), self.barcode_class_id, self.barcode_instance_id, request_data=self.service_data_start, data_type=None, 
                                        name= self.start_scan, connected=True, unconnected_send=False )
            self.barcode_connect.emit(self.currently_scanning)
            self.finished_method.emit()
                
            self.read_status()
        
    
    @pyqtSlot(bool, name='Barcode data Available')
    def read_status(self):
        try:
            with self.barcode_scanner:
                reset_read = self.barcode_scanner.generic_message(self.sr_1000_service_dict.get("read_complete_clear"), self.barcode_class_id, self.barcode_instance_id, data_type=None, 
                                                            name= self.reset_read_complete, connected=True, unconnected_send=False)
                read_status_ = self.barcode_scanner.generic_message(self.sr_1000_service_dict.get("get_attribute_single"), self.barcode_class_id, self.barcode_instance_id, attribute=self.read_status_attribute_id, data_type=self.check_read_status, 
                                            name= self.read_success, connected=True, unconnected_send=False )
                
                self.read_complete = read_status_[1][1]
                
        except Exception:
            return
        self.successful_read.emit(self.read_complete)
        self.finished_method.emit()
       
    
    def main_function(self):
        while self.currently_scanning:
            try:
                self.read_status()
                if self.read_complete:
                    self.grab_barcode()
                else: 
                    continue
            except Exception as message:
                print(message)
                return
    
    @pyqtSlot(str, name='Scanned barcode')
    def grab_barcode(self):
        with self.barcode_scanner:
            get_data = self.barcode_scanner.generic_message(self.sr_1000_service_dict.get("acquire_read"), self.barcode_class_id, self.barcode_instance_id, request_data=self.service_data_result, data_type=STRING, 
                                                    name= self.grabs_barcode, connected=True, unconnected_send=False)
            try:
                get_data = list(get_data)
                barcode = get_data[1]
                self.barcode = barcode[3:-4]
            except TypeError:
                return
            except IndexError:
                return
        self.barcode_string.emit(self.barcode)
        self.finished_method.emit()
            
    @pyqtSlot(bool, name='Scanning Status')
    def stop_scanning(self):
        if self.currently_scanning:
            self.currently_scanning = False
            self.barcode_connect.emit(self.currently_scanning)
            self.finished_method.emit()
        
            with self.barcode_scanner:
                stop_reading = self.barcode_scanner.generic_message(self.sr_1000_service_dict.get("stop_read"), self.barcode_class_id, self.barcode_instance_id, data_type=None, 
                                name= self.stop_scan, connected=True, unconnected_send=False )
            
            
            