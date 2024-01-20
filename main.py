from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices
from gui_class import ControlGui
from barcode_ip_scanner import SR_1000



barcode_scanner_ip = '192.168.1.10'


class Main(QObject):
    
    def __init__(self):
        super().__init__()
        
        self.gui_window = ControlGui()
        self.barcode_scanner = SR_1000(barcode_scanner_ip)
        self.agile_stock_website = QUrl('https://agilestockweb.azurewebsites.net/')
        
        self.gui_window.launch_website_button.clicked.connect(lambda: launch_agile_stock(self.agile_stock_website))
        
 
def launch_agile_stock(url_addr):
    QDesktopServices.openUrl(url_addr)
    
        
if __name__ == '__main__':
    app = QApplication([])
    win = Main()
    
    app.exec()
        