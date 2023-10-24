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
from typing import Optional, Dict, Tuple
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa

custom_headers = {
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,kn;q=0.7",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}

output_file_no_duplicates = "amazon_url_list_no_duplicates.csv"

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


def get_amazon_soup(url: str, driver_type: str = "re") -> BeautifulSoup:
    """
    Fetches a BeautifulSoup object for the given Amazon URL using the specified driver type.
    Returns: BeautifulSoup: Parsed web page content.
    """
    print(f"\nScraping Amazon URL: {url}")
    if driver_type == "uc":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=3200x20800")
        chrome_options.add_argument('--no-sandbox')
        driver = uc.Chrome(enable_cdp_events=True, options=chrome_options, version_main=114)
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        finally:
            driver.quit()

    elif driver_type == "re":
        try:
            response = requests.get(url, headers=custom_headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            soup = None

    else:
        raise ValueError(f"Invalid driver type. Use 're' or 'uc'.")

    return soup


def check_amazon_url_status(soup: Optional[BeautifulSoup]) -> int:
    page_status = 0
    messages: Dict[str, Tuple[str, int]] = {
        "Robot or human?": ("Automated Traffic Detected", 999),
        "Amazon.com": ("Page Error, Change driver (404)", 404),
        "Amazon.com. Spend less. Smile more.": ("Page Error, Invalid URL (400)", 400),
    }
    if not soup:
        print("No Soup")
        return page_status
    try:
        title_element = soup.select_one("#title") or soup.find('title')
        title = title_element.text.strip() if title_element else None
    except Exception as e:
        print(f"Error parsing soup: {e}")
        return page_status
    if title and title in messages:
        print(messages[title][0])
        page_status = messages[title][1]
    elif title:
        print(f"Title: {title}")
        page_status = 200
    else:
        print("Unknown error")

    return page_status


def extract_product_details(soup: BeautifulSoup):
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

    return specifications_b, about_item_items


def extract_product_table(soup: BeautifulSoup):
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

    specifications_additional = []
    about_item_additional = []
    if len(specifications) < 1:
        specifications_additional, about_item_additional = extract_product_details(soup)
        specifications.extend(specifications_additional)
    product_table = extract_product_table(soup)
    product_id = re.search(r'/dp/([^?/]+)', url).group(1)

    manufacturer = None
    if product_table.get('Manufacturer'):
        manufacturer = product_table.get('Manufacturer')
    if not manufacturer:
        for spec in specifications:
            if spec.get('key') == 'Manufacturer':
                manufacturer = spec.get('value')

    blob_product_data = ({
        'id': product_id,
        'url': url,
        'url_status': '200',
        'type': "product",
        'name': title,
        'brand': formatted_brand,
        'manufacturerName': manufacturer,
        'shortDescription': description,
        'specifications': specifications,
        'specifications_b': specifications_additional,
        'aboutItem': about_item,
        'additionalInfo': about_item_additional,
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
    print("Amazon Scraping Started\n")
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
