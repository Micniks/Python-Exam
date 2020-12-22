import matplotlib.pyplot as plt
import bs4
import requests
import urllib.request
import re
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

 
class Webscraber:
    
    def webcrawling_using_selenium_soup(search_param):
        url = 'https://roll20.net/compendium/dnd5e/BookIndex/'
        errMsg = ""
        text = ""
        print("Starting up...")

        #Setting up the driver & getting the url 
        try:        
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0")
            options = Options()
            options.headless = True

            browser = webdriver.Firefox(options=options)
            browser.get(url)
            print("Got Browser")

        except Exception as err:
            print('Error related to Browser-Setup', err)
            errMsg = 'Error related to Browser-Setup'

        #Find the search-bar and send input-text (keys) 'Fireball'
        try:
            if (len(errMsg) <= 0):
                search_box = browser.find_element_by_id('homesearch')
                search_box.send_keys(search_param)
                search_box.send_keys(Keys.RETURN)
        except Exception as err:
            print('Error related to search-field', err)
            errMsg = 'Error related to search-field'

        #Click the search-button     
        try:
            if (len(errMsg) <= 0):
                #Click the search button
                button = browser.find_element_by_id('homesearchbutton')
                button.click()
                browser.implicitly_wait(5)
        except Exception as err:
            print('Error related to button-click', err)
            errMsg = 'Error related to button-click'

        # find the folder we want to extract data from and click to enter it  
        try:
            if (len(errMsg) <= 0):
                folder = browser.find_element_by_link_text(search_param)
                folder.click()
                browser.implicitly_wait(5)
        except Exception as err:
            print('Error related to folder-search', err)
            errMsg = 'Error related to folder-search'

        # Find and specify the data we want to extract.. print it
        try:
            if (len(errMsg) <= 0):
                #Extract data
                soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
                extract_data = soup.find("div", {"id": "pagecontent"})
                text = extract_data.getText()
     
        except Exception as err:
            print('Error related to extracting-data', err) 
        print(text)
        return text

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program allows you to input a string, and searches https://roll20.net/compendium/dnd5e/ for that string. Selenium is added, by using the searchbar, and selecting the right object from list, which is then returned')
    parser.add_argument('-ab','--inputparam', nargs='+', help='<Required> Please give a String value as parameter', required=True)
    args = parser.parse_args()
    input = args.inputparam
    
    if(len(input) == 1):
        try:          
            result = Webscraber.webcrawling_using_selenium_soup(str(input))
            print(result)
        except ValueError:
            print("One or more of the ability scores could not be read as a String") 
    else:
        print("The given input needs exactly 1 argument, key searchword(Str)")    
    
    