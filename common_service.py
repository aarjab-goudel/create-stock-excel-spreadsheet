from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
import constants

global_driver = None

def getHeader():
    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    # is generally good practice when building a scraper
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1', # Do Not Track Request Header 
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    return headers

def getProfileTexyByTicker(soup, text, tag_name):
    text_tag_results = soup.find_all(lambda tag: tag.name == tag_name and text in tag.text)
    if text_tag_results:
        for text_tag in text_tag_results:
            if text_tag.text == text:
                row_tag = text_tag.parent
                return row_tag
    else:
        print('Error in getting  ' + text + ' from this tag: ' + tag_name)
        return None



def getStatisticsRowByText(soup, text, tag_name):
    text_tag_results = soup.find_all(lambda tag: tag.name == tag_name and text in tag.text)
    if text_tag_results:
        for text_tag in text_tag_results:
            if text_tag.text == text:
                row_tag = text_tag.parent.parent
                return row_tag
    else:
        print('Error in getting  ' + text + ' from this tag: ' + tag_name)
        return None

def getProfileValueFromRowByText(soup, text, tag_name):
    profile_row = getStatisticsRowByText(soup, text, tag_name)
    mini_soup = BeautifulSoup(str(profile_row), "html.parser")
    profile_td = mini_soup.find_all('td')[1]
    print(profile_td.text)
    return profile_td.text

def getRowValueFromStatisticsRow(soup, text, tag_name):
    row_tag = getStatisticsRowByText(soup, text, tag_name)
    if row_tag:
        stat_map = {text: ''}
        mini_soup = BeautifulSoup(str(row_tag), "html.parser")
        td_tags = mini_soup.find_all('td')
        for td_tag in td_tags:
            if text not in td_tag.text:
                stat_map[text] = td_tag.text
        return stat_map
    else:
        return None


def getRowByText(soup, text, tag_name):
    text_tag_results = soup.find_all(lambda tag: tag.name == tag_name and text in tag.text)
    if text_tag_results:  
        for text_tag in text_tag_results:
            if text_tag.text == text:
                row_tag = text_tag.parent.parent.parent
                return row_tag
    else:
        print('Error in getting ' + text + ' from this tag: ' + tag_name)
        return None

def getRowValuesByText(soup, text, tag_name):
    row_tag = getRowByText(soup, text, tag_name)
    if row_tag:
        row_map = {text: []}
        mini_soup = BeautifulSoup(str(row_tag), "html.parser")
        span_tags = mini_soup.find_all('span')
        for span_tag in span_tags:
            if span_tag.text != text:
                row_map[text].append(span_tag.text)
        return row_map
    else:
        return None


def is_valid_number(num):
    """
    Returns True if s is a number that can contain commas and a negative sign, False otherwise.
    """
    try:
        float(num.replace(',', ''))
        return True
    except ValueError:
        return False

def getDriver():
    global global_driver
    if not global_driver:
        options = Options()
        options.add_argument('--headless')
        global_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return global_driver
    else:
        return global_driver

def quitDriver():
    global global_driver
    global_driver.close()
    global_driver.quit()
    global_driver = None



def clickQuarterlyButton(url):
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, constants.SLEEP_TIME).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/button'))).click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def clickOperatingExpense(url):
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, constants.SLEEP_TIME).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))).click()
    WebDriverWait(driver, constants.SLEEP_TIME).until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Operating Expense']/button[@aria-label='Operating Expense']"))).click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def cleanRowValues(values):
    clean_list = []
    try:
        for value in values:
            new_int = int(value.replace(",", ""))
            divide_by_thousand = int(new_int / 1000)
            str_item = '{0:,.2f}'.format(divide_by_thousand).split('.')[0]
            clean_list.append(str_item)
        return clean_list
    except:
        return values

    

