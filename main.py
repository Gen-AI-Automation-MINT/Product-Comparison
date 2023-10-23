import requests
import json
import config
import pandas as pd
from passing_to_llm import conduct_product_comparison
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from process_urls import scrape_both

if __name__ == "__main__":
    amazon_urls = amazon_url_list_exa
    walmart_urls = walmart_url_list_exa
    amazon_index = walmart_index = 5
    amazon_data, walmart_data = scrape_both(amazon_urls, walmart_urls, amazon_index, walmart_index)
    result = conduct_product_comparison(walmart_data, amazon_data)
    print(result)
