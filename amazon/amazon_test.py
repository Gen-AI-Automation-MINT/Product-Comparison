from amazon_main import get_amazon_soup, check_amazon_url_status, extract_product_data, amazon_url_list
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa

if __name__ == "__main__":
    amazon_url = amazon_url_list[18]
    soup_data = get_amazon_soup(amazon_url, driver_type='uc')
    page_status_ = check_amazon_url_status(soup_data)
    # if page_status_ == 200:
    #     product_data = extract_product_data(soup_data, json_blob, amazon_url)
    #     print(product_data)
