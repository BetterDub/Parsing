# Basic scraping for titles

import sys
import time
from tempfile import mkdtemp

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# For better scraping (time to load the page after scrolling)
SCROLL_PAUSE_TIME = 0.5

# headers = {
#     "User-Agent": (
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/122.0.0.0 Safari/537.36"
#     ),
#     "Accept-Language": "en-US,en;q=0.9",
# }

# Magic toomba-yoomba
temp_profile = mkdtemp()

# DO NOT TOUCH THIS, IMMA CUT YOUR ARMS OFF IF YOU DO
options = Options()
options.add_argument("--headless")  # Comment out to see browser
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")  # 0 = INFO, 3 = FATAL
options.add_argument(f"--user-data-dir={temp_profile}")

# Magic toomba-yoomba
service = Service(log_path='nul' if sys.platform == 'win32' else '/dev/null')

def scrape(url) -> list:

    # Initialize the browser
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )

    hrefs = []

    try:
        print(f"Opening {url}...")
        driver.get(url)

        # Wait for divs with class "card-item" to be present
        wait = WebDriverWait(driver, 10)

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Scraping titles
        cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-item"))) # Uses magic string

        for card in cards:
            try:
                link = card.find_element(By.CLASS_NAME, "card-item-caption") # Uses magic string
                hrefs.append(link.get_attribute("href"))
            except Exception:
                continue

        print("Extracted hrefs:")
        for href in hrefs:
            print(href)
        print(f"Titles scraped in total: {len(hrefs)}")

    except:
        print("Title link scraping went to shit")
        hrefs = ['error']

    driver.quit()

    return hrefs

# Just in case, this is the borked requests realization
# def scrape():

    # # Send a GET request to the URL
    # response = requests.get(url, headers=headers)

    # # Check if the request was successful
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'html.parser')
        
    #     # Find all divs with the class "card-item"
    #     card_items = soup.find_all("div", class_="card-item")

    #     # Extract hrefs from links with class "card-item-caption"
    #     hrefs = []
    #     for item in card_items:
    #         link = item.find("a", class_="card-item-caption")
    #         if link and 'href' in link.attrs:
    #             hrefs.append(link['href'])

    #     # Print or use the hrefs as needed
    #     print("Extracted hrefs:")
    #     for href in hrefs:
    #         print(href)
    # else:
    #     print(f"Failed to retrieve the page. Status code: {response.status_code}")

def scrapeTitle(url) -> dict:

    # Initialize the browser
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )

    reply = {
        'title' : '',
        'description' : ''
    }

    # magic strings, manual check is needed to monitor
    title_class = 'tb_tf'
    desc_class = 't5_bp'

    try:
        print(f"Opening {url}...")
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # Scraping metadata
        # FUCK THIS, for some reason dumb selemium threw shitzillion exceptions 
        # for 90 minutes straight, but then suddenly it stopped for no reason at all.
        # If an exception gets raised here I recommend to experiment with waiting time,
        # use different methods in EC and BY, or just straingh up pick a different div to get info from
        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, title_class)))
        desc = wait.until(EC.presence_of_element_located((By.CLASS_NAME, desc_class)))

        try:
            reply['title'] = title.text
            reply['description'] = desc.text
        except Exception:
            # If it gets here then you should manually inspect the scraping source page
            print("data extraction failed")

    except Exception as e:
        print(e)
        print("Title metadata scraping went to shit")
        reply = {"exception" : "exception"}

    driver.quit()

    return reply