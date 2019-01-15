from CraigsListScraper import CraigsListScraper
from KijijiScraper import KijijiScraper
from FacebookScraper import FacebookScraper
from LetsGoScraper import LetGoScraper
from bs4 import BeautifulSoup
import urllib.request
from CoordScrape import CoordScraper


def manual_scrape():
    ad_type = input("Ad Type (Games, Cars etc): ")
    search_radius = input("Radius: ")
    postal_code = input("Postal Code: ")
    postal_code = postal_code.replace(" ", "")
    min_price = input("Min Price: ")
    max_price = input("Max Price: ")
    query = input("Search: ")

    if (min_price >= 0 and min_price <= max_price):
        results = scrape_craigslist("Toronto", "Toronto", ad_type, search_radius, postal_code, min_price, max_price, query)
        results = results + scrape_kijiji("Toronto", "Toronto", ad_type, search_radius, postal_code, min_price, max_price, query)
        create_html(results)   
    else:
        print("Min PRICE ERROR")   

def automatic_scrape():
    ad_type = "Games"
    search_radius = "50"
    postal_code = "m1k5k1"
    min_price = "15"
    max_price = "70"
    query = "valkyria"

    results = scrape_craigslist("Toronto", "Toronto", ad_type, search_radius, postal_code, min_price, max_price, query)
    results = results + scrape_kijiji("Toronto", "Toronto", ad_type, search_radius, postal_code, min_price, max_price, query)
    results = results + scrape_facebook(ad_type, search_radius, postal_code, min_price, max_price, query)
    create_html(results)

def scrape_facebook(ad_type, search_distance, postal, min_price, max_price, query):
    coords = CoordScraper(postal)
    coords.load_url()
    latlng =  coords.get_coords()
    coords.quit()
    scraper = FacebookScraper(ad_type, latlng, search_distance, min_price, max_price, query)
    scraper.load_url() 
    return scraper.extract_post_titles()
    """
    facebook_results = scraper.extract_post_titles()
    scraper.quit()
    return facebook_results
    """


def scrape_craigslist(city, region, section, search_distance, postal, min_price, max_price, query):
    scraper = CraigsListScraper(city, region, section, search_distance, postal, min_price, max_price, query)
    scraper.load_url()
    resultList = scraper.extract_post_titles()
    scraper.quit()
    return resultList

def scrape_kijiji(city, region, section, search_distance, postal, min_price, max_price, query):
    kijiji_scraper = KijijiScraper(city, region, section, search_distance, postal, min_price, max_price, query)
    return kijiji_scraper.extract_post_urls()

def create_html(scrape_results):
    f = open("results.html", "w")
    heading = "<!DOCTYPE html><html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"><title>Python Scraper Results</title></head><body>"
    f.write(heading)
    message = "<h1>Scraper Results</h1><table><tr><th>Thumbnail</th><th>Price</th><th>Date</th><th>Listing</th></tr>"
    f.write(message)
    for element in scrape_results:
        row = "<tr>"
        row += "<td><img src=\"" + element["img"] + "\" width=100 height=100/></td>"  
        row += "<td>" + element["cost"] + "</td>"
        row += "<td>" + element["date"] + "</td>"
        row += "<td><a href=\"" + element["link"] + "\">" + element["title"] + "</a></td>"
        row += "</tr>"
        f.write(row)
    closing = "</table></body></html>"
    f.write(closing)
    f.close()

if __name__ == "__main__":
    """ Either call manual_scrape or automatic_scrape based on your preferences """
    #automatic_scrape()
    #create_html(scrape_facebook("Games", "100", "n0r1k0", "20", "70", "switch"))
    #create_html(scrape_facebook("Games", "100", "m1k5k1", "20", "70", "wii"))
    scraper = LetGoScraper("Games", "m1k5k1", "50", "20", "70", "Valkyria")
    scraper.load_url()
    scraper.extract_post_titles()


    
    
