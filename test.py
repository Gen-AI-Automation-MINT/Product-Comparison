import json
import requests

f = open('walmart_full.json', 'r')
data = json.load(f)

raw_product_data = data["props"]["pageProps"]["initialData"]["data"]["product"]

print(data["props"]["pageProps"]["initialData"]["data"]['idml'].get('specifications'))

f.close()
