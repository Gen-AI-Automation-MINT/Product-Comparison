import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

custom_headers = {
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,kn;q=0.7",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}

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

product_data_list = []


def get_product_info(url):
    response = requests.get(url, headers=custom_headers)
    if response.status_code != 200:
        print("Error in getting webpage")
        print(url + " failed")
        product_data_list.append({
            "url": url,
            "type": None,
            "name": None,
            "brand": None,
            "shortDescription": None,
            "specifications": None,
        })

    soup = BeautifulSoup(response.text, "lxml")

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
    product_data_list.append({
        "url": url,
        "type": "product",
        "name": title,
        "brand": brand,
        "shortDescription": description,
        "specifications": specifications,
    })
    if response.status_code == 200:
        print(url + " done")


for url in amazon_url_list:
    get_product_info(url)

print(product_data_list)

with open("amazon_full.json", "w") as f:
    json.dump(product_data_list, f, indent=4)
