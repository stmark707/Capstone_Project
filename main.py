from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, QThread, pyqtSignal




barcode_scanner_ip = '192.168.1.10'


class Main(QObject):
    
    def __init__(self):
        super().__init__()
        