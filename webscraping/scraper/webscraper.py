'''
This is a docstring for the module
'''
import os, os.path, shutil
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager #installs Chrome webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from typing import Optional
import time
import boto3
from sqlalchemy import create_engine
import urllib.request
from tqdm import tqdm
from pathlib import Path
import tempfile
import uuid #universally unique id
from uuid import UUID
import json
from json import JSONEncoder

class Scraper:
    '''
    This class is a scraper that can be used to browse different websites

    Parameters:
    url: str
        Link we want to visit
    --------------
    Attributes:
    driver:
        Webdriver object

    '''

    #load webpage in initialiser
    def __init__(self, url: str = "https://store.eu.square-enix-games.com/en_GB/", headless = True):  
        

        #to enter credentials, use '-it' between run and filename in terminal
        DATABASE_TYPE = input("Enter Database Type: ")
        DBAPI = input("Enter DBAPI: ") #database API - API to connect Python with database
        #use AWS details to connect database - saved in Environment Variables
        HOST = input("Enter endpoint: ") #endpoint
        USER = input("Enter your username: ") #username
        PASSWORD = input("Enter your password: ")
        DATABASE = input("Enter Database: ")
        PORT = input("Enter port: ")
        
        self.client = boto3.client('s3')
        
        #self.bucket = os.environ.get('DB_BUCKET')

        '''DATABASE_TYPE = os.environ.get('DB_DATABASE_TYPE')
        DBAPI = os.environ.get('DB_DBAPI') #database API - API to connect Python with database
        #use AWS details to connect database - saved in Environment Variables
        HOST = os.environ.get('DB_HOST') #endpoint
        USER = os.environ.get('DB_USER') #username
        PASSWORD = os.environ.get('DB_PASS')
        DATABASE = os.environ.get('DB_DATABASE')
        PORT = os.environ.get('DB_PORT')'''

        self.engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
        
        #have user add aws credentials without accidentally sharing
        self.key_id = input("Enter your AWS key id: ")
        self.secret_key = input("Enter your AWS secret key: ")
        self.bucket = input("Enter your bucket name: ")
        self.region = input("Enter your region: ")
        self.client = boto3.client('s3', 
            aws_access_key_id = self.key_id,
            aws_secret_access_key = self.secret_key,
            region_name = self.region)
        
        options = ChromeOptions()
        #add arguments before creating driver
        options.add_argument("--no-sandbox") 
        #options.binary_location = '/usr/bin/google-chrome'
        options.add_argument("--headless")
                
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox") 
        options.add_argument("--remote-debugging-port=9222") 
                
        options.add_argument("start-maximized")
        options.add_argument('--disable-gpu')
                
        options.add_argument("window-size=1920,1080") 

        #self.driver = Chrome(ChromeDriverManager().install(), options=options) #create driver
        #self.driver = Chrome(ChromeDriverManager().install())
        try:
            if headless:
                options.add_argument("--headless")
                self.driver = Chrome(ChromeDriverManager().install(), options=options) #create driver
                
            else:
                self.driver = Chrome(ChromeDriverManager().install()) #create driver
            self.driver.get(url)
            #driver = Chrome() #specify location of chromedriver if downloading webdriver
            print("Webpage loaded successfully")
        except NoSuchElementException:
            print("Webpage not loaded - please check")

        self.driver.maximize_window() #maximise window upon loading webpage
        
        #self.client = boto3.client('s3')
        #self.bucket = os.environ.get('DB_BUCKET')
        #self.bucket = input("Enter bucket name: ")

    #click accept cookies button on webpage
    def accept_cookies(self, xpath: str = '//*[@id="onetrust-accept-btn-handler"]'): 
        '''
        Looks for and clicks on the accept cookies button

        Parameters:
        ---------
        xpath: str
            The xpath of the accept cookies button

        '''
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            time.sleep(5)
            self.driver.find_element(By.XPATH, xpath).click()
            print("'Accept Cookies' button clicked")
        except TimeoutException: #if accept button is not found after 10 seconds by driver
            print("No cookies found") 
        
        return None

    #access and type in search bar
    def search_bar(self, text, xpath: str = './/a[@id="search-button"]', 
                    xpath1: str = '//*[@id="search-form-wrapper"]/form/div/input',
                    xpath2: str = './/button[@class="btn search-button-submit"]'): 
        
        '''
        Look for and write something in search bar

        Parameters
        ----------
        xpath: str
            xpath for the search button - opens search bar

        xpath1: str
            xpath for search bar - allows keywords to be be input
        
        xpath2: str
            xpath for search button to submit keywords - forward to result page

        text: str
            text to be passed to search bar

        '''
        #click on search bar icon
        try:
            time.sleep(1)
            (WebDriverWait(self.driver, 5)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            self.driver.find_element(By.XPATH, xpath).click()
            print("Search bar opened")
        except TimeoutException:
            print("Search bar not found")
        
        #open search bar
        try:
            time.sleep(1)
            (WebDriverWait(self.driver, 5)
                .until(EC.presence_of_element_located((By.XPATH, xpath1))))
            time.sleep(2)
            self.driver.find_element(By.XPATH, xpath1).click()
        except TimeoutException:
            print("Search bar not found - input")
        
        #input keywords to search
        try:
            self.text = text
            self.search = self.driver.find_element(By.XPATH, xpath1)
            self.search.send_keys(self.text)
            print(f"Search keywords entered - '{self.text}'")
            time.sleep(2)
        except NoSuchElementException:
            print("Cannot input keywords")
        
        #submit input
        try:
            self.search = self.driver.find_element(By.XPATH, xpath2).click()
            print(f"Submit search button clicked - redirected to results for {self.text}")
            time.sleep(2)
        except NoSuchElementException:
            print("Cannot submit search")

        return self.text, self.driver.find_element(By.XPATH, '//span[@class="counter-number"]').text, "products in this category"
        
    #navigate tabs - change id for games, merchandise or preorders
    def navigate(self, xpath: str = '//*[@id="merchandise"]'): 
        '''
        This is to navigate the site using the navigation bar

        Parameters
        -------------
        xpath: str
            xpath to identify desired tab on navigation bar
        '''
        
        self.tab_select = self.driver.find_element(By.XPATH,xpath)
        time.sleep(2)
        self.tab_select.click()
        time.sleep(2)

        return None
     

    
    def find_container(self, xpath: str = '//div[@class="catalogue row"]'):
        '''
        This is to find the container with the search results so the links can be accessed 
        for data scraping

        Parameters
        -------
        xpath: str
            locate the results container
        '''
        
        #### Following code block will only scroll through results page once if there is another method being called in same cell of Jupyter Notebook ####
        SCROLL_PAUSE_TIME = 3

            # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
                # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
              
            if new_height == last_height:
                break  
            last_height = new_height
        print('Loading products...')
        return self.driver.find_element(By.XPATH, xpath) #align with while loop to ensure scrolling through whole page 
    
    def collect_page_links(self, xpath : str = ".//a"):

        '''
        This is to find links in the search results container 
        Parameters
        -------
        xpath: str
            locate the links in the results container which will be stored in self.link_list
        '''
        self.container = self.find_container()
        #find many elements that correspond with the XPath - they have to be direct children of the container
        #i.e. one level below the container
        time.sleep(5)
        self.list_products = self.container.find_elements(By.XPATH, xpath)
        self.link_list = []
        #display progress bar whilst collecting page links
        for i, product in enumerate(tqdm(self.list_products, desc = 'Collecting page links: ')):
        #for product in self.list_products: #iterate through each product
            #print(product.text) #print each product in text format
            self.link_list.append(product.get_attribute("href"))
        
        return self.link_list
    
    def check_duplicates(self):
        '''
        This is to check whether any duplicate links are in self.link_list 
        by adding elements one by one to list and while adding check if it is duplicated or not
        '''
        self.select_list = self.link_list
        setOfElems = set()
        for elem in self.link_list:
            if elem in setOfElems:
                return True
            else:
                setOfElems.add(elem)         
        return False
    
    def check_duplicates1(self):
        '''
        This is to confirm whether there are any duplicates and, if so, remove the duplicates and update the list accordingly
        '''
        print("Checking for duplicate links")
        self.result = self.check_duplicates()
        if self.result:
            print('Yes, list contains duplicates')
            '''
            create dictionary from list then remove any duplicates before converting back into list 
            - order retained
            '''
            self.link_list = list(dict.fromkeys(self.link_list))
            print("Duplicates removed")
        else:
            print('No duplicates found in list')

        return self.link_list
    
    def get_product_info(self, xpath1 : str = '//h3[@class="product-title"]', 
                        xpath2 : str = '//span[@class="price"]', xpath3 : str = './/img', 
                        xpath4 : str = './/a'):

        self.container = self.find_container()
        self.product_dict = {"product_link": [], "product_name": [], "price": [], "product_id": [], "product_uuid": []}

        self.product_name = self.container.find_elements(By.XPATH, xpath1)
        self.product_price = self.container.find_elements(By.XPATH, xpath2)
        self.image_link = self.container.find_elements(By.XPATH, xpath3)
        self.image_list = []
        
        self.product_link = self.container.find_elements(By.XPATH, xpath4)
        self.link_list = []

        #display progress bar whilst collecting product info
        for i, link in enumerate(tqdm(self.product_link, desc = 'Collecting page links: ')):
            product_link = link.get_attribute("href")
            self.link_list.append(product_link)
            self.product_dict["product_link"].append(product_link)
            self.z = product_link.rsplit("/", 6)
            self.product_dict["product_id"].append(self.z[5])

        for i, product in enumerate(tqdm(self.product_name, desc = 'Collecting product names: ')): 
            self.product_uuid = uuid.uuid4()
            self.product_dict["product_name"].append(product.text) 
            self.product_dict["product_uuid"].append(self.product_uuid)

        for i, price in enumerate(tqdm(self.product_price, desc = 'Collecting product prices: ')):
            self.product_dict["price"].append(price.text) 
            
        return self.product_dict
    
    def download_product_info(self): #save product_dict in json file and upload to s3 bucket
       product_file = f"se_product_data_{self.text}"
       create_file = os.path.join(product_file+".json") #add file type here

       try:
            with open(create_file, "w") as fp: #specify path here - create data.json file
                    #Dealing with no UUID serialization support in json
                    JSONEncoder_olddefault = JSONEncoder.default
                    def JSONEncoder_newdefault(self, o):
                            if isinstance(o, UUID): return str(o)
                            return JSONEncoder_olddefault(self, o)
                    JSONEncoder.default = JSONEncoder_newdefault
                    
                    json.dump(self.product_dict, fp,  indent=4)
                    self.client.upload_file(f"se_product_data_{self.text}.json", self.bucket, f"se_product_data_{self.text}.json") #json file will be added to bucket
            #time.sleep(3)
            #os.remove(create_file) #remove json file from cwd once uploaded to s3 bucket
       except RuntimeError:
            print("Not supported - file not uploaded to bucket")
       
       return f"Data uploaded to {self.bucket} as json file"
    
    def get_images(self, 
                    xpath : str = '//figure[@class="product-boxshot-container"]', 
                    xpath2 : str = 'figure[@class="product-boxshot-container hover-boxshot"]'):
        '''
        This is to find the product images in the search results container 
        Parameters
        -------
        xpath: str
            locate the images in the results container and their respective links from srcset
        '''
        self.image_link = self.container.find_elements(By.XPATH, './/img')
        self.src_list = []
        #display progress bar whilst collecting images
        for i, link in enumerate(tqdm(self.image_link, desc = 'Collecting image links: ')):
            y = link.get_attribute('srcset')
            s = y.split("1x")

            if ".jpg" not in s[0]:
                    pass
            else:
                self.src_list.append(s[0]) #obtain image from 1st link only
        return self.src_list
    
    def download_images(self):
        #folder = input("Enter folder name: ")
       path = f"scraper_image_data_{self.text}"
       #self.client.put_object(Bucket=self.bucket, Key=(path+'/'))
       for i, scr in enumerate(tqdm(self.src_list, desc = "Downloading images")):  
            scr = f"{self.text}_image_{i}.png"
                
            if ".jpg" not in self.src_list[i]:
                    pass
            else: 
                    urllib.request.urlretrieve(self.src_list[i], scr)
                    self.client.upload_file(scr, self.bucket, f'{path}/{scr}')
                    #time.sleep(1)
                    #os.remove(scr) #remove images from cwd once uploaded to s3 bucket
       if self.src_list is None:
                print("No images found - please run get_images() first")
                return None
    

if __name__ == "__main__": #will only run methods below if script is run directly
    scraper = Scraper() #call scraper class
    scraper.accept_cookies()
    scraper.navigate()
    scraper.search_bar(input("Enter search keywords: ")) #input or add search keyword here
    scraper.find_container()
    #scraper.collect_page_links()
    scraper.get_product_info()
    scraper.download_product_info()
    #scraper.check_duplicates1()
    scraper.get_images()
    scraper.download_images()