import json


def prompt_generator(walmart_product, amazon_product):
    user_content1 = f"""
   I am providing the JSON data of two products here.
   Walmart Product = {walmart_product}
   Amazon Product = {amazon_product}
   Your task is to conduct a detailed attribute comparison between the two products, focusing on the following key aspects:
   Product Name, Brand, Short Description, and Additional Attributes (such as Color, Material, Cost, and Type).
   Subsequently, present the matching details for my analysis. Your output should deliver a detailed breakdown of the 
   matching attributes, facilitating in-depth analysis. Additionally, provide the percentage match for easier reference. 
   Justify the percentage match by providing a detailed explanation of the matching attributes.
   """.strip()

    user_content2 = f"""
    I am providing the JSON data of two products here.
    Walmart Product = {walmart_product}
    Amazon Product = {amazon_product}
    Your task is to conduct a detailed attribute comparison between the two products, focusing on the following on all the aspects.
    AND GENERATE THE JSON DATA IN THE FORMATE OF THE GIVEN EXAMPLE.
    Different match types:
    1.Exact Match
    2.Incorrect Match
    3.Not Sure
    The rule is that if the attribute is matched exactly, then the match type is "Exact Match". If the attribute is not matched, then the match type is "Incorrect Match". If the attribute is matched but not sure, then the match type is "Not Sure".
    EXAMPLE: {{"walmart_product_id": "123", "amazon_product_id": "123", "match_type": "Exact Match"}}
    Your Response should be in the form of JSON data.
    No need of labeling the match type for all the each attributes individually. Just label the match type for the entire product.
    """.strip()

    user_content3 = f"""
        "Using the provided JSON data, compare the attributes of two products from Walmart (WM) and a competitor (Comp).
        **Provided Data**:
        - Walmart Product: {walmart_product}
        - Amazon Product: {amazon_product}
        **Comparison Criteria**:
        - **Exact Match**: Both products have the exact same attribute.
        - **Not Sure Match**:
            - Examine all listed attributes in both WM and Comp.
            - If 2 or more values are absent in either, flag the match type as "Not Sure".
        - **Incorrect Match**:
            - Disregard values from the Brand and Title.
            - Focus on mismatches in Model, Size, Color, Pack/Count between WM & Comp.
            - If 2 or more attributes mismatch: Flag as "Strong Incorrect".
            - If fewer than 2 attributes mismatch: Flag as "Weak Incorrect".
        **Example Output**:
        ```json
        {{"walmart_product_id": "000",
          "amazon_product_id": "000",
          "match_type": "Exact Match"
        }}
        ```
        **Note**: Provide a singular match type for the entire product comparison, rather than individual attributes. Your response should be in JSON format.
    """.strip()

    message_role_content = "You are an expert understanding the JSON data. I am conducting an Product comparison. Take a deep breath before you start. YOUR RESPONSE WILL BE ONLY IN THE FORM OF JSON DATA."

    return user_content3, message_role_content


def get_products_data_from_json(amazon_json, walmart_json, index_element):
    with open(amazon_json, 'r') as f:
        amazon_data_ = json.load(f)
        a_el_data = amazon_data_[index_element]
    with open(walmart_json, 'r') as f:
        walmart_data_ = json.load(f)
        w_el_data = walmart_data_[index_element]
    return a_el_data, w_el_data


if __name__ == "__main__":
    amazon_json_path = "./amazon/amazon_data.json"
    walmart_json_path = "./walmart/walmart_data.json"
    amazon_data, walmart_data = get_products_data_from_json(amazon_json_path, walmart_json_path, 0)
    user_content, message_role_content = prompt_generator(amazon_data, walmart_data)
    print(user_content)
    print(message_role_content)
