from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, QRegExp
from PyQt5.QtGui import QColor, QBrush, QRegExpValidator
import sys

'''
    TODO: write function to grab selected item from table, pass it to items for database
'''

class ControlGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ControlGui, self).__init__()
        uic.loadUi('design_files/simplified_inventory_interface_manual_search_added.ui', self)
        
        self.database_actions_stacked_widget.setCurrentIndex(0)
        self.barcode_api_stacked_widget.setCurrentIndex(0)
        
        self.barcode_result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.barcode_result_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.database_entry_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.database_entry_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.remove_item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.remove_item_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.add_items_button.clicked.connect(lambda: self.database_actions_stacked_widget.setCurrentIndex(0))
        self.remove_item_button.clicked.connect(lambda: self.database_actions_stacked_widget.setCurrentIndex(1))
        
        self.clear_entry_table_button.clicked.connect(self.clear_recent_entry_table)
        
        self.barcode_scanner_radio_button.toggled.connect(lambda: self.barcode_api_stacked_widget.setCurrentIndex(0))
        self.no_device_radio_button.toggled.connect(lambda: self.barcode_api_stacked_widget.setCurrentIndex(1))
        
        isbn_regex = QRegExp("^\\d{13}$")
        
        isbn_validator = QRegExpValidator(isbn_regex, self)
        
        self.isbn_search_input_box.setValidator(isbn_validator)
        self.isbn_input_box.setValidator(isbn_validator)
        
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
        self.entry_color_list = ['#52A40', '#037120']
        self.removal_color_list = ['#080808','#037120','#3465a4']
        
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
        
            
    def write_to_database_entry_table(self, recent_entry):
        # will take in a list, passed from barcode api
        row_count = self.database_entry_table.rowCount()
        self.database_entry_table.insertRow(row_count)
        
        for item in range(2):
            temp = QTableWidgetItem(recent_entry[item])
            temp.setTextAlignment(Qt.AlignCenter)
            temp.setForeground(QBrush(QColor(self.entry_color_list[item])))
            self.database_entry_table.setItem(row_count, item, temp)
            self.database_entry_table.resizeRowToContents(row_count)
            self.database_entry_table.scrollToBottom()
            
    
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
            else:
                continue
                
    def grab_input_fields(self):
        items_for_database = {
                                    'TITLE': '',
                                    'AUTHOR': '',
                                    'GENRE' : '',
                                    'ISBN': '',
                                    'PUBLISHED_DATE' : '',
                                    'PUBLISHER' : '',
                                    'EDITION': ''
                                }
        
        for (index, (key, value)) in enumerate(items_for_database.items()):
            items_for_database[key] = self.add_item_list[index].text()
        return items_for_database
                
    
    def write_to_database_remove_item_table(self, items_to_display):
        row_count = self.remove_item_table.rowCount()
        self.remove_item_table.insertRow(row_count)
        
        for item in range(3):
            temp = QTableWidgetItem(items_to_display[item])
            temp.setTextAlignment(Qt.AlignCenter)
            temp.setForeground(QBrush(QColor(self.removal_color_list[item])))
            self.remove_item_table.setItem(row_count, item, temp)
            self.remove_item_table.resizeRowToContents(row_count)
            self.remove_item_table.scrollToBottom()
    
    def clear_all_add_item_fields(self):
        
        for items in range(len(self.add_item_list)):
            self.add_item_list[items].clear()
            
    def clear_recent_entry_table(self):
        self.database_entry_table.clearContents()
        self.database_entry_table.setRowCount(0)
        
    def clear_deleted_item_table(self):
        self.remove_item_table.clearContents()
        self.remove_item_table.setRowCount(0)
    
    def clear_isbn_search_input_box(self):
        self.isbn_search_input_box.setText('')
        
if __name__ == '__main__':
    app = QApplication([])
    win = ControlGui()
    
    app.exec_()