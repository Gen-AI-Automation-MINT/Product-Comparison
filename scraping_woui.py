from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from amazon.amazon_test import process_amazon_url
from walmart.walmart_test import process_walmart_url

amazon_index = walmart_index = 1
walmart_url_ = walmart_url_list_inc[amazon_index]
amazon_url_ = amazon_url_list_inc[walmart_index]

if __name__ == "__main__":
    print("Test Scraping Started\n")
    a_product_data = process_amazon_url(amazon_url_)
    w_product_data = process_walmart_url(walmart_url_)
    print("\nAmazon Data")
    print(a_product_data)
    print("\nWalmart Data\n")
    print(w_product_data)
