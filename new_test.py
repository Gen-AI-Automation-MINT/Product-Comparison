from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from amazon.amazon_test import process_amazon_url
from walmart.walmart_test import process_walmart_url
import json

if __name__ == "__main__":
    walmart_url_ = walmart_url_list_exa[10]
    print("Test Scraping Started\n")
    process_walmart_url(walmart_url_)
