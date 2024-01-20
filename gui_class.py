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
        
        self.show()        
        
        
        
if __name__ == '__main__':
    app = QApplication([])
    win = ControlGui()
    
    app.exec()