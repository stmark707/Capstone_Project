from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor, QBrush, QDoubleValidator
import sys

'''
    TODO: write function to grab selected item from table, pass it to items for database
'''

class ControlGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ControlGui, self).__init__()
        uic.loadUi('design_files/simplified_inventory_interface.ui', self)
        
        self.barcode_result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.barcode_result_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.database_entry_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.database_entry_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.remove_item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.remove_item_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
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
        
        self.color_list = ['#52A40','#F57900', '#204A87', '#080808']
        
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
                                        
        self.add_item_list = [self.book_title_input_box, self.author_input_box, self.genre_input_box, self.isbn_input_box, self.publisher_date_input_box, 
                                 self.edition_input_box, self.publisher_input_box]
        
        '''
            TODO: Get publisher or publishing date
            TODO: Get book edition
        '''
        
        self.items_for_database = {
                                    'TITLE': '',
                                    'AUTHOR': '',
                                    'GENRE' : '',
                                    'ISBN': '',
                                    'PUBLISHER DATE' : '',
                                    'PUBLISHER' : '',
                                    'EDITION': ''
                                }
        
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
    
    @pyqtSlot(object, name="Full book info")        
    def book_information_transfer(self, book_info):
        self.items_for_database = book_info.copy()
        print(f'inside book information transfer {self.items_for_database}')
            
    def write_to_database_entry_table(self, recent_entry):
        # will take in a list, passed from barcode api
        pass
    
    @pyqtSlot(list, name="barcode result list")
    def write_to_barcode_search_table(self, barcode_search_results):
        row_count = self.barcode_result_table.rowCount()
        self.barcode_result_table.insertRow(row_count)
        
        
        for item in range(4):
            temp = QTableWidgetItem(barcode_search_results[item])
            temp.setTextAlignment(Qt.AlignCenter)
            temp.setForeground(QBrush(QColor(self.color_list[item])))
            self.barcode_result_table.setItem(row_count, item, temp)
            self.barcode_result_table.resizeRowToContents(row_count)
            self.barcode_result_table.scrollToBottom()
    
    def write_selected_item_to_add_entry_fields(self):
        #write items selected in barcode search table to their fields, 
        for (index, (key, value)) in enumerate(self.items_for_database.items()):
            if value != '':
                info = self.items_for_database.get(key)
                self.add_item_list[index].setText(info)
                print(info)
                print(index)
            else:
                continue
                
    def grab_input_fields(self):
        pass
    
    @pyqtSlot(list, name="Database search results")
    def write_to_database_remove_item_table(self, items_to_display):
        pass
    
    def clear_all_add_item_fields(self):
        
        for items in range(len(self.add_item_list)):
            self.add_item_list[items].clear()
    
        
if __name__ == '__main__':
    app = QApplication([])
    win = ControlGui()
    
    app.exec_()