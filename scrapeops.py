import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import config

SCRAPEOPS_API_KEY = config.scrapeops_api_key
product_url_list = [
    "https://www.walmart.com/ip/466185717?selected=true",
    "https://www.walmart.com/ip/1286642938?selected=true",
    "https://www.walmart.com/ip/736755300?selected=true",
    "https://www.walmart.com/ip/158741871?selected=true",
    "https://www.walmart.com/ip/925123195?selected=true",
    "https://www.walmart.com/ip/109999521?selected=true",
    "https://www.walmart.com/ip/314409680?selected=true",
    "https://www.walmart.com/ip/755983708?selected=true",
    "https://www.walmart.com/ip/674290295?selected=true",
    "https://www.walmart.com/ip/288150096?selected=true",
    "https://www.walmart.com/ip/377111281?selected=true",
    "https://www.walmart.com/ip/332498618?selected=true",
    "https://www.walmart.com/ip/116481628?selected=true",
    "https://www.walmart.com/ip/135821061?selected=true",
    "https://www.walmart.com/ip/931359?selected=true",
    "https://www.walmart.com/ip/1182714231?selected=true",
    "https://www.walmart.com/ip/666004175?selected=true",
    "https://www.walmart.com/ip/614858163?selected=true",
    "https://www.walmart.com/ip/937248769?selected=true",
]


def scrapeops_url(url):
    payload = {'api_key': SCRAPEOPS_API_KEY, 'url': url, 'country': 'us'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


product_data_list = []

full_product_data = []

for url in product_url_list:
    try:
        response = requests.get(scrapeops_url(url))
        if response.status_code == 200:
            html_response = response.text
            soup = BeautifulSoup(html_response, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if script_tag is not None:
                json_blob = json.loads(script_tag.get_text())
                full_product_data.append(json_blob["props"]["pageProps"]["initialData"]["data"])
                raw_product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
                product_data_list.append({
                    'url': url,
                    'type': raw_product_data.get('type'),
                    'name': raw_product_data.get('name'),
                    'brand': raw_product_data.get('brand'),
                    'manufacturerName': raw_product_data.get('manufacturerName'),
                    'shortDescription': raw_product_data.get('shortDescription'),
                    'specifications': json_blob["props"]["pageProps"]["initialData"]["data"]['idml'].get(
                        'specifications'),
                    'price': raw_product_data['priceInfo']['currentPrice'].get('price'),
                    'currencyUnit': raw_product_data['priceInfo']['currentPrice'].get('currencyUnit'),
                })
                print('Success', url)

    except Exception as e:
        print('Error', e)
        print('Error', url)
        product_data_list.append({
            "url": url,
            "type": None,
            "name": None,
            "brand": None,
            "manufacturerName": None,
            "shortDescription": None,
            "specifications": None,
            "price": None,
            "currencyUnit": None,
        })

print(product_data_list)

with open('walmart_full.json', 'w') as json_file:
    json.dump(product_data_list, json_file, indent=4)

with open('walmart_full_scrape.json', 'w') as json_file:
    json.dump(full_product_data, json_file, indent=4)
