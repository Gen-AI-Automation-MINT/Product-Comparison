from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from amazon.amazon_test import process_amazon_url
from walmart.walmart_test import process_walmart_url
import json


def scrape_both(amazon_urls, walmart_urls, amazon_index, walmart_index):
    amazon_url = amazon_urls[amazon_index] if amazon_index < len(amazon_urls) else None
    walmart_url = walmart_urls[walmart_index] if walmart_index < len(walmart_urls) else None

    if amazon_url and walmart_url:
        print("Test Scraping Started\n")
        amazon_data_ = process_amazon_url(amazon_url)
        walmart_data_ = process_walmart_url(walmart_url)

        return amazon_data_, walmart_data_
    else:
        return None, None


def push_data_to_json(data):
    with open('data.json', 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    amazon_urls = amazon_url_list_exa
    walmart_urls = walmart_url_list_exa
    amazon_index = 6
    walmart_index = 6
    print("Test Scraping Started\n")
    amazon_data, walmart_data = scrape_both(amazon_urls, walmart_urls, amazon_index, walmart_index)
