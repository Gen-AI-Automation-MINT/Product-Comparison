import csv
import json
import pandas as pd

input_file = "input_files/Sample_Output_2510.xlsx"
json_file = "score_data.json"


def extract_urls_to_csv(input_file_):
    df = pd.read_excel(input_file_)
    df = df[['Item_Id', 'Retailer_Id', 'Walmart_Url', 'Comp_Url', 'Match_Type']]
    df.to_csv("input_files/urls.csv", index=False)
    print("URLs extracted to urls.csv")


def extract_urls(input_csv_file):
    walmart_url = []
    comp_url = []

    with open(input_csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Match_Type'] == 'Exact Match':
                walmart_url.append(row['Walmart_Url'])
                comp_url.append(row['Comp_Url'])

    return walmart_url, comp_url


if __name__ == "__main__":
    with open(json_file, 'r') as fp:
        json_data = json.load(fp)
    output_csv_file = 'incorrect_match_output.csv'
    with open(output_csv_file, 'w', newline='') as csv_file:
        fieldnames = ['Item_Id', 'Retailer_Id', 'Walmart_Url', 'Comp_Url', 'Similarity_Score', 'Match_Type',
                      "Match_Type_by_human"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for data in json_data:
            item_id = data['amazon_product_id']
            retailer_id = data['walmart_product_id']
            similarity_score = data['similarity_score']

            if similarity_score < 0.3:
                match_type = 'Incorrect Match'
            else:
                match_type = 'NA'

            csv_writer.writerow({
                'Item_Id': item_id,
                'Retailer_Id': retailer_id,
                'Walmart_Url': f'https://www.walmart.com/{retailer_id}',
                'Comp_Url': f'https://www.example.com/{item_id}',
                'Similarity_Score': similarity_score,
                'Match_Type': match_type,
                'Match_Type_by_human': "Incorrect Match"
            })
