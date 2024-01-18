from openai import OpenAI
import json
import csv
import time
from config import open_ai_api_key

client = OpenAI(api_key=open_ai_api_key)

system_prompt = """
You will be provided with json data of an ecommerce product, and your task is to extract only these attributes - [title, brand, model, size, color, pack/count, material] from it and generate JSON output. 
The output should be in the following format:
{
    "title": "product title",
    "brand": "product brand",
    "model": "product model",
    "size": "product size or dimensions",
    "color": "product color",
    "pack_count": "number of items or pack count",
    "material": "product material"
}
"""


def process_product(product_data):
    user_prompt = f"Here is the product details: \n{json.dumps(product_data, indent=2)}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        token_usage = response.usage.total_tokens
        json_response = response.choices[0].message.content
        print(json_response)
        print(f"Total tokens used: {token_usage}")
        return json_response

    except Exception as e:
        print(f"Error generating output for product: {product_data}")
        print(e)
        return None


def write_to_csv(file_path, json_data):
    headers = ["id", "title", "brand", "model", "size", "color", "pack_count", "material"]
    try:
        with open(file_path, 'x', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerow(json_data)
    except FileExistsError:
        with open(file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerow(json_data)


def main():
    with open('amazon/amazon_data.json', 'r') as file:
        product_details = json.load(file)
        az_output_file = 'llm_output.csv'
    with open('walmart/walmart_data.json', 'r') as file:
        product_details = json.load(file)
        wm_output_file = 'llm_output.csv'
    output_file = 'llm_output.csv'

    for product in product_details:
        if int(product.get('url_status')) == 200:
            result = process_product(product)
            if result:
                result_dict = json.loads(result)
                write_to_csv(output_file, result_dict)
            print("Waiting for next request...")
            for i in range(20, 0, -1):
                print(f"Loading... {i} seconds remaining", )
                time.sleep(1)
            print("\n")


if __name__ == "__main__":
    main()
