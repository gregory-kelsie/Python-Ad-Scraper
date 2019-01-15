from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class CoordScraper(object):
    def __init__(self, postal_code):
        self.url = "https://www.google.ca/search?rlz=1C5CHFA_enCA775CA775&ei=VekGXOK0Cse45gLOx6DAAQ&q=" + postal_code + "+lat+long&oq=" + postal_code + "+lat+long&gs_l=psy-ab.3...2123.2123..2329...0.0..0.86.86.1......0....1..gws-wiz.......0i71.ik7i-fKncHs"
        self.driver = webdriver.Chrome()
        self.delay = 3 #The maximum waiting time for the browser to load the content.
    
    
    def load_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            #Wait until the id="searchform" is loaded.
            wait.until(EC.presence_of_element_located((By.ID, "search")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time.")
            
    def quit(self):
        self.driver.quit()

    def get_coords(self):
        try:
            coords = self.driver.find_element_by_class_name("Z0LcW").text
            coords = coords.split(",")
            lat = coords[0]
            lon = coords[1]
            if (lat[-1] == "N"):
                lat = lat[:-3]
            else:
                lat = "-" + lat[:-3]
            if (lon[-1] == "W"):
                lon = "-" + lon[1:-3]
            else:
                lon = lon[:-3]
            return [lat, lon]
        except:
            return None
