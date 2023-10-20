from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import csv, pyautogui, time, os, codecs, threading
import urllib.parse, urllib.request
import undetected_chromedriver as uc
import pyodbc
from datetime import datetime
import ssl
import psycopg2
import pandas as pd
import json
from lxml import etree
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
    print(f"Scraping Walmart URL: {url}")
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


def extract_product_data(soup: BeautifulSoup, blob: dict, url) -> dict:
    raw_product_data = blob["props"]["pageProps"]["initialData"]["data"]["product"]
    blob_product_data = ({
        'url': url,
        'type': raw_product_data.get('type'),
        'name': raw_product_data.get('name'),
        'brand': raw_product_data.get('brand'),
        'manufacturerName': raw_product_data.get('manufacturerName'),
        'shortDescription': raw_product_data.get('shortDescription'),
        'specifications': blob["props"]["pageProps"]["initialData"]["data"]['idml'].get(
            'specifications'),
    })
    return blob_product_data


if __name__ == "__main__":
    for walmart_url in walmart_urls:
        soup_data = get_walmart_soup(walmart_url, driver_type='uc')
        page_status_, json_blob = check_walmart_url_status(soup_data)
        if page_status_ == 200:
            breadcrumbs_text = extract_breadcrumbs(soup_data, json_blob)
            product_data = extract_product_data(soup_data, json_blob, walmart_url)
            print(product_data)
