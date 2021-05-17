from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from time import sleep

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
        options=options
    )
    return driver

def connect_to_mzgov(browser):
    base_url = 'https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19'
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            print("Connecting to MZ.GOV...")
            browser.get(base_url)
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            print("Connected to MZ.GOV!")
            return True
        except Exception:
            connection_attempts += 1
            print(f'Error connecting to {base_url}')
            print(f'Attempt #{connection_attempts}.')

    return False

def connect_to_arcgis(browser, url):
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            print("Connecting to ARCGIS...")
            browser.get(url)
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            print("Connected to ARCGIS!")
            return True
        except Exception:
            connection_attempts += 1
            print(f'Error connecting to {url}')

    return False


def parse_mz_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    iframe_blocks = soup.find_all('iframe')
    return iframe_blocks[0].get('src')

def parse_arcgis_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    iframe_blocks = soup.find_all('iframe')
    return iframe_blocks[0].get('src')

def connect_to_rcb_gis(browser, url):
    connection_attempts = 0
    while connection_attempts < 1:
        try:
            print("Connecting to RCB GIS...")
            browser.get(url)
            for x in range(0,15):
                sleep(30)
                browser.get_screenshot_as_file(f'./{x}.png')        
            # WebDriverWait(browser, 60).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, 'full-container'))
            # )
            print("Conntected to RCB GIS!")
            return True
        except Exception:
            connection_attempts += 1
            print(f'Error connecting to {url}')
    return False

def parse_rcb_gis(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    # iframe_blocks = soup.find_all('iframe')
    # return iframe_blocks[0].get('src')



if __name__ == '__main__':
    browser = get_driver()
    next_url = ""
    if connect_to_mzgov(browser=browser):
        html = browser.page_source
        next_url = parse_mz_html(html)
        print(next_url)
    browser.quit()

    browser = get_driver()
    if connect_to_arcgis(browser=browser, url=next_url):
        html = browser.page_source
        next_url = parse_arcgis_html(html)
        print(next_url)
    browser.quit()

    browser = get_driver()
    if connect_to_rcb_gis(browser = browser, url = next_url):
        html = browser.page_source
        parse_rcb_gis(html)
    browser.quit()

    

