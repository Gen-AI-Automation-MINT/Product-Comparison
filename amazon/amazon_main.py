from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import csv
import pyautogui
import time
import os
import codecs
import threading
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
import re
from typing import Optional
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa

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

STATUS_MAP = {
    0: "0",
    200: "200",
    400: "400",
    404: "404",
    999: "999"
}


def get_amazon_url_list():
    with open(f"{output_file_no_duplicates}", 'r') as file:
        reader = csv.reader(file)
        walmart_url_list = []
        for row in reader:
            walmart_url_list.append(row[2])
        return walmart_url_list


def get_amazon_soup(url: str, driver_type: str = 're') -> BeautifulSoup:
    print(f"\n\nScraping Amazon URL: {url}")

    if driver_type == 'uc':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        with uc.Chrome(options=options, version_main=114) as driver:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
    elif driver_type == 're':
        try:
            response = requests.get(url, headers=custom_headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
        except requests.RequestException:
            print(f"{url} failed")
            soup = None
    else:
        raise ValueError("Invalid driver type. Use 're' or 'uc'.")

    return soup


def check_amazon_url_status(soup: Optional[BeautifulSoup]) -> int:
    title = None
    page_status = 400
    messages = {
        "None": ("Failed", 0),
        "Robot or human?": ("Automated Traffic Detected", 999),
        "Amazon.com": ("Page Error, Change driver", 404),
        "Amazon.com. Spend less. Smile more.": ("Page Error", 400),
    }

    if soup:
        title_element = soup.select_one("#title") or soup.find('title')
        if title_element:
            title = title_element.text.strip()

    if title:
        if title in messages:
            print(messages[title][0])
            page_status = messages[title][1]
        else:
            print(f"Title: {title}")
            page_status = 200
    else:
        page_status = 0
        print("No Soup")

    return page_status


def extract_product_details(soup: BeautifulSoup, url):
    specifications_b = []
    about_item_items = []
    product_details_section = soup.find('a', id='productFactsToggleButton')
    if product_details_section:
        product_details_content = product_details_section.find_next('div', class_='a-expander-content')
        if product_details_content:
            product_details = product_details_content.find_all('div', class_='a-row')
            for i in range(0, len(product_details), 2):
                key_element = product_details[i].find('span', class_='a-size-small a-color-base a-text-bold')
                value_element = product_details[i + 1].find('span', class_='a-size-base a-color-secondary')
                key = key_element.text.strip() if key_element else None
                value = value_element.text.strip() if value_element else None
                if key:
                    specifications_b.append({
                        "key": key,
                        "value": value
                    })

    about_item = soup.find('h3', class_='sldp-title')
    if about_item:
        for ul in about_item.find_all_next('ul', class_='a-unordered-list'):
            about_item_items.append(ul.text.strip())

    print("\nAbout This Item:")
    for item in about_item_items:
        print(item)
    return specifications_b, about_item_items


def extract_product_table(soup: BeautifulSoup, url):
    product_info = {}
    formatted_product_info = {}
    product_info_section = soup.find('div', id='productDetails_secondary_view_div')
    if product_info_section:
        product_info_table = product_info_section.find('table', class_='a-keyvalue prodDetTable')

        if product_info_table:
            rows = product_info_table.find_all('tr')
            for row in rows:
                th = row.find('th', class_='a-span3 prodDetSectionEntry')
                td = row.find('td', class_='a-span9 a-align-center prodDetSectionEntry')
                if th and td:
                    key = th.text.strip()
                    value = td.text.strip()
                    product_info[key] = value
    if product_info:
        formatted_product_info = {key: value.replace('\u200e', '').strip() for key, value in product_info.items()}

    return formatted_product_info


def extract_product_data(soup: BeautifulSoup, url) -> dict:
    title_element = soup.select_one("#title")
    title = title_element.text.strip() if title_element else None
    brand_element = soup.select_one("#bylineInfo")
    brand = brand_element.text.strip() if brand_element else None
    formatted_brand = None
    if brand:
        match = re.search(r'(?:Brand:|Visit the )([^<]+)', brand)
        if match:
            formatted_brand = match.group(1).strip()
    about_item = []
    for items in soup.find_all("li", attrs={'class': 'a-spacing-mini'}):
        about_item.append(items.text.strip())
    description_element = soup.find("div", attrs={'id': 'productDescription_fullView'})
    description = description_element.text.strip() if description_element else None

    specifications_element_name = soup.find_all("span", attrs={'class': 'a-size-base a-color-tertiary'})
    specifications_element_value = soup.find_all("span", attrs={'class': 'a-size-base a-color-base'})
    specifications = []
    for name, value in zip(specifications_element_name, specifications_element_value):
        name_text = name.text.strip()
        value_text = value.text.strip()
        specifications.append({"key": name_text, "value": value_text})
    specifications_b = []
    if len(specifications) < 2:
        specifications_b, about_item = extract_product_details(soup, url)
    product_table = extract_product_table(soup, url)
    product_id = re.search(r'/dp/([^?/]+)', url).group(1)
    blob_product_data = ({
        'id': product_id,
        'url': url,
        'url_status': '200',
        'type': "product",
        'name': title,
        'brand': formatted_brand,
        'manufacturerName': None,
        'shortDescription': description,
        'specifications': specifications,
        'specifications_b': specifications_b,
        'aboutItem': about_item,
        'productTable': product_table,

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


def generate_error_data(a_url, status):
    product_id = re.search(r'/dp/([^?/]+)', a_url).group(1)
    return {
        'id': product_id,
        'url': a_url,
        'url_status': status,
        'match_type': 'Amazon Page Problem'
    }


if __name__ == "__main__":
    scrape_list = amazon_url_list_inc
    print(f"Scraping {len(scrape_list)} URLs\n ")
    for amazon_url in scrape_list:
        soup_data = get_amazon_soup(amazon_url, driver_type='re')
        page_status_ = check_amazon_url_status(soup_data)
        if page_status_ == 200:
            product_data = extract_product_data(soup_data, amazon_url)
            print(product_data)
        else:
            product_data = generate_error_data(amazon_url, STATUS_MAP.get(page_status_, "Unknown"))

        push_the_data_to_json(product_data)
