from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem, QApplication
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QColor, QBrush, QDoubleValidator
import sys

class ControlGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ControlGui, self).__init__()
        uic.loadUi('design_files/simplified_inventory_interface.ui', self)
        
        self.barcode_result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(2))
        self.barcode_result_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(2))
        
        self.database_entry_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(2))
        self.database_entry_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(2))
        
        self.remove_item_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(2))
        self.remove_item_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode(2))
        
        self.add_items_button.clicked.connect(lambda: self.database_actions_stacked_widget.setCurrentIndex(0))
        self.remove_item_button.clicked.connect(lambda: self.database_actions_stacked_widget.setCurrentIndex(1))
        
        
        
        self.color_dict = {
                            'teal_blue': '#09486d',
                            'dark_blue': '#52A40',
                            'lighter_black': '#080808',
                            'blumine': '#204A87',
                            'orange': '#cc5c00',
                            'green': '#037120',
                            'bright_orange': '#F57900',
                            'trendy_pink': '#75507B',
                            'azure_blue': '#3465a4',
                            'red' : '#E90B0B'
                        }
        
        self.barcode_default_comm_stylesheet = '''
                                                    color: White;
                                                    font-family: "SourceSansPro-Bold";
                                                    font-weight: 600;
                                                    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #DBE9F3, stop: 0.1 #FF0000, stop: 0.5 #FF0000, stop: 1 #E90B0B, stop: 1 #BB0009);
                                                    font-size: 14px;
                                                    border-radius: 4px;
                                                    border-style: outset;
	                                                border-width: 1px;
	                                                border-color:black;
	                                                padding: 6px;
	                                                outline-offset: 4px;
                                            '''
                                            
        self.barcode_scanning_stylesheet = '''
                                                    color: White;
	                                                font-family: "SourceSansPro-Bold";
	                                                font-weight: 600;
	                                                font-size: 14px;
	                                                background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #98FF99, stop: 0.1 #78C26B, stop: 0.5 #4DB044, stop: 1 #4DB044, stop: 1 #248423);
	                                                border-style: outset;
	                                                border-width: 1px;
	                                                border-color:black;
	                                                padding: 6px;
	                                                outline-offset: 4px;
	                                                border-radius: 4px;
                                        '''
        
        self.show()        
        
    @pyqtSlot(bool, name='Barcode data Available')
    def change_barcode_status_message(self, read_status):
        if read_status:
            self.barcode_status_dynamic_label.setText('Read Successful')
        else:
            self.barcode_status_dynamic_label.setText('Read Unsuccessful')
    
    @pyqtSlot(bool, name="Scanning Status")       
    def barcode_comm_status(self, scanning):
        if scanning:
            self.barcode_scanner_comm_label.setStyleSheet(self.barcode_scanning_stylesheet)
        else:
            self.barcode_scanner_comm_label.setStyleSheet(self.barcode_default_comm_stylesheet)
        
    @pyqtSlot(str, name='Scanned barcode')
    def barcode_string(self, barcode):
        if barcode:
            self.item_barcode_dynamic_label.setText(barcode)
            self.isbn_search_dynamic_label.setText(barcode)
        else:
            self.item_barcode_dynamic_label.setText('{NULL}')
            self.isbn_search_dynamic_label.setText('{NULL}')
        
if __name__ == '__main__':
    app = QApplication([])
    win = ControlGui()
    
    app.exec()