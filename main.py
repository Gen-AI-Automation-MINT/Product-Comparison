import requests
import json
import config
import pandas as pd
import re
import time
import csv
from passing_to_llm import conduct_product_comparison
from generate_file import add_urls_to_excel, remove_duplicate_rows, output_file_no_duplicates
from process_urls import scrape_both
from llm_csv_gen import process_product, write_to_csv
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def get_cosine_sim(str1, str2):
    vectorizer = TfidfVectorizer().fit_transform([str1, str2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]


def compare_products(product_a, product_b):
    similarity_score_ = 0.0

    if product_a["name"] and product_b["name"]:
        cos_name_score = get_cosine_sim(product_a["name"], product_b["name"])
        similarity_score_ += cos_name_score
        print("\nProduct Name Matched", cos_name_score)

    if product_a["specifications"] and product_b["specifications"]:
        spec_a_ = ' '.join([item["value"] for item in product_a["specifications"]])
        spec_a = spec_a_.join([item["key"] for item in product_a["specifications_b"]])
        spec_b = ' '.join([item["value"] for item in product_b["specifications"]])
        similarity_score_ += get_cosine_sim(spec_a, spec_b)
        print("Specification Matched", get_cosine_sim(spec_a, spec_b))

    if product_a["shortDescription"] and product_b["shortDescription"]:
        short_desc_a = ' '.join(product_a["shortDescription"])
        short_desc_b = ' '.join(product_b["shortDescription"])
        similarity_score_ += get_cosine_sim(short_desc_a, short_desc_b)
        print("Short Description Matched", get_cosine_sim(short_desc_a, short_desc_b))

    return similarity_score_ / 3


def dump_the_data_to(p_data):
    try:
        with open('output_files/product_data.json', 'r') as fp:
            data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, list):
        data.append(p_data)
    elif isinstance(data, dict):
        data = [data, p_data]
    else:
        data = [p_data]

    with open('data_exa.json', 'w') as fp:
        json.dump(data, fp, indent=4)


def dump_the_score_to(p_data):
    try:
        with open('output_files/score_data_exa.json', 'r') as fp:
            data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, list):
        data.append(p_data)
    elif isinstance(data, dict):
        data = [data, p_data]
    else:
        data = [p_data]

    with open('output_files/score_data_exa.json', 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    amazon_url_list = []
    walmart_url_list = []

    try:
        with open(output_file_no_duplicates, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                if 'walmart_url' in row and 'comp_url' in row:
                    walmart_url_list.append(row['walmart_url'])
                    amazon_url_list.append(row['comp_url'])
                else:
                    print("Warning: Missing expected keys in row")

    except FileNotFoundError:
        print("Error: The file 'input_files/urls.csv' was not found.")

    print(f"Will be Processing:  Walmart URLs: {len(walmart_url_list)} |  Amazon URLs: {len(amazon_url_list)}")
    for i in range(len(walmart_url_list)):
        print(f"Index URL no: {i + 1}")
        amazon_index = walmart_index = i
        amazon_data, walmart_data = scrape_both(amazon_url_list, walmart_url_list, amazon_index, walmart_index)

        if amazon_data.get('url_status') == '200' and walmart_data.get('url_status') == '200':
            amazon_id = amazon_data.get('id')
            az_llm_response = process_product(amazon_data)
            if az_llm_response:
                llm_response_dict = json.loads(az_llm_response)
                llm_response_dict['id'] = amazon_id
                write_to_csv('output_files/az_attribute.csv', llm_response_dict)
            print("Waiting for next request...")
            for j in range(20, 0, -1):
                print(f"Loading... {j} seconds remaining")
                time.sleep(1)
            print("\n")

            walmart_id = walmart_data.get('id')
            wm_llm_response = process_product(walmart_data)
            if wm_llm_response:
                llm_response_dict = json.loads(wm_llm_response)
                llm_response_dict['id'] = walmart_id
                write_to_csv('output_files/wm_attribute.csv', llm_response_dict)
            print("Waiting for next request...")
            for j in range(20, 0, -1):
                print(f"Loading... {j} seconds remaining")
                time.sleep(1)
            print("\n")
            data_ = {
                "amazon_product_id": amazon_data["id"],
                "walmart_product_id": walmart_data["id"],
                "amazon_data": amazon_data,
                "walmart_data": walmart_data,
            }
            dump_the_data_to(data_)
