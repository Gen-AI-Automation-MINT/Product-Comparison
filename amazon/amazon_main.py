from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import csv, pyautogui, time, os, codecs, threading
import undetected_chromedriver as uc
import pyodbc
from datetime import datetime
import ssl
import psycopg2
import pandas as pd
import json
from lxml import etree
from seleniumbase import Driver
import requests

custom_headers = {
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,kn;q=0.7",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}

output_file_no_duplicates = "../output_files/output_file_no_duplicates.csv"

amazon_url_list = [
    "https://www.amazon.com/dp/B075NSQ7LY?th=1&psc=1",
    "https://www.amazon.com/dp/B089GMJ8RS?th=1&psc=1",
    "https://www.amazon.com/dp/B07L2MW2VK?th=1&psc=1",
    "https://www.amazon.com/dp/B00K1PBYKE?th=1&psc=1",
    "https://www.amazon.com/dp/B00L76QUAK?th=1&psc=1",
    "https://www.amazon.com/dp/B072BC9LQG?th=1&psc=1",
    "https://www.amazon.com/dp/B089SPJZJW?th=1&psc=1",
    "https://www.amazon.com/dp/B07Q8RTRW3?th=1&psc=1",
    "https://www.amazon.com/dp/B099K1DP9P?th=1&psc=1",
    "https://www.amazon.com/dp/B00IKVS79C?th=1&psc=1",
    "https://www.amazon.com/dp/B00OEJZKIK?th=1&psc=1",
    "https://www.amazon.com/dp/B0B3XRT96M?th=1&psc=1",
    "https://www.amazon.com/dp/B007YT34VM?th=1&psc=1",
    "https://www.amazon.com/dp/B07VVMHHMP?th=1&psc=1",
    "https://www.amazon.com/dp/B00745BUGW?th=1&psc=1",
    "https://www.amazon.com/dp/B00B37ERSU?th=1&psc=1",
    "https://www.amazon.com/dp/B07MY8PWHN?th=1&psc=1",
    "https://www.amazon.com/dp/B08YZBK7N5?th=1&psc=1",
    "https://www.amazon.com/dp/B07SQL5L8W?th=1&psc=1",
]


def get_amazon_url_list():
    with open(f"{output_file_no_duplicates}", 'r') as file:
        reader = csv.reader(file)
        walmart_url_list = []
        for row in reader:
            walmart_url_list.append(row[2])
        return walmart_url_list


def get_amazon_soup(url: str, driver_type: str = 're') -> BeautifulSoup:
    print(f"\n\n\nScraping Amazon URL: {url}")
    if driver_type == 'uc':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = uc.Chrome(options=options, version_main=114)
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        finally:
            driver.quit()
    elif driver_type == 're':
        response = requests.get(url, headers=custom_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
        else:
            print(url + " failed")
            soup = None
    else:
        raise ValueError("Invalid driver type. Use 're' or 'uc'.")

    return soup


def check_amazon_url_status(soup: BeautifulSoup):
    if soup:
        title_element = soup.select_one("#title")
        if title_element:
            title = title_element.text.strip()
        else:
            title = soup.find('title').get_text().strip()
    else:
        title = None
    if title:
        print(f"Title: {title}")
        page_status = 200
    elif title == "Robot or human?":
        print("Automated Traffic Detected")
        page_status = 999
    elif title == "Amazon.com":
        print("Page Error, Change driver")
        page_status = 404
    else:
        print("Amazon Page Problem")
        page_status = 400

    return page_status


def extract_product_data(soup: BeautifulSoup, url) -> dict:
    title_element = soup.select_one("#title")
    title = title_element.text.strip() if title_element else None
    brand_element = soup.select_one("#bylineInfo")
    brand = brand_element.text.strip() if brand_element else None
    about_item = []
    for items in soup.find_all("li", attrs={'class': 'a-spacing-mini'}):
        about_item.append(items.text.strip())
    description_element = soup.find("div", attrs={'id': 'productDescription_fullView'})
    description = description_element.text.strip() if description_element else None
    specifications_element_name = soup.find_all("span", attrs={'class': 'a-size-base a-color-tertiary'})
    specifications_element_value = soup.find_all("span", attrs={'class': 'a-size-base a-color-base'})
    specifications = []
    length = len(specifications_element_name) if len(specifications_element_name) < len(
        specifications_element_value) else len(specifications_element_value)
    for i in range(length):
        name = specifications_element_name[i].text.strip() if specifications_element_name[i] else ""
        value = specifications_element_value[i].text.strip() if specifications_element_value[i] else ""
        specifications.append({
            "name": name,
            "value": value
        })

    blob_product_data = ({
        'url': url,
        'url_status': '200',
        'type': "product",
        'name': title,
        'brand': brand,
        'manufacturerName': None,
        'shortDescription': description,
        'specifications': specifications,
    })
    return blob_product_data


def push_the_data_to_json(p_data):
    try:
        with open('amazon_data.json', 'r') as fp:
            data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, list):
        data.append(p_data)
    elif isinstance(data, dict):
        data = [data, p_data]
    else:
        data = [p_data]

    with open('amazon_data.json', 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    for amazon_url in amazon_url_list:
        soup_data = get_amazon_soup(amazon_url, driver_type='re')
        page_status_ = check_amazon_url_status(soup_data)
        if page_status_ == 200:
            product_data = extract_product_data(soup_data, amazon_url)
            print(product_data)
            push_the_data_to_json(product_data)
        elif page_status_ == 400:
            product_data = ({
                'url': amazon_url,
                'url_status': '400'
            })
            push_the_data_to_json(product_data)
        elif page_status_ == 999:
            product_data = ({
                'url': amazon_url,
                'url_status': '999'
            })
            push_the_data_to_json(product_data)
        else:
            product_data = ({
                'url': amazon_url,
                'url_status': '404'
            })
            push_the_data_to_json(product_data)
