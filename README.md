# webscraper -- Webscraping Project - AiCore

This project focuses on developing a webscraper package for a specific website that collects and stores selected information for the user.

## Milestone 1

The website chosen for this project was Square Enix store as I am familiar with the site, the company and the video games they are affiliated with.

## Milestone 2

A Scraper class was created to access a site, click on the accept cookies button, and includes a few methods for standard navigation around a site (e.g. clicking on tabs and adding keywords to the search bar. There were some issues in accessing the "accept cookies" button in terms of checking if the button was within another frame, locating the proper Xpath and clicking on the button, but these were eventually rectified. Once the methods were added and tested, if name == "main" block was added to initialise the class only if the script was run directly.

  import selenium
  from selenium import webdriver
  from selenium.webdriver import Chrome
  from webdriver_manager.chrome import ChromeDriverManager #installs Chrome webdriver
  from selenium.webdriver.common.by import By
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC
  from selenium.common.exceptions import TimeoutException, NoSuchElementException
  
    class Scraper:
          try:
            self.driver = Chrome(ChromeDriverManager().install()) #create driver
            self.driver.get(url)
            #driver = Chrome() #specify location of chromedriver if downloading webdriver
            print("Webpage loaded successfully")
            
        except NoSuchElementException:
            print("Webpage not loaded - please check")
    
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
        
    if __name__ == "__main__": #will only run methods below if script is run directly
    scraper = Scraper() #call scraper class
    scraper.accept_cookies()
        
## Milestone 3

This milestone was quite complex yet interesting. Whilst it was relatively straightforward to iterate through the specified number of links, issues arose and were resolved (partially if not fully) when it came to scraping specific data from each page, such as the product name, price, description and images. The first and last pieces of data seem to have a lower success rate in being scraped, as they were dependent on the size of the window the webpage was in (which could have an effect on the xpath copied as found in a demo), although the xpaths remained the same for these regardless of size. Nevertheless, a maximize_window() method was added to the class to automatically maximised the window to resolve the issue with scraping the product name for the example.

The data was easily stored in their respective dictionaries, but there were a few issues encountered when it came to writing up code to create a new folder and data dumping in the required json file that also needed to be created in the new folder. The first part was relatively simple, but to create the file in the desired folder required another line or two of code before this worked (the same applied with adding any downloaded images to the desired folder), otherwise the file was created in the current working directory instead. For the images, the code was amended so that any images downloaded at an earlier part in the script were simply moved to the desired folder.

Additional code was also required to be able to dump the UUID numbers into the json file. Fortunately the code was readily available on StackOverflow, so it was copied and pasted in.

The code was reviewed and modified where possible, before the Scraper class was moved to a .py file and imported into the newly created .ipynb (original script has been retained just in case older code is required).

## Milestone 4

This milestone was comprised of documenting and testing the webscraper to help understand what each method in the Scraper class was for, their parameters and what would be returned, and to test each method in a separate script to ensure everything was working properly.

Documenting was relatively simple, but the difficulty experienced during this milestone came from unit testing; given that each method was essentially being tested anyway in the relevant script(s), it was hard to understand why testing would also be required, otherwise it was quite straightforward to create tests for the public methods to check they were working properly.

Although all the tests are passing, they can be improved in some parts.

The Scraper class was also modified to include the method that would add links to a list (to be iterated through in the webpage (Square Enix) script); this was a sensible step to take given links would be accessed for any website from which data would be scraped, thereby completely separating all the generic methods from the custom methods.

## Milestone 5

This milestone required retrieving previously saved data and uploading it to an s3 bucket and sql databse. Because only half of the data was stored in a json file (product data only) at this point, it was necessary to scrape the data again in order to save the image data into a separate json file, otherwise the images would be linked to the wrong product when trying to retrieve them from the images folder. Whilst scraping this data again, the naming conventions in the dictionaries were edited so that the pandas dataframes containing the product and image data could be merged and uploaded into a single sql table. It was easier to merge the data at this stage rather than when they were uploaded into sql tables.

In addition, parts of webscraper.py and Square_Enix.ipynb needed amending in order to accommodate for other methods for a more robust scraping process, such as implementing a method which would keep scrolling through the results page until the end so more products could be cycled through, adding if statements to pass any product pages which required the user to input their date of birth as some data could not be scraped properly if not at all (e.g. product image and price), and locating and amending the relevant xpath for the image link on the product page. A lot of testing was needed to see if some methods needed to be in their own cells in the latter script for example, so some backtracking was required before the milestone could be completed.

Further methods were implemented so that some data could be scraped just from the results page, particularly if the boto3_upload.ipynb script was only being used. Moreover, a couple more test methods were added to test_scraper.py to ensure the correct data/xpath was being looked at on the results page.

Once this was all implemented and tested, any sensitive data was stored locally before pushing to the repository.

This milestone was quite time consuming, but the time was worth the results achieved at each stage. A lot was learned in the process, and the steps taken ensure a lot of time is saved when scraping.

## Milestone 6

This milestone was relatively straightforward as I needed to ensure the scraper and tests ran without issues and/or stopping, and avoid any duplicate images and data being collected and stored. As I was already sorting out the scraper in Milestone 5 due to some difficulties in obtaining the product image links, this milestone could be completed alongside other tasks.

In addition, whenever the scraper was run, any previous data was overwritten which was reassuring to know since this meant there would be no duplicate data. But as a precaution, a couple of methods were implemented which would check whether any duplicate links were collected to and, if so, removed from the list before gathering additional product data.

## Milestone 7

This milestone was an introduction to Docker once the code was refactored and tests were all passing; as with Milestone 6, the latter tasks were easily completed whilst improving code in Milestone 5.

In terms of Docker, this was an interesting new software which runs similar to GitHub in that files are stored locally and pushed to a remote repository, with a major difference being that the files would be stored as images instead. Whilst the process was straightforward, there were some difficulties in ensuring the script was running properly and all the modules were included in requirements.txt for example. But once this was resolved, the next objective was being able to recall the commands required to push the docker image to a remote repository which sometimes lead to multiple containers being created (and later removed).

Regardless, this was an enjoyable yet challenging milestone which allowed me to learn about Docker and Cloud technology.

## Milestone 8

This milestone focused on monitoring the scraper via a Prometheus container, hardware metrics and Docker container, thus requiring Docker and the EC2 instance to be linked to Prometheus and Prometheus being linked to Grafana. 

It was important that the files were created in their correct locations to avoid any errors, particularly when linking Docker and EC2 instance to Prometheus, something which I realised when the daemon.json file was not located in the correct path despite all the code within the file being correct.

Once resolved, it was a straightforward procedure to link Prometheus to Grafana and monitor the metrics.

A relatively simple milestone to complete, but not without its issues which could have been easily avoided the first time around.
