import requests
import json
import config
import pandas as pd
import re
import csv
from passing_to_llm import conduct_product_comparison
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from process_urls import scrape_both
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def get_cosine_sim_n(str1, str2):
    vectorizer = TfidfVectorizer().fit_transform([str1, str2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]


def compare_products_n(product_a, product_b):
    similarity_score_ = 0.0

    if product_a["name"] and product_b["name"]:
        cos_name_score = get_cosine_sim_n(product_a["name"], product_b["name"])
        similarity_score_ += cos_name_score
        print("\nProduct Name Matched", cos_name_score)

    if product_a["specifications"] and product_b["specifications"]:
        spec_a_ = ' '.join([item["value"] for item in product_a["specifications"]])
        spec_a = spec_a_.join([item["key"] for item in product_a["specifications_b"]])
        spec_b = ' '.join([item["value"] for item in product_b["specifications"]])
        similarity_score_ += get_cosine_sim_n(spec_a, spec_b)
        print("Specification Matched", get_cosine_sim_n(spec_a, spec_b))

    if product_a["shortDescription"] and product_b["shortDescription"]:
        short_desc_a = ' '.join(product_a["shortDescription"])
        short_desc_b = ' '.join(product_b["shortDescription"])
        similarity_score_ += get_cosine_sim_n(short_desc_a, short_desc_b)
        print("Short Description Matched", get_cosine_sim_n(short_desc_a, short_desc_b))

    return similarity_score_ / 3


def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)[0][1]


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer()
    return vectorizer.fit_transform(text).toarray()


def compare_products(product_a, product_b):
    similarity_score_ = 0

    # Brand Matching
    if product_a["brand"].lower() in product_b["name"].lower() or product_b["brand"].lower() in product_a[
        "name"].lower():
        similarity_score_ += 1
        print("Brand Matched")

    # Product Name Matching
    if get_cosine_sim(product_a["name"], product_b["name"]) > 0.5:
        similarity_score_ += 1
        print("Product Name Matched", get_cosine_sim(product_a["name"], product_b["name"]))

    # Short Description Matching
    if isinstance(product_a["shortDescription"], list):
        short_desc_a = ' '.join(product_a["shortDescription"])
    else:
        short_desc_a = product_a["shortDescription"]
    if get_cosine_sim(short_desc_a, ' '.join(product_b["shortDescription"])) > 0.6:
        similarity_score_ += 1

    # Specification Matching
    spec_a = {item["key"]: item["value"] for item in product_a["specifications_b"]}
    spec_b = {item["key"]: item["value"] for item in product_b["specifications"]}

    matching_keys = set(spec_a.keys()) & set(spec_b.keys())
    for key in matching_keys:
        if spec_a[key].lower() == spec_b[key].lower():
            similarity_score_ += 1

    return similarity_score_


def dump_the_data_to(p_data):
    try:
        with open('data_exa.json', 'r') as fp:
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
        with open('score_data_exa.json', 'r') as fp:
            data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, list):
        data.append(p_data)
    elif isinstance(data, dict):
        data = [data, p_data]
    else:
        data = [p_data]

    with open('score_data_exa.json', 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    amazon_urls = amazon_url_list_inc
    walmart_urls = walmart_url_list_inc
    walmart_url_exact = []
    comp_url_exact = []
    walmart_url_incorrect = []
    comp_url_incorrect = []
    with open('input_files/urls.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Match_Type'] == 'Exact Match':
                walmart_url_exact.append(row['Walmart_Url'])
                comp_url_exact.append(row['Comp_Url'])
            if row['Match_Type'] == 'Incorrect Match':
                walmart_url_incorrect.append(row['Walmart_Url'])
                comp_url_incorrect.append(row['Comp_Url'])
    print("Will be Processing: ", len(walmart_url_exact), len(comp_url_exact))
    for i in range(len(comp_url_exact)):
        print(f"Index: {i}")
        amazon_index = walmart_index = i
        amazon_data, walmart_data = scrape_both(comp_url_exact, walmart_url_exact, amazon_index, walmart_index)
        if amazon_data.get('url_status') == '200' and walmart_data.get('url_status') == '200':
            similarity_score = compare_products_n(amazon_data, walmart_data)

            print(f"Final Score: {similarity_score}")
            data_ = {
                "amazon_product_id": amazon_data["id"],
                "walmart_product_id": walmart_data["id"],
                "amazon_data": amazon_data,
                "walmart_data": walmart_data,
                "similarity_score": similarity_score
            }
            dump_the_data_to(data_)

            score_data = {
                "amazon_product_id": amazon_data["id"],
                "walmart_product_id": walmart_data["id"],
                "similarity_score": similarity_score
            }
            dump_the_score_to(score_data)

    # result = conduct_product_comparison(walmart_data, amazon_data)
    # print(result)
