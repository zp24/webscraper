import unittest
from scraper.webscraper import Scraper 

#make sure the method to be tested contains a return function
'''
Running a successful Unittest: 

1. Tell scraper to go to a target page 
2. Run method on the page 
3. Make an assertion based on what the method in the class returns

'''
class TestScraper(unittest.TestCase): #gives access to testing capabilities within class
    def setUp(self):
        self.scraper = Scraper() #navigate to url
    
    def test_searchbar(self):
        text = "kingdom hearts"
        result = self.scraper.search_bar(text)
        self.assertIn(result, 'kingdom hearts') #strings must match for test to run successfully (i.e. text must equal aearch keywords)
    
    def test_navigate(self):
        id = '//*[@id="merchandise"]'
        result = self.scraper.navigate(id)
        self.assertIsNone(result, '//*[@id="merchandise"]') #returns None

    def test_accept_cookies(self):
        cookie_id = '//*[@id="onetrust-accept-btn-handler"]'
        result = self.scraper.accept_cookies(cookie_id)
        self.assertIsNone(result, '//*[@id="onetrust-accept-btn-handler"]') #returns None
    
    def test_find_container(self):
        text = "final fantasy"
        self.scraper.search_bar(text)
        container = self.scraper.find_container()
        #//*[@id="slick-slide03"]/a
        result = container.text[0:18]
        self.assertIn(result, "FINAL FANTASY VIII - REMASTERED") #assertEqual will return FAILED test if used
    
    def test_find_links(self):
        text = "final fantasy"
        self.scraper.search_bar(text)
        self.scraper.find_container()
        link = './/a'
        result = self.scraper.collect_page_links(link)
        self.assertIn('square-enix', result[10]) #strings must match for test to run successfully
        #get_attribute("href")
    
    def test_find_images(self):
        text = "final fantasy"
        self.scraper.search_bar(text)
        container = self.scraper.find_container()
        result = self.scraper.get_images(container=container) #images are stored in a list
        
        self.assertIn('.jpg', result[5]) #find .jpg in selected image - all images in find_images are .jpg format
    
        
if __name__ == '__main__':
    unittest.main()

#python -m unittest test_scraper.py
