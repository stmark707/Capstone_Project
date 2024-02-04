from gui_class import ControlGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl, QJsonDocument
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from json import loads


class DataHandler(QObject):
    
    def __init__(self, gui_window: ControlGui):
        super().__init__()
        self.gui = gui_window
        self.agile_stock_website_post = 'https://agilestockweb.azurewebsites.net/api/inventoryitem' #type cast to QUrl
        self.url = QUrl()
        self.scheme = 'https'
        self.host = 'agilestockweb.azurewebsites.net'
        self.api_path = '/api/inventoryitem'
        self.api_search = '/api/inventoryitem/isbnsearch'
        self.agile_stock_get_by_isbn = ''
        self.server_request = QNetworkRequest()
        self.server_manager = QNetworkAccessManager()
        self.server_response = None
        self.data = {
                        
                        "TITLE": "",
                        "AUTHOR": "",
                        "PUBLISHER": "",
                        "PUBLISHED_DATE": "",
                        "GENRE": "" ,
                        "ISBN": "",
                        "EDITION": ""
                        
                    }
        self.database_query = {
                                "AUTHOR": "",
                                "BOOKID": "",
                                "GENRE": "",
                                "ISBN": "",
                                "PUBLISHED_DATE": "",
                                "PUBLISHER": "",
                                "TITLE": ""

                            }
        
        
        
        '''
            TODO: figure out database operations
        '''
        
    def reply_parse(self, reply):
        #print('inside reply parse')
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            #print(f'data inside reply parse {data} type{type(data)}\n')
            if data:
                print(f'\ndata in response {data} type of {type(data)} {len(data)}\n')
                self.check_response(data)
        else:
            print(reply.errorString())

    def check_response(self, response_data):
        temp_dict = loads(response_data.data().decode("utf-8"))
        
        if "errorMessage" in temp_dict:
            return
        elif "AS_BOOK" in temp_dict:
            self._internal_data_retreival()
        else:
            result_dict = temp_dict.pop()
            isbn = result_dict.get("ISBN")
            database_id = result_dict.get("BOOKID")
            database_id = str(database_id)
        
            recent_entry = [database_id, isbn]
            self.gui.write_to_database_entry_table(recent_entry)
            
            
    
    def post_request(self, data):
        self.data = data
        data = [data]
        
        self.url.setScheme(self.scheme)
        self.url.setHost(self.host)
        self.url.setPath(self.api_path)
        self.server_request.setUrl(self.url)
        
        self.server_request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')
        self.server_manager.finished.connect(self.reply_parse)
        
        formatted_data = QJsonDocument(data).toJson()
        
        self.server_manager.post(self.server_request, formatted_data)
        
        
        
    def data_item_retrieval(self):
        #ask database for isbn
        
        
        self.agile_stock_get_by_isbn = '/' + self.agile_stock_get_by_isbn
        
        self.api_search = '/api/inventoryitem/isbnsearch' + self.agile_stock_get_by_isbn
        print(self.agile_stock_get_by_isbn)
        self.url.setScheme(self.scheme)
        self.url.setHost(self.host)
        self.url.setPath(self.api_search)
        
        
        server_request = QNetworkRequest(self.url)
        self.server_manager.finished.connect(self.reply_parse)
        
        self.server_manager.get(server_request)
        
    def _internal_data_retreival(self):
    
        isbn = self.data.get('ISBN')
        isbn = '/' + isbn
        
        self.api_search = '/api/inventoryitem/isbnsearch' + isbn
       
        self.url.setScheme(self.scheme)
        self.url.setHost(self.host)
        self.url.setPath(self.api_search)
        
        
        server_request = QNetworkRequest(self.url)
        self.server_manager.finished.connect(self.reply_parse)
        
        self.server_manager.get(server_request)