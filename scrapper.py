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

def conntect_to_page_and_wait_for_specific_element(browser, url, by, by_satisfier, timeout, max_tries):
    connection_attempts = 0
    while connection_attempts < max_tries:
        try:
            print(f"Connecting to [ {url} ]")
            browser.get(url)
            WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located((by, by_satisfier))
            )
            return
        except Exception:
            connection_attempts += 1
            print(f"Error connecting to [ {url} ]")
    raise Exception(f"Error connecting to [ {url} ]")

def parse_for_src_from_iframe(html):
    soup = BeautifulSoup(html, "html.parser")
    iframe_blocks = soup.find_all('iframe')
    return iframe_blocks[0].get('src')

def connect_to_rcb_gis(browser, url):
    connection_attempts = 0
    while connection_attempts < 1:
        try:
            print(f"Connecting to [ {url} ]")
            browser.get(url)
            for x in range(0,120):
                sleep(60)
                browser.get_screenshot_as_file(f'./{x}.png')        
            # WebDriverWait(browser, 60).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, 'full-container'))
            # )
            print("Conntected to RCB GIS!")
        except Exception:
            connection_attempts += 1
            print(f'Error connecting to {url}')
            raise Exception(f'Error connecting to RCB GIS')

def parse_rcb_gis(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())



if __name__ == '__main__':
    browser = get_driver()
    next_url = "https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19"
    
    try:
        #MZ PAGE
        conntect_to_page_and_wait_for_specific_element(browser=browser, url=next_url, by=By.TAG_NAME, by_satisfier="iframe", timeout=30, max_tries=3)
        html = browser.page_source
        next_url = parse_for_src_from_iframe(html)
        #ARCGIS
        conntect_to_page_and_wait_for_specific_element(browser=browser, url=next_url, by=By.TAG_NAME, by_satisfier="iframe", timeout=30, max_tries=3)
        html = browser.page_source
        next_url = parse_for_src_from_iframe(html)
        #RCB ARCGIS
        connect_to_rcb_gis(browser = browser, url = next_url)
        html = browser.page_source
        parse_rcb_gis(html)
    except Exception as ex:
        print(ex)
    finally:
        browser.quit()



    

