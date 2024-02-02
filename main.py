from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from gui_class import ControlGui
from barcode_v3 import BarcodeIntake
from database_handler import DataHandler
from barcode_ip_scanner import SR_1000

'''
    TODO: Ensure we only see a 13 digit barcode, no partials.

'''

barcode_scanner_ip = '192.168.1.10'

device_list = []
thread_list = []

class Main(QObject):
    
    def __init__(self):
        super().__init__()
        
        self.gui_window = ControlGui()
        self.data_handler = DataHandler(self.gui_window)
        
        self.barcode_api = BarcodeIntake(self.gui_window, self.data_handler)
        self.barcode_scanner = SR_1000(barcode_scanner_ip, self.gui_window, self.barcode_api)
        self.information_storage = { 
                                        "TITLE": "",
                                        "AUTHOR": "",
                                        "PUBLISHER": "",
                                        "PUBLISHED_DATE": "",
                                        "GENRE": "" ,
                                        "ISBN": "",
                                        "EDITION": ""
                                    }
        
        self.barcode_thread = QThread()
        
        self.barcode_api_thread = QThread()
        
        self.agile_stock_website = QUrl('https://agilestockweb.azurewebsites.net/')
        
        self.barcode_scanner.moveToThread(self.barcode_thread)
        
        self.barcode_api.moveToThread(self.barcode_api_thread)
        
        
                
        self.barcode_thread.started.connect(self.barcode_scanner.main_function)
        self.barcode_api_thread.started.connect(self.barcode_api.main_function)
        
        
        device_list.append(self.barcode_scanner) #try different approach later
        thread_list.append(self.barcode_thread)
        thread_list.append(self.barcode_api_thread)
        
        
        
        self.gui_window.launch_website_button.clicked.connect(lambda: launch_agile_stock(self.agile_stock_website))
        self.gui_window.start_scanning_button.clicked.connect(trigger_scanner)
        self.gui_window.stop_scanning_button.clicked.connect(stop_scanner)
        self.gui_window.clear_results_button.clicked.connect(self.gui_window.clear_all_add_item_fields)
        #self.gui_window.remove_selected_item_button.clicked.connect(self.data_handler.data_item_entry)
        self.gui_window.search_database_button.clicked.connect(self.grab_isbn)
        self.gui_window.barcode_result_table.selectionModel().selectionChanged.connect(self.populate_entry_results)
        self.gui_window.submit_items_button.clicked.connect(self.add_item_to_database)

        
        #apost = self.data_handler.post_request()
        #test = self.data_handler.data_item_retrieval()
        #print(f'test: {test} apost: {apost}')
    def grab_isbn(self):
        self.data_handler.agile_stock_get_by_isbn = self.gui_window.search_database_input_box.text()
        self.data_handler.data_item_retrieval()
        self.gui_window.search_database_input_box.clear()
        
    def populate_entry_results(self):
        #print('inside populate entries')
        #print(f'\ninside main, populate entries {self.gui_window.items_for_database}\n')
        for (key, value) in self.gui_window.items_for_database.items():
            if value != '':
                self.information_storage[key] = self.gui_window.items_for_database.get(key)
                #print(f'\ninside populate enrty results {self.information_storage}\n')
        self.gui_window.write_selected_item_to_add_entry_fields()
          
    def add_item_to_database(self):
        check_value = self.gui_window.isbn_input_box.text()
        check_isbn = self.information_storage.get('ISBN')
        if check_value == check_isbn:
            print(self.information_storage)
            self.data_handler.post_request(self.information_storage)
        elif check_value:
            data_from_fields = self.gui_window.grab_input_fields()
            self.gui_window.clear_all_add_item_fields()
            self.data_handler.post_request(data_from_fields)
            
        else:
            return
        
def launch_agile_stock(url_addr):
    QDesktopServices.openUrl(url_addr)
    
def trigger_scanner():
    device_list[0].start_scanning()
    _awake_thread()
    
def _awake_thread():
    for thread in thread_list:
        thread.start()
        
def _quit_thread():
    for thread in thread_list:
        if thread.isRunning():
            thread.requestInterruption()
            thread.quit()
    
def stop_scanner():
    _quit_thread()
    device_list[0].stop_scanning()
    
        
if __name__ == '__main__':
    app = QApplication([])
    win = Main()
    
    app.exec_()
        