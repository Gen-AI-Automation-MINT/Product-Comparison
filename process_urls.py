from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from amazon.amazon_test import process_amazon_url
from walmart.walmart_test import process_walmart_url


def scrape_both(amazon_urls, walmart_urls, a_index, w_index):
    amazon_url = amazon_urls[a_index] if a_index < len(amazon_urls) else None
    walmart_url = walmart_urls[w_index] if w_index < len(walmart_urls) else None

    if amazon_url and walmart_url:
        amazon_data = process_amazon_url(amazon_url, dtype='re')
        walmart_data = process_walmart_url(walmart_url, dtype='so')
        return amazon_data, walmart_data
    else:
        return None, None


if __name__ == "__main__":
    amazon_urls_ = amazon_url_list_exa
    walmart_urls_ = walmart_url_list_exa
    amazon_index = walmart_index = 2
    print("\nTest Scraping Started\n")
    amazon_data_, walmart_data_ = scrape_both(amazon_urls_, walmart_urls_, amazon_index, walmart_index)
