from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

class LetGoScraper(object):
    def __init__(self, ad_type, postal_code, radius, min_price, max_price, query):
        if (postal_code[3] != " "):
            self.postal_code = postal_code[:3] + " " + postal_code[3:]
        else:
            self.postal_code = postal_code
        self.radius = radius
        self.min_price = min_price
        self.max_price = max_price
        self.query = query
        self.url = "https://ca.letgo.com/en"
        self.driver = webdriver.Chrome()
        #self.driver.implicitly_wait(100)
        self.delay = 3 #The maximum waiting time for the browser to load the content.
        print(self.url)
        
    def load_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            #Wait until the id="searchform" is loaded.
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "locationLabel")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time.")

    def extract_post_titles(self):
        self.set_location()
        self.set_price_range()
        post_title_list = []

    def set_location(self):
        locationButton = self.driver.find_element_by_class_name("locationLabel")
        locationButton.click()
        time.sleep(3)
        postalInput = self.driver.find_element_by_class_name("MapLocationFinderStyle__LocationsAutosuggestions-m7m5vd-6")
        postalInput = postalInput.find_element_by_class_name("sc-VigVT")
        postalInput = postalInput.find_element_by_class_name("sc-fBuWsC")
        postalInput = postalInput.find_element_by_class_name("input")
        postalInput.click()
        postalInput.clear()
        postalInput.send_keys(self.postal_code)
        time.sleep(3)
        postalInput.send_keys(Keys.DOWN, Keys.RETURN)
        time.sleep(3)
        set_location_btn = self.driver.find_elements_by_class_name("MapLocationFinderStyle__ControlsWrapper-m7m5vd-5")[1]
        set_location_btn = set_location_btn.find_element_by_class_name("sc-iwsKbI")
        set_location_btn.click()  
        time.sleep(3)   

    def set_price_range(self):
        priceButton = self.driver.find_element_by_class_name("activeKey")
        priceButton.click()
        time.sleep(1)
        minButton = self.driver.find_element_by_name("min")
        minButton.click()
        minButton.send_keys(self.min_price)
        maxButton = self.driver.find_element_by_name("max")
        maxButton.click()
        maxButton.send_keys(self.max_price)
        time.sleep(1)
        applyButton = self.driver.find_element_by_class_name("Filtersstyles__PriceRow-sc-1cm9xbc-0")
        applyButton = applyButton.find_elements_by_class_name("sc-iwsKbI")[1]
        applyButton.click() 