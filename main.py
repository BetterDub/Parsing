# The parsing module for the project

#import time
#from bs4 import BeautifulSoup

import scraping
import dbhandler

# Source url
url = "https://anilib.me/ru/catalog"

# PARAMETERS FOR DB CONNECTION, DON'T FORGET TO SET TO CUSTOM
conn_options = {
    "DB_NAME" : "betterdub", # should be manually created, 
        # autocommit doesn't let to do it from here
    "DB_USER" : "postgres",
    "DB_PASSWORD" : "----", # CYKA NE ZABUD POMENYAT
    "DB_HOST" : "localhost",
    "DB_PORT" : "5432"
}

def main():

    # For some reason shitty ass weebs reply with code 403 
    # if requests module is used, even with headers.
    # But selenium worked so fuck them 

    # scraped_links = scraping.scrape(url=url) # works

    # test title metadata scraping
    # print(f"scraped title: {scraping.scrapeTitle(url=scraped_links[0])}") # works

    handler = dbhandler.DBHandler(options=conn_options)
    handler.liveMode()

    # test the handler

    # handler.executeQuery("""
    #     DROP TABLE IF EXISTS test;

    #     CREATE TABLE test(
    #         id INT PRIMARY KEY,
    #         info TEXT
    #     );
                         
    #     INSERT INTO test (id, info)
    #     VALUES
    #         (1, 'first'),
    #         (10, 'tenth');
                         
    #     SELECT * FROM test;
    # """)
    # print(handler.fetch())

    # works

# Entry point
if __name__ == "__main__":
    main()