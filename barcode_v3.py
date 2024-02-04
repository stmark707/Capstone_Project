import requests 
import json
from bs4 import BeautifulSoup 
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from database_handler import DataHandler
from gui_class import ControlGui


#This is the class that will be used to create the object
# TO DO - change the title, auth, genre, etc to something more generic, so as to be able to be a BOOK or ITEM  

class BarcodeIntake(QObject):
    
    search_results = pyqtSignal(list, name="barcode results list")
    book_stats = pyqtSignal(object, name="Full book info")
    finished_method = pyqtSignal()
    
    def __init__(self, gui_window:ControlGui, data_handler:DataHandler):
        super().__init__()
        self.gui = gui_window
        self.barcode_string = ""
        
        self.book_info = {
                            'TITLE': '',
                            'AUTHOR': '',
                            'GENRE' : '',
                            'ISBN' : '',
                            'PUBLISHER DATE': '',
                            'EDITION': '',
                            'PUBLISHER': ''
                        }
        self.titleEntry = []
        self.headers = {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Accept-Encoding': 'gzip,deflate'
                        }
        
        self.search_results.connect(self.gui.write_to_barcode_search_table)
        self.book_stats.connect(self.gui.book_information_transfer)
        
        self.apiKey = 'https://api.upcitemdb.com/prod/trial/lookup?upc='
        
                   
    def barcode_lookup(self):
        '''
            TODO: Get publisher or publishing date
            TODO: Get book edition
        '''
        lookupkey = self.apiKey + self.barcode_string
        
        resp = requests.get(lookupkey, self.headers)
        data = json.loads(resp.text)
        
                 
        self._getAuthor()
        
        try:
            for offer in data['items'][0]['offers']: # I want to get 5 different titles from the offer section And does not contain the word By or by 
                if (len(self.titleEntry) < 5) & (offer["title"].title() not in self.titleEntry) & (f'{self.book_info["AUTHOR"]}' not in offer["title"].title()):
                    self.titleEntry.append(offer["title"].title())
                    
        except:
            print('Error in barcode lookup')
            return
                
        title = (max(self.titleEntry, key=len))
        self.book_info['TITLE'] = title.replace(',', ' ').replace("'",'')
        
        self.book_info['ISBN'] = data['items'][0]['isbn']
        self._barcode_display_list()
        
    @pyqtSlot(object, name="Full book info")
    @pyqtSlot(list, name="barcode results list")           
    def _barcode_display_list(self):
        #TODO: update when publisheer and edition is ready
        display_list = []
        place_holder = 'NULL'
        display_list.append(self.book_info['TITLE'])
        display_list.append(self.book_info['AUTHOR'])
        display_list.append(self.book_info['GENRE'])
        display_list.append(self.book_info['PUBLISHER'])
        
       
        self.book_stats.emit(self.book_info)
        self.finished_method.emit()
        self.search_results.emit(display_list)
        self.finished_method.emit()
            
    
    def _getAuthor(self):

        
        url1 = "https://shop.harvard.com/book/"
        url2 = self.barcode_string
        url = url1 + url2        

        # grabs the html from the page 
        html = requests.get(url).text

        # Now, we could simply apply bs4 to html tag
        soup = BeautifulSoup(html, "html.parser") 

        #This gets Author, Genre, and Publisher, can also get publishing date (instead of edition)
        try:
            relatedInfo = soup.find('fieldset', {'id' : 'aba-product-details-fieldset'})
            publisher = relatedInfo.find(string='Publisher:').next_element.strip()
            pubDate = relatedInfo.find(string='Publication Date:').next_element.strip()
            
            genreLocation = soup.find('fieldset',{'class': 'collapsible abaproduct-related-editions'})
            genreInfo = genreLocation.findNext('a').text.strip()
            
            authorLocation = soup.find('div',{'class': 'author'}).text.strip()
            author = authorLocation[3:]
            
            self.book_info['AUTHOR'] = author.replace("'", '')
            self.book_info['GENRE'] = genreInfo
            self.book_info['PUBLISHER'] = publisher
            self.book_info['PUBLISHER DATE'] = pubDate
            
        except:
            print('Error in barcode lookup')            
            return        
        
        
    
        
    @pyqtSlot(str, name="Scanned barcode")
    def check_barcode(self, barcode):
        
        if self.barcode_string == barcode:
            return
        elif barcode:
            self.barcode_string = barcode
            self.barcode_lookup()
        
        else:
            return
    
    def main_function(self):        
        return
        
     
        
    
    