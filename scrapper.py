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
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
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
        except Exception as ex:
            connection_attempts += 1
            print(f'Error connecting to {base_url}')
            print(ex)
            print(f'Attempt #{connection_attempts}.')

    return False

def connect_to_arcgis(browser, url):
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            print("Connecting to ARCGIS...")
            browser.get(url)
            sleep(15)
            browser.find_element_by_id('app')
            print("Connected to ARCGIS!")
            return True
        except Exception as ex:
            print(str(ex))
            connection_attempts += 1
            print(f'Error connecting to {url}')

    return False


def parse_mz_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    iframe_blocks = soup.find_all('iframe')
    return iframe_blocks[0].get('src')

def parse_arcgis_html(html):
    soup = soup = BeautifulSoup(html, 'html.parser')
    dock_elements = soup.find_all(class_="dock-element")
    for dock_element in dock_elements:
        print(dock_element)


if __name__ == '__main__':
    browser = get_driver()
    if connect_to_mzgov(browser=browser):
        html = browser.page_source
        arcgis_url = parse_mz_html(html)
        print(arcgis_url)
        if connect_to_arcgis(browser, arcgis_url):
            html = browser.page_source
            parse_arcgis_html(html)

    browser.quit()

