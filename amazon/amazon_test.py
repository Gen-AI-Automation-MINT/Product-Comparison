from .amazon_main import get_amazon_soup, check_amazon_url_status, extract_product_data, generate_error_data, STATUS_MAP
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa


def process_amazon_url(amazon_url):
    a_soup_data = get_amazon_soup(amazon_url, driver_type='re')
    a_page_status_ = check_amazon_url_status(a_soup_data)
    if a_page_status_ == 200:
        a_product_data = extract_product_data(a_soup_data, amazon_url)
        print(a_product_data)
    else:
        a_product_data = generate_error_data(amazon_url, STATUS_MAP.get(a_page_status_, "Unknown"))
    return a_product_data


# if __name__ == "__main__":
#     amazon_url_ = amazon_url_list_exa[20]
#     print("Test Scraping Started\n")
#     process_amazon_url(amazon_url_)
