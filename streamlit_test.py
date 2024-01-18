from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from amazon.amazon_test import process_amazon_url
from walmart.walmart_test import process_walmart_url
import json
import streamlit as st
st.set_page_config(layout="wide")

# amazon_url_ = st.text_area("Amazon URL", amazon_url_)
# walmart_url_ = st.text_area("Walmart URL", walmart_url_)
amazon_index = walmart_index = st.number_input("Index", min_value=0, max_value=100, value=0)
walmart_url_ = walmart_url_list_exa[amazon_index]
amazon_url_ = amazon_url_list_exa[walmart_index]

process = st.button("Process")
st.write("Amazon URL: ", amazon_url_)
st.write("Walmart URL: ", walmart_url_)

if process:
    print("Test Scraping Started\n")
    a_product_data = process_amazon_url(amazon_url_)
    w_product_data = process_walmart_url(walmart_url_)
    col1, col2 = st.columns(2)
    with col1:
        st.write("Amazon Data\n")
        st.write(a_product_data)
    with col2:
        st.write("Walmart Data\n")
        st.write(w_product_data)
