from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request
import html5lib

class CraigsListScraper(object):
    sections = {"Games": "vga"}
    regions = {"Toronto": "tor"}
    def __init__(self, city, region, section, radius, postal, min_price, max_price, query):
        self.city = city
        self.region = region
        self.query = query
        self.section = section
        self.search_distance = radius
        self.postal = postal
        self.min_price = min_price
        self.max_price = max_price
        self.url = "https://toronto.craigslist.ca/search/" + CraigsListScraper.regions[region] + "/" + CraigsListScraper.sections[section] + "?query=" + query + "&search_distance=" + radius + "&postal=" + postal + "&min_price=" + min_price + "&max_price=" + max_price
        self.driver = webdriver.Chrome()
        self.delay = 3 #The maximum waiting time for the browser to load the content.
        print(self.url)

    def getURL(self):
         return self.url

    def load_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            #Wait until the id="searchform" is loaded.
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time.")

    def load_url2(self, new_url):
        self.driver.get(new_url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            #Wait until the id="searchform" is loaded.
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time.")  
    
    def extract_post_titles(self):
        all_post = self.driver.find_elements_by_class_name("result-row")
        post_title_list = []
        for post in all_post:
            postImage = ""
            try:
                postImage = post.find_element_by_tag_name("img")
                postImage = postImage.get_attribute("src")
            except:
                postImage = ""
            postPrice = post.find_element_by_class_name("result-price").text
            
            postDate = post.find_element_by_tag_name("time").text
            postTitle = post.find_element_by_class_name("result-title").text
            link = post.find_element_by_class_name("hdrlnk").get_attribute("href")
            post_title_list.append({"title": postTitle, "date": postDate, "cost": postPrice, "img": postImage, "link": link})

        nextPage = self.driver.find_element_by_class_name("buttons")
        
        nextPage = nextPage.find_elements_by_class_name("next")
        if (nextPage):
            nextPage = nextPage[0]
            nextPageHref = nextPage.get_attribute("href")
            if nextPageHref == "":
                return post_title_list
            else:
                self.load_url2(nextPageHref)
                return post_title_list + self.extract_post_titles()
        return post_title_list 
    
 

    def download_image(self, image_url):
        full_path = image_url.split("/")[-1]
        urllib.request.urlretrieve(image_url, full_path)
    
    def quit(self):
        self.driver.quit()