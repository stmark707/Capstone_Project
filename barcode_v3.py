import sys  
import requests 
import json
import time 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.firefox.options import Options

#This is the class that will be used to create the object
# TO DO - change the title, auth, genre, etc to something more generic, so as to be able to be a BOOK or ITEM  

class barcode_intake:
    def __init__(self):
        self.barcode_string = ""
        self.titleEntry = []
        self.firstEntry = ""        #title+/item name+        
        self.secondEntry = ""       #author+/manufacturer+
        self.thirdEntry = ""        #genre-/category+
        self.fourthEntry = ""       #isbn+/upc+
        self.fifthEntry = ""        #publisher+/domain

    def __str__(self): #looks weird becuase of the indentation, but it works
        return f"""Barcode: {self.barcode_string}
Title: {self.firstEntry}
Author: {self.secondEntry}
Genre: {self.thirdEntry}
ISBN: {self.fourthEntry}
Publisher: {self.fifthEntry}"""

        code = code.replace("-", "")  # Remove dashes if present

        if len(code) == 12 and code.isdigit():
            return "UPC Code"
        elif (len(code) == 10 or len(code) == 13) and (code.isdigit() or (code[:-1].isdigit() and code[-1] == 'X')):
            return "ISBN Code"
        else:
            return "Unknown Code"
                
    def barcode_lookup(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip,deflate'
        }
        
        apiKey = 'https://api.upcitemdb.com/prod/trial/lookup?upc='
        UpcItem = self.barcode_string
        lookupkey = apiKey + UpcItem
        
        resp = requests.get(lookupkey, headers=headers)
        data = json.loads(resp.text)
        
        self.firstEntry = data['items'][0]['title']
        #self.secondEntry = data['items'][0]['author']
        self.thirdEntry = data['items'][0]['category']
        self.fourthEntry = data['items'][0]['isbn']
        self.fifthEntry = data['items'][0]['publisher']
        
        for offer in data['items'][0]['offers']: # I want to get 5 different titles from the offer section
            if (len(self.titleEntry) < 5) & (offer["title"].title() not in self.titleEntry):
                self.titleEntry.append(offer["title"].title())

        #next I want to get the missing info, like author from the a public library using the titles I got from the offers section
        #okay then maybe I can let the user choose which title they want to use,
        #and while they're choosing, I can get the other info from the web scraping
        #then I can use the user selection to be the title.
            
        thislist = [self.firstEntry, 
                    self.secondEntry, 
                    self.thirdEntry, 
                    self.fourthEntry, 
                    self.fifthEntry]
        
        print("Title Suggestions:" + self.titleEntry.__str__())
        
        # return thislist
    
    def getAuthor(self):

        url = "https://ocls.info/books-movies-more/books-magazines/"
        #f_options is firefox options for the driver
        f_options = Options()
        f_options.add_argument("--headless")
        driver = webdriver.Firefox(options=f_options)
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
        
        driver.close()
        self.secondEntry = author    
    
    def printInfo(barcode_intake):
    
        print(barcode_intake)
        
    #clear data from object and set barcode to argument
    def setBarcode(self, barcodeString):
        self.barcode_string = barcodeString
        #check if the barcode is valid is in the data base
    
    #temporary function to get the barcode from the user(while get barcode from other source)
def read_barcode():
    barcode = ""
    print("Scan a barcode (terminate with Enter key):")

    while True:
        try:
            char = sys.stdin.read(1)
            if char == '\n':
                break
            barcode += char
        except KeyboardInterrupt:
            break

    return barcode

scan = barcode_intake()

scan.setBarcode(read_barcode())

scan.barcode_lookup()
scan.getAuthor()
scan.printInfo()
