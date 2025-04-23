# The parsing module for the project

#import time
#from bs4 import BeautifulSoup

import scraping

# Source url
url = "https://anilib.me/ru/catalog"

def main():

    # For some reason shitty ass weebs reply with code 403 
    # if requests module is used, even with headers.
    # But selenium worked so fuck them 

    scraped_links = scraping.scrape(url=url)

    # test title metadata scraping
    print(f"scraped title: {scraping.scrapeTitle(url=scraped_links[0])}")

# Entry point
if __name__ == "__main__":
    main()