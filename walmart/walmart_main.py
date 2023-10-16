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

output_file_no_duplicates = "../output_files/output_file_no_duplicates.csv"

walmart_urls = ['https://www.walmart.com/ip/999541784?selected=true',
                "https://www.walmart.com/ip/996900990?selected=true",
                "https://www.walmart.com/ip/158741871?selected=true",
                "https://www.walmart.com/ip/925123195?selected=true",
                "https://www.walmart.com/ip/109999521?selected=true",
                "https://www.walmart.com/ip/314409680?selected=true",
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


def get_walmart_soup(url: str) -> (BeautifulSoup, dict):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    print(f"Scraping Walmart URL: {url}")
    with uc.Chrome(options=options, version_main=114) as driver:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        json_blob_data = json.loads(script_tag.get_text())

    return soup, json_blob_data


def check_walmart_url_status(soup: BeautifulSoup, blob: dict) -> None:
    title = soup.find("title")
    if title is None:
        err = blob.get("props", {}).get("pageProps", {}).get("initialData", {}).get("errors", [{}])[0].get("message")
        if err:
            print(f"Walmart Page Problem: {err}")
    elif title.text.strip() in PROBLEMATIC_TITLES:
        print("Walmart Page Problem")
    else:
        print("Walmart Page OK")


def extract_breadcrumbs(soup: BeautifulSoup, blob: dict) -> str:
    breadcrumbs = soup.find("ol", class_="w_4HBV")
    n_breadcrumbs = blob["props"]["pageProps"]["initialData"]["data"]["contentLayout"]["pageMetadata"]["pageContext"][
        "itemContext"].get("categoryPathName")
    # print(n_breadcrumbs)
    if breadcrumbs is None:
        return "No Breadcrumbs Found"
    else:
        b_text = breadcrumbs.text.strip()
        print(b_text)
        return b_text


if __name__ == "__main__":
    walmart_url = walmart_urls[5]
    soup_data, json_blob = get_walmart_soup(walmart_url)
    check_walmart_url_status(soup_data, json_blob)
    breadcrumbs_text = extract_breadcrumbs(soup_data, json_blob)
    raw_product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
