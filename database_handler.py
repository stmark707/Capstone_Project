from gui_class import ControlGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl, QJsonDocument
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply



class DataHandler(QObject):
    
    recent_database_entries = pyqtSignal(list, name="Database id, ISBN")
    database_search_results = pyqtSignal(list, name= "Database search results")
    finished_method = pyqtSignal()
    
    def __init__(self, gui_window: ControlGui):
        super().__init__()
        self.gui = gui_window
        self.database_search_results.connect(self.gui.write_to_database_remove_item_table)
        self.agile_stock_website_post = 'https://agilestockweb.azurewebsites.net/api/inventoryitem' #type cast to QUrl
        self.url = QUrl()
        self.scheme = 'https'
        self.host = 'agilestockweb.azurewebsites.net'
        self.api_path = '/api/inventoryitem'
        self.api_search = '/api/inventoryitem/isbnsearch'
        self.agile_stock_get_by_isbn = ''
        self.http_request = QWebEngineHttpRequest()
        self.server_request = QNetworkRequest()
        self.server_manager = QNetworkAccessManager()
        self.server_response = None
        self.data = [{
                        
                        "TITLE": "this is another test",
                        "AUTHOR": "embedded test 3",
                        "PUBLISHER": "oewifbe",
                        "PUBLISHED_DATE": "38394423",
                        "GENRE": "fan fiction",
                        "ISBN": "768445756"
                        
                    }]
        
        self.api_info = False
        
        '''
            TODO: figure out database operations
        '''
        
    def data_item_entry(self):
        self.data = self.gui.items_for_database.copy()
        self.post_request()

    
    def reply_parse(self, reply):
        print('inside reply parse')
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            print(f'data inside reply parse {data} type{type(data)}')
            if data:
                print('not empty call parse method')
            print(self.api_info)
        else:
            print(reply.errorString())

    
    def post_request(self):
        self.url.setScheme(self.scheme)
        self.url.setHost(self.host)
        self.url.setPath(self.api_path)
        self.server_request.setUrl(self.url)
        print(f'inside of post {self.url}')
        self.server_request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')
        self.server_manager.finished.connect(self._handle_reply)
        data = QJsonDocument(self.data).toJson()
        print(data)
        self.server_manager.post(self.server_request, data)
        
        
    def data_item_retrieval(self):
        #ask database for isbn
        self.api_info = True
        print('inside data item retrieval')
        self.agile_stock_get_by_isbn = '/' + self.agile_stock_get_by_isbn
        print(self.agile_stock_get_by_isbn)
        self.api_search = '/api/inventoryitem/isbnsearch' + self.agile_stock_get_by_isbn
        print(self.api_search)
        self.url.setScheme(self.scheme)
        self.url.setHost(self.host)
        self.url.setPath(self.api_search)
        print(self.url)
        
        server_request = QNetworkRequest(self.url)
        self.server_manager.finished.connect(self.reply_parse)
        
        self.server_manager.get(server_request)
        
        
    
