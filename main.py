import requests
import json
import config
import pandas as pd
import re
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
    similarity_score = 0.0

    # Product Name Matching
    similarity_score += 2 * get_cosine_sim_n(product_a["name"], product_b["name"])

    if product_a["specifications"] and product_b["specifications"]:
        spec_a_ = ' '.join([item["value"] for item in product_a["specifications"]])
        spec_a = spec_a_.join([item["key"] for item in product_a["specifications_b"]])
        spec_b = ' '.join([item["value"] for item in product_b["specifications"]])
        similarity_score += get_cosine_sim_n(spec_a, spec_b)

    return similarity_score / 3


def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)[0][1]


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer()
    return vectorizer.fit_transform(text).toarray()


def compare_products(product_a, product_b):
    similarity_score = 0

    # Brand Matching
    if product_a["brand"].lower() in product_b["name"].lower() or product_b["brand"].lower() in product_a[
        "name"].lower():
        similarity_score += 1

    # Product Name Matching
    if get_cosine_sim(product_a["name"], product_b["name"]) > 0.5:
        similarity_score += 1

    # Short Description Matching
    if isinstance(product_a["shortDescription"], list):
        short_desc_a = ' '.join(product_a["shortDescription"])
    else:
        short_desc_a = product_a["shortDescription"]
    if get_cosine_sim(short_desc_a, ' '.join(product_b["shortDescription"])) > 0.6:
        similarity_score += 1

    # Specification Matching
    spec_a = {item["key"]: item["value"] for item in product_a["specifications_b"]}
    spec_b = {item["key"]: item["value"] for item in product_b["specifications"]}

    matching_keys = set(spec_a.keys()) & set(spec_b.keys())
    for key in matching_keys:
        if spec_a[key].lower() == spec_b[key].lower():
            similarity_score += 1

    return similarity_score


def dump_the_data_to(p_data):
    try:
        with open('data.json', 'r') as fp:
            data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, list):
        data.append(p_data)
    elif isinstance(data, dict):
        data = [data, p_data]
    else:
        data = [p_data]

    with open('data.json', 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    amazon_urls = amazon_url_list_inc
    walmart_urls = walmart_url_list_inc
    # amazon_index = walmart_index = 20
    for i in range(len(amazon_urls)):
        amazon_index = walmart_index = i
        amazon_data, walmart_data = scrape_both(amazon_urls, walmart_urls, amazon_index, walmart_index)
        if amazon_data.get('url_status') == '200' and walmart_data.get('url_status') == '200':
            com_score = compare_products_n(amazon_data, walmart_data)
            print(com_score)
            data_ = {
                "amazon_product_id": amazon_data["id"],
                "walmart_product_id": walmart_data["id"],
                "amazon_data": amazon_data,
                "walmart_data": walmart_data,
                "com_score": com_score
            }
            dump_the_data_to(data_)

    # result = conduct_product_comparison(walmart_data, amazon_data)
    # print(result)
