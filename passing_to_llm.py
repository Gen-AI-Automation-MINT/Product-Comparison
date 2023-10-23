import requests
import config
import json
import re
from test_data import amazon_url_list_404, walmart_url_list_404, walmart_url_list_inc, amazon_url_list_inc, \
    walmart_url_list_exa, amazon_url_list_exa
from process_urls import scrape_both
from llm_prompt import prompt_generator

amazon_json_path = "./amazon/amazon_data.json"
walmart_json_path = "./walmart/walmart_data.json"


def get_products_data_from_json(amazon_json, walmart_json, index_element):
    with open(amazon_json, 'r') as f:
        amazon_data_ = json.load(f)
        a_el_data = amazon_data_[index_element]
    with open(walmart_json, 'r') as f:
        walmart_data_ = json.load(f)
        w_el_data = walmart_data_[index_element]
    return a_el_data, w_el_data


def conduct_product_comparison(amazon_product, walmart_product):
    print("\n\nPassing data to Anyscale API")
    content, message_role_content = prompt_generator(amazon_product, walmart_product)
    user_content = f"{content}"
    api_base = "https://api.endpoints.anyscale.com/v1"
    url = f"{api_base}/chat/completions"
    token = config.anyscale_api_key
    s = requests.Session()

    payload = {
        "model": "meta-llama/Llama-2-13b-chat-hf",
        "messages": [
            {"role": "system",
             "content": f"{message_role_content}"},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.1
    }

    try:
        resp = s.post(url, headers={"Authorization": f"Bearer {token}"}, json=payload)

        if resp.status_code == 200:
            response_data = resp.json()
            response_content_ = response_data['choices'][0]['message']['content']
            usage_ = response_data.get('usage', {})

            return response_content_, usage_
        else:
            return f"Error: Anyscale API request failed with status code {resp.status_code}"

    except Exception as e:
        return f"Error: {str(e)}"


def extract_json_from_string(s):
    pattern = r"\{.*?\}"
    match = re.search(pattern, s, re.DOTALL)  # re.DOTALL makes . match newline as well

    if match:
        json_str = match.group()
        return json.loads(json_str)
    return None


if __name__ == "__main__":
    amazon_urls = amazon_url_list_exa
    walmart_urls = walmart_url_list_exa
    amazon_index = walmart_index = 4
    amazon_data, walmart_data = scrape_both(amazon_urls, walmart_urls, amazon_index, walmart_index)
    # amazon_data, walmart_data = get_products_data_from_json(amazon_json_path, walmart_json_path, amazon_index)

    if amazon_data.get('url_status') != '200' and walmart_data.get('url_status') != '200':
        print("Both URLs are not valid")
        exit(1)
    response_content, usage = conduct_product_comparison(amazon_data, walmart_data)
    print("LLM Response: \n", response_content)
    result = extract_json_from_string(response_content)
    print("Result:", result)
    formated_usage = f"Prompt Tokens: {usage['prompt_tokens']} | Completion Tokens: {usage['completion_tokens']} | Total Tokens: {usage['total_tokens']}"
    print("Usage: ", formated_usage)
