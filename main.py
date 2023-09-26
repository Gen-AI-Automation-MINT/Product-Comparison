import requests
import json
import config
import pandas as pd

token = config.anyscale_api_key

with open('amazon_full.json') as f:
    amazon_data = json.load(f)

with open('walmart_full.json') as f:
    walmart_data = json.load(f)

s = requests.Session()

api_base = "https://api.endpoints.anyscale.com/v1"
url = f"{api_base}/chat/completions"

for i in range(0, 2):
    input(f"Press enter to continue... {i}")
    if walmart_data[i]['name'] != None and amazon_data[i]['name'] != None:
        walmart_product = walmart_data[i]
        amazon_product = amazon_data[i]
        print(walmart_product, amazon_product)
        user_content = f"I am providing the JSON data of two products here. Walmart Product = {walmart_product} | Amazon Product = {amazon_product} Your task is to conduct a detailed attribute comparison between the two products, focusing on the following key aspects: Product Name, Brand, Short Description, and Additional Attributes (such as Color, Material, Cost, and Type). Subsequently, present the matching details for my analysis. Your output should deliver a detailed breakdown of the matching attributes, facilitating in-depth analysis."
        print("\n\n\n")
        print(user_content)
        body = {
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "messages": [
                {"role": "system", "content": "You are an expert in NLP and understanding the json data of products."},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.5
        }
        resp = s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body)
        print(resp)
        print(resp.status_code)
        print(resp.json()['choices'][0]['message']['content'])
        print("\n\n\n")