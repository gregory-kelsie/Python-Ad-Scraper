from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time

class FacebookScraper(object):
    sections = {"Games": "686977074745292"}
    def __init__(self, ad_type, latlng, radius, min_price, max_price, query):
        self.latlng = latlng
        self.radius = radius
        self.min_price = min_price
        self.max_price = max_price
        self.query = query
        self.url = "https://www.facebook.com/marketplace/toronto/search?query=" + query + "&minPrice=" + min_price + "&maxPrice=" + max_price + "&latitude=" + latlng[0] + "&longitude=" + latlng[1] + "&categoryID=" + FacebookScraper.sections[ad_type] + "&radiusKM=" + self.radius + "&vertical=C2C"
        self.driver = webdriver.Chrome()
        #self.driver.implicitly_wait(100)
        self.delay = 3 #The maximum waiting time for the browser to load the content.
        print(self.url)

    def load_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            #Wait until the id="searchform" is loaded.
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_65db")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time.")
        
    def extract_post_titles(self):
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                lastCount = lenOfPage
                time.sleep(3)
                lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True 
        """bodyElement = self.driver.find_element_by_tag_name("body")
        for i in range(1, 100):
            bodyElement.send_keys(Keys.PAGE_DOWN)
            time.sleep(.3)"""
        

        #all_post = self.driver.find_elements_by_class_name("_1oem")
        all_post = self.driver.find_elements_by_class_name("_65db")[0]
        all_post = all_post.find_elements_by_class_name("_1oem")
        post_title_list = []
        for post in all_post:
            try:
                link = post.get_attribute("href")
                postTitle = post.get_attribute("title")
                postPrice = post.find_element_by_class_name("_f3l").text
                postImage = post.find_element_by_class_name("_7ye").get_attribute("src")
                post_title_list.append({"title": postTitle, "date": "", "cost": postPrice, "img": postImage, "link": link})
            except Exception as e:
                print(e)
        return post_title_list