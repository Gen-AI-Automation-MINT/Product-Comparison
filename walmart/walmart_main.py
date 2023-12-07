from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import csv
import undetected_chromedriver as uc
import requests
import json
import re
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa, walmart_url_incorrect

from seleniumbase import Driver

output_file_no_duplicates = "../output_files/output_file_no_duplicates.csv"

custom_headers = {
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,kn;q=0.7",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}


def get_walmart_url_list():
    with open(f"{output_file_no_duplicates}", 'r') as file:
        reader = csv.reader(file)
        walmart_url_list = []
        for row in reader:
            walmart_url_list.append(row[2])
        return walmart_url_list


def get_walmart_soup(url: str, driver_type: str = 'uc') -> BeautifulSoup:
    print(f"\nScraping Walmart URL: {url}")
    if driver_type == 're':
        try:
            response = requests.get(url, headers=custom_headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            soup = None
        return soup
    elif driver_type == 'so':
        try:
            scrapeops_response = requests.get(
                url='https://proxy.scrapeops.io/v1/',
                params={
                    'api_key': '14355e00-a2df-4040-b577-11c254784e0f',  # Replace with your actual API key
                    'url': url,
                },
            )
            scrapeops_response.raise_for_status()
            soup = BeautifulSoup(scrapeops_response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error scraping {url} using scrapeops: {e}")
            soup = None
        return soup
    driver = None
    try:
        if driver_type == 'uc':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = uc.Chrome(options=options, version_main=114, enable_cdp_events=True)
        elif driver_type == 'sb':
            driver = Driver(uc=True)
        else:
            raise ValueError("Invalid driver type. Use 're', 'uc', or 'sb'.")

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    finally:
        if driver:
            print("Used Driver", driver_type)
            # driver.quit()

    return soup


def check_walmart_url_status(soup: BeautifulSoup):
    title = soup.find("title")
    page_status = 0
    PROBLEMATIC_TITLES = {
        "Prints Builder | Walmart Photo",
        "Walmart.com | Save Money. Live Better",
        "Request Rejected"
    }
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
        page_status = 200
        print(f"Title: {title.text.strip()}")

    return page_status, json_blob_data


def extract_breadcrumbs(soup: BeautifulSoup, blob: dict) -> str:
    breadcrumbs = soup.find("ol", class_="w_4HBV")
    if breadcrumbs is None:
        return "No Breadcrumbs Found"
    else:
        b_text = breadcrumbs.text.strip()
        print(f"Breadcrumbs: {b_text}")
        return b_text


def is_exclusive(soup: BeautifulSoup) -> bool:
    searched_words = [
        'Walmart Exclusive',
        'Exclusively at Walmart',
        'Exclusively for Walmart',
        'Exclusive to Walmart',
        'exclusively at Walmart',
        'Only at Walmart',
        'Only available at Walmart and Walmart.com',
        'WALMART EXCLUSIVE',
        'exclusive to Walmart',
        'Walmart-Exclusive',
        'Walmart exclusive',
    ]

    for word in searched_words:
        regex = re.compile(f'.*{word}.*', re.IGNORECASE)
        found = soup.find_all(string=regex, recursive=True)
        if found:
            return True

    return False


def format_short_description(description):
    if re.search(r'<[^>]+>', description):
        soup = BeautifulSoup(description, 'html.parser')
        list_items = soup.find_all('li')
        formatted_description = [item.get_text(strip=True) for item in list_items]
    else:
        formatted_description = [sentence.strip() for sentence in description.split('.') if sentence.strip()]

    return formatted_description


def extract_product_data(soup: BeautifulSoup, blob: dict, url) -> dict:
    raw_product_data = blob.get("props", {}).get("pageProps", {}).get("initialData", {}).get("data", {}).get("product",
                                                                                                             {})
    title = raw_product_data.get('name', '')
    if raw_product_data.get('shortDescription'):
        formatted_description = format_short_description(raw_product_data.get('shortDescription'))
    else:
        formatted_description = []

    idml_data = blob.get("props", {}).get("pageProps", {}).get("initialData", {}).get("data", {}).get('idml', {})
    specification_blob = idml_data.get('specifications')
    if specification_blob:
        formatted_specifications = [{"key": item.get("name", ""), "value": item.get("value", "")} for item in
                                    specification_blob]
    else:
        formatted_specifications = []

    all_dangerous_html = soup.find_all("div", class_="dangerous-html mb3")
    additional_info = []
    for i in all_dangerous_html:
        additional_info.append(i.text)
    manufacturer = None
    if raw_product_data.get('manufacturerName'):
        manufacturer = raw_product_data.get('manufacturerName')
    if not manufacturer:
        for spec in formatted_specifications:
            if spec.get('key') == 'Manufacturer':
                manufacturer = spec.get('value')

    product_id = re.search(r'/ip/(\d+)\?', url).group(1)
    blob_product_data = ({
        'id': product_id,
        'url': url,
        'url_status': '200',
        'type': raw_product_data.get('type'),
        'name': title,
        'brand': raw_product_data.get('brand'),
        'manufacturerName': manufacturer,
        'shortDescription': formatted_description,
        'specifications': formatted_specifications,
        "additionalInfo": additional_info
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


driver = Driver(uc=True)
if __name__ == "__main__":
    # walmart_url_i = []
    # with open('../input_files/urls.csv', 'r') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     for row in csv_reader:
    #         if row['Match_Type'] == 'Not Sure':
    #             walmart_url_i.append(row['Walmart_Url'])
    print("Walmart Scraping Started\n")
    scrape_list = walmart_url_incorrect

    print(f"Scraping {len(scrape_list)} URLs\n ")
    for walmart_url in scrape_list:
        # walmart_url = scrape_list[1]
        driver.get(walmart_url)
        soup_data = BeautifulSoup(driver.page_source, 'html.parser')
        # soup_data = get_walmart_soup(walmart_url, driver_type='sb')
        if soup_data:
            page_status_, json_blob = check_walmart_url_status(soup_data)
            if page_status_ == 200:
                breadcrumbs_text = extract_breadcrumbs(soup_data, json_blob)
                product_data = extract_product_data(soup_data, json_blob, walmart_url)
                print(product_data)
            else:
                product_data = generate_error_data(walmart_url, page_status_)
                print(product_data)
        else:
            product_data = generate_error_data(walmart_url, 404)
            print(product_data)

        push_the_data_to_json(product_data)
