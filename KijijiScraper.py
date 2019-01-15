from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request

import datetime
from datetime import timedelta

class KijijiScraper(object):
    sections = {"Games": ["b-video-games-consoles", "k0c141l1700273"], "Cars": ["b-cars-trucks", "k0c27l1700273"]}
    regions = {"Toronto": "city-of-toronto"}
    def __init__(self, city, region, section, radius, postal, min_price, max_price, query):
        self.city = city
        self.region = region
        self.query = query
        self.section = section
        self.search_distance = radius
        self.postal = postal
        self.min_price = min_price
        self.max_price = max_price
        self.url = "https://www.kijiji.ca/" + KijijiScraper.sections[section][0] + "/" + KijijiScraper.regions[region] + "/" + query + "/" + KijijiScraper.sections[section][1] + "r" + radius + ".0?&address=" + postal + "&ad=offering&price=" + min_price + "__" + max_price
        print(self.url)


    def getURL(self):
         return self.url 
    
    def extract_post_urls(self):
        post_title_list = []
        html_page = urllib.request.urlopen(self.url)
        #You don't need lxml, but it stops a bunch of warnings
        soup = BeautifulSoup(html_page, features="html5lib")
        for post in soup.findAll("div", ["regular-ad"]):
            try:
                imgURL = post.find("img")
                imgURL = imgURL["src"]
                price = post.find("div", ["price"]).string
                price = price.strip()
                title = post.find("a", ["title"]).string
                title = title.strip()
                date = post.find("span", ["date-posted"]).string
                date = date.strip()
                date = self.convert_date(date)
                link = "https://www.kijiji.ca" + post.find("a", ["title"])["href"]
                post_title_list.append({"title": title, "date": date, "cost": price, "img": imgURL, "link": link})
            except:
                pass
        nextPage = soup.findAll("span", ["prevnext-link"])
        if (nextPage):
            if (nextPage[0].string[0] == "N"):
                self.url = "https://www.kijiji.ca" + nextPage[0]["data-href"]
                return post_title_list + self.extract_post_urls()
            elif (len(nextPage) > 1 and nextPage[1].string[0] == "N"):
                self.url = "https://www.kijiji.ca" + nextPage[1]["data-href"]
                return post_title_list + self.extract_post_urls()
        return post_title_list
    
    def get_month(self, month):
        month = str(month)
        if (month == "1"):
            month = "Jan"
        elif (month == "2"):
            month = "Feb"
        elif (month == "3"):
            month = "Mar"
        elif (month == "4"):
            month = "Apr"
        elif (month == "5"):
            month = "May"
        elif (month == "6"):
            month = "Jun"
        elif (month == "7"):
            month = "Jul"
        elif (month == "8"):
            month = "Aug"
        elif (month == "9"):
            month = "Sep"
        elif (month == "10"):
            month = "Oct"
        elif (month == "11"):
            month = "Nov"
        elif (month == "12"):
            month = "Dec"
        return month

    def convert_date(self, date):
        if (date[0] == "<"):
            now = datetime.datetime.now()
            month = self.get_month(now.month)
            return month + " " + str(now.day)
        elif (date[0] == "Y"):
            now = datetime.datetime.now() - timedelta(days=1)
            month = self.get_month(now.month)
            return month + " " + str(now.day)
        else:
            date = date.split("/")
            month = self.get_month(date[1])
            return month + " " + date[0]