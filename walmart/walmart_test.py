from .walmart_main import get_walmart_soup, check_walmart_url_status, extract_breadcrumbs, extract_product_data, \
    generate_error_data
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa


def process_walmart_url(walmart_url):
    w_soup_data = get_walmart_soup(walmart_url, driver_type='sb')
    w_page_status_, w_json_blob = check_walmart_url_status(w_soup_data)
    if w_page_status_ == 200:
        w_breadcrumbs_text = extract_breadcrumbs(w_soup_data, w_json_blob)
        w_product_data = extract_product_data(w_soup_data, w_json_blob, walmart_url)
        print(w_product_data)
    else:
        w_product_data = generate_error_data(walmart_url, w_page_status_)
        print(w_product_data)
    return w_product_data
