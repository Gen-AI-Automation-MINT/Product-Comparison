from walmart_main import get_walmart_soup, check_walmart_url_status, extract_breadcrumbs, extract_product_data
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa

output_file_no_duplicates = "../output_files/output_file_no_duplicates.csv"

walmart_urls = ['https://www.walmart.com/ip/999541784?selected=true',
                "https://www.walmart.com/ip/996900990?selected=true",
                "https://www.walmart.com/ip/925123195?selected=true",
                "https://www.walmart.com/ip/314409680?selected=true",
                "https://www.walmart.com/ip/158741871?selected=true",
                "https://www.walmart.com/ip/109999521?selected=true",
                "https://www.walmart.com/ip/755983708?selected=true"]

if __name__ == "__main__":
    walmart_url = walmart_url_list_exa[0]
    print("Scraping Started\n")
    # for walmart_url in walmart_url_list_exa:
    soup_data = get_walmart_soup(walmart_url, driver_type='uc')
    page_status_, json_blob = check_walmart_url_status(soup_data)
    if page_status_ == 200:
        breadcrumbs_text = extract_breadcrumbs(soup_data, json_blob)
        product_data = extract_product_data(soup_data, json_blob, walmart_url)
        print(product_data)
