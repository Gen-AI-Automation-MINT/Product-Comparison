import pandas as pd
import json

df = pd.read_csv('data.csv')
with open('amazon_full.json') as f:
    amazon_data = json.load(f)

with open('walmart_full.json') as f:
    walmart_data = json.load(f)

walmart_url = df['Walmart_Url']
amazon_url = df['Comp_Url']

walmart_url = walmart_url[1:]
amazon_url = amazon_url[1:]

walmart_url = walmart_url.to_list()
amazon_url = amazon_url.to_list()

for i in range(len(walmart_data)):
    if walmart_data[i]['type'] != None and amazon_data[i]['type'] != None:
        walmart_product = walmart_data[i]
        amazon_product = amazon_data[i]


