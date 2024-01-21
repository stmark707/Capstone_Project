from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices
from gui_class import ControlGui
from barcode_ip_scanner import SR_1000



barcode_scanner_ip = '192.168.1.10'

device_list = []
thread_list = []

class Main(QObject):
    
    def __init__(self):
        super().__init__()
        
        self.gui_window = ControlGui()
        self.barcode_scanner = SR_1000(barcode_scanner_ip, self.gui_window)
        self.barcode_thread = QThread()
        
        self.agile_stock_website = QUrl('https://agilestockweb.azurewebsites.net/')
        
        self.barcode_scanner.moveToThread(self.barcode_thread)
        
        self.barcode_thread.started.connect(self.barcode_scanner.main_function)
        
        device_list.append(self.barcode_scanner) #try different approach later
        thread_list.append(self.barcode_thread)
        
        self.gui_window.launch_website_button.clicked.connect(lambda: launch_agile_stock(self.agile_stock_website))
        self.gui_window.start_scanning_button.clicked.connect(trigger_scanner)
        self.gui_window.stop_scanning_button.clicked.connect(stop_scanner)
 
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
    
    app.exec()
        