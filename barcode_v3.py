import sys  
import requests 
import json
import time 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#import chromedriver_binary
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from database_handler import DataHandler
from gui_class import ControlGui
from time import sleep

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
                            "Title": '',
                            'Author': '',
                            'Genre' : '',
                            'ISBN' : '',
                            'Publisher': ''
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
        print(f'Inside barcode lookup')
        lookupkey = self.apiKey + self.barcode_string
        
        resp = requests.get(lookupkey, self.headers)
        data = json.loads(resp.text)
        
       
        for offer in data['items'][0]['offers']: # I want to get 5 different titles from the offer section
            if (len(self.titleEntry) < 5) & (offer["title"].title() not in self.titleEntry):
                self.titleEntry.append(offer["title"].title())
                
        self._getAuthor()
        
        self.book_info['Title'] = data['items'][0]['title']
        self.book_info['Genre']= data['items'][0]['category']
        self.book_info['ISBN'] = data['items'][0]['isbn']
        self.book_info['Publisher'] = data['items'][0]['publisher']
        self._barcode_display_list()
        
                
    pyqtSlot(list, name="barcode results list")           
    def _barcode_display_list(self):
        #TODO: update when publisheer and edition is ready
        display_list = []
        place_holder = 'NULL'
        display_list.append(self.book_info['Title'])
        display_list.append(self.book_info['Author'])
        display_list.append(place_holder)
        display_list.append(place_holder)
        
        print(f'inside barcode display list {display_list}')
        
        self.search_results.emit(display_list)
        self.finished_method.emit()
            
    
    def _getAuthor(self):

        
        url = "https://ocls.info/books-movies-more/books-magazines/"
        #f_options is firefox options for the driver
        
        #driver = Service('usr/lib/chromium-browser/chromedriver') Raspberry pi
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        print ("Headless Firefox Initialized")

        # this is just to ensure that the page is loaded
        time.sleep(2)        
        search_box = driver.find_element(By.NAME, "searcharg")
        search_box.send_keys(min(self.titleEntry, key=len))
        search_box.submit()
        time.sleep(3)  

        # renders JS code and stores all info in static HTML code. 
        html = driver.page_source 

        # Now, we could simply apply bs4 to html tag
        soup = BeautifulSoup(html, "html.parser") 

        #use the autho info text to get the first and last name using a comma as a delimiter
        authorInfo = soup.find('div', {'class' : 'briefcitAuthor'}).text.strip()
        authorLast = authorInfo[ : authorInfo.find(',')]
        authorFirst = authorInfo[authorInfo.find(',')+2 : authorInfo.find(',', authorInfo.find(',')+1)].strip()        
        author = f"{authorFirst} {authorLast}"
        
        self.book_info['Author'] = author
        print(f'Value of author inside getAuthor {author}')
        driver.close()   
    
        
    @pyqtSlot(str, name="Scanned barcode")
    def check_barcode(self, barcode):
        print(f'inside barcode api, passed string {barcode}')
        if self.barcode_string == barcode:
            return
        elif barcode:
            self.barcode_string = barcode
            self.barcode_lookup()
        
        else:
            return
    
    def main_function(self):
        
        return
        
     
        
    
    