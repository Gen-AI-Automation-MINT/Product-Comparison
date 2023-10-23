from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import csv
import pyautogui
import time
import os
import codecs
import threading
import urllib.parse
import urllib.request
import undetected_chromedriver as uc
import pyodbc
from datetime import datetime
import ssl
import psycopg2
import pandas as pd
import json
from lxml import etree
import re

from seleniumbase import Driver

output_file_no_duplicates = "../output_files/output_file_no_duplicates.csv"

walmart_urls = ['https://www.walmart.com/ip/999541784?selected=true',
                "https://www.walmart.com/ip/996900990?selected=true",
                "https://www.walmart.com/ip/925123195?selected=true",
                "https://www.walmart.com/ip/314409680?selected=true",
                "https://www.walmart.com/ip/158741871?selected=true",
                "https://www.walmart.com/ip/109999521?selected=true",
                "https://www.walmart.com/ip/755983708?selected=true"]

PROBLEMATIC_TITLES = {
    "Prints Builder | Walmart Photo",
    "Walmart.com | Save Money. Live Better",
    "Request Rejected"
}


def get_walmart_url_list():
    with open(f"{output_file_no_duplicates}", 'r') as file:
        reader = csv.reader(file)
        walmart_url_list = []
        for row in reader:
            walmart_url_list.append(row[2])
        return walmart_url_list


def get_walmart_soup(url: str, driver_type: str = 'undetected') -> BeautifulSoup:
    print(f"\n\nScraping Walmart URL: {url}")
    if driver_type == 'uc':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = uc.Chrome(options=options, version_main=114)
    elif driver_type == 'sb':
        driver = Driver(uc=True)
    else:
        raise ValueError("Invalid driver type. Use 'undetected' or 'seleniumbase'.")

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        driver.quit()

    return soup


def check_walmart_url_status(soup: BeautifulSoup):
    title = soup.find("title")
    page_status = 0
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    json_blob_data = {}
    if script_tag:
        json_blob_data = json.loads(script_tag.get_text())
    if title is None:
        err = json_blob_data.get("props", {}).get("pageProps", {}).get("initialData", {}).get("errors", [{}])[0].get(
            "message")
        if err:
            page_status = err
            print(f"Walmart Page Problem: {err}")
    elif title.text.strip() in PROBLEMATIC_TITLES:
        print("Walmart Page Problem")
        page_status = 400
    elif title.text.strip() == "Robot or human?":
        print("Automated Traffic Detected")
        page_status = 999
    else:
        print("Walmart Page Valid")
        page_status = 200

    return page_status, json_blob_data


def extract_breadcrumbs(soup: BeautifulSoup, blob: dict) -> str:
    breadcrumbs = soup.find("ol", class_="w_4HBV")
    if breadcrumbs is None:
        return "No Breadcrumbs Found"
    else:
        b_text = breadcrumbs.text.strip()
        print(b_text)
        return b_text


def format_short_description(description):
    if re.search(r'<[^>]+>', description):
        soup = BeautifulSoup(description, 'html.parser')

        list_items = soup.find_all('li')
        formatted_description = [item.get_text(strip=True) for item in list_items]
    else:
        formatted_description = [sentence.strip() for sentence in description.split('.') if sentence.strip()]

    return formatted_description


def extract_product_data(soup: BeautifulSoup, blob: dict, url) -> dict:
    raw_product_data = blob["props"]["pageProps"]["initialData"]["data"]["product"]
    product_id = re.search(r'/ip/(\d+)\?', url).group(1)
    formatted_description = format_short_description(raw_product_data.get('shortDescription'))
    specification_blob = blob["props"]["pageProps"]["initialData"]["data"]['idml'].get('specifications')
    formatted_specifications = [{"key": item["name"], "value": item["value"]} for item in specification_blob]
    description_data = []
    for i in formatted_description:
        description_data.append(i)
    blob_product_data = ({
        'id': product_id,
        'url': url,
        'url_status': '200',
        'type': raw_product_data.get('type'),
        'name': raw_product_data.get('name'),
        'brand': raw_product_data.get('brand'),
        'manufacturerName': raw_product_data.get('manufacturerName'),
        'shortDescription': description_data,
        'specifications': blob["props"]["pageProps"]["initialData"]["data"]['idml'].get(
            'specifications'),
        'formatted_specifications': formatted_specifications,
    })
    return blob_product_data


def push_the_data_to_json(p_data):
    try:
        with open('walmart_data.json', 'r') as fp:
            data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, list):
        data.append(p_data)
    elif isinstance(data, dict):
        data = [data, p_data]
    else:
        data = [p_data]

    with open('walmart_data.json', 'w') as fp:
        json.dump(data, fp, indent=4)


def generate_error_data(w_url, status):
    product_id = re.search(r'/ip/(\d+)\?', w_url).group(1)
    return {
        'id': product_id,
        'url': w_url,
        'url_status': status,
        'match_type': 'Walmart Page Problem'
    }


if __name__ == "__main__":
    print("Scraping Started\n")
    walmart_url = "https://www.walmart.com/ip/314409680?selected=true"
    # for walmart_url in walmart_urls:
    soup_data = get_walmart_soup(walmart_url, driver_type='uc')
    page_status_, json_blob = check_walmart_url_status(soup_data)
    if page_status_ == 200:
        breadcrumbs_text = extract_breadcrumbs(soup_data, json_blob)
        product_data = extract_product_data(soup_data, json_blob, walmart_url)
        print(product_data)
    else:
        product_data = generate_error_data(walmart_url, page_status_)
        print(product_data)

    push_the_data_to_json(product_data)
