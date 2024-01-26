from gui_class import ControlGui
import json.dumps
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread




class DataHandler(QObject):
    
    recent_database_entries = pyqtSignal(list, name="Database id, ISBN")
    database_search_results = pyqtSignal(list, name= "Database search results")
    finished_method = pyqtSignal()
    
    def __init__(self, gui_window: ControlGui):
        
        self.gui = gui_window
        self.query = QThread()
        self.database_search_results.connect(self.gui.write_to_database_remove_item_table)
        
        '''
            TODO: figure out database operations
        '''
        
    def data_item_entry(self):
        #grab self.items_for_database from gui class
        pass
    
    
    def data_item_retrieval(self):
        #ask database for isbn
        pass
    
    
    @pySlot(list, name='Database Search Results')
    def _post_retrieval_results(self):
        pass