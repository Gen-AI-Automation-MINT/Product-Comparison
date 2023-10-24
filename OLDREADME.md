
### Product Comparison Task Assessment Report

##### Introduction

This report presents the methodology, findings, and analysis of a product comparison task. The
primary objective was to compare two products, one from Amazon and one from Walmart, and
determine whether they are the same or not. The task involved data scraping, attribute extraction,
and leveraging a Language Model for similarity assessment.
Methodology

1. Data Collection
   To collect data from Amazon and Walmart, I used Python's requests library to fetch product
   information from the respective websites. I used a headless Chrome browser to access the data
   seamlessly.
   I used Beautiful Soup for accessing specific tags. I have also implemented anti-bot bypassing logic to
   provide a proxy header since both the webpage have Anti-Bot Protection. (ScrapeOps Proxy
   Aggregator )
2. Data Extraction
   I extracted product attributes, including:

* Product Name
* Brand
* Short Description
* Other Attributes (Colour, Material, Cost, Type)
  The code effectively collected these attributes from both Amazon and Walmart product pages.

3. Language Model Interaction
   I used the Language Model "meta-llama/Llama-2-70b-chat-hf" to assess the similarity between the
   two products. The following prompt was used:

```py
llm_prompt = """ 
I am providing the JSON data of two products here. Your task is to conduct a detailed attribute 
comparison between the two products, focusing on the following key aspects: Product Name, Brand, 
Short Description, and Additional Attributes (such as Color, Material, Cost, and Type). Subsequently, 
present the matching details for my analysis. Your output should deliver a detailed breakdown of the 
matching attributes, facilitating in-depth analysis.
"""
```

Code for language model interaction not shown for brevity.
Scraping Results
• Product 1 (Amazon):

```json
{
  "url": "https://www.amazon.com/dp/B075NSQ7LY?th=1&psc=1",
  "type": "product",
  "name": "GorgeousHomeLinen (N25) 2 Solid Faux Silk Bronze Grommet Curtain Panels for Small Windows (Charcoal)",
  "brand": "Brand: Gorgeous Home LINEN",
  "shortDescription": "These 2 Pieces Set Window Curtain Panels will look great in  the kitchen, bedroom, bathroom, laundry room, basemen or SIZE 'W x 36'H Each. The panels feature an attractive unique fabric very",
  "specifications": [
    {
      "name": "Brand",
      "value": "Gorgeous Home LINEN"
    },
    {
      "name": "Color",
      "value": "Charcoal"
    },
    {
      "name": "Material",
      "value": "Faux Silk"
    },
    {
      "name": "Opacity",
      "value": "Blackout"
    }
  ]
}
```

• Product 1 (Walmart): {

```json
{
  "url": "https://www.walmart.com/ip/466185717?selected=true",
  "type": "Curtains & Valances",
  "name": "2 Piece N25 CHARCOAL Luxury Kitchen, Short Window Curtain Semi Sheer Panel, 2 Faux Silk Tier Panels With Bronze Grommets",
  "brand": "SAMIMPORT-2011",
  "shortDescription": "2 Piece Semi Sheer Bronze Antique Grommet Kitchen Window Curtain Set Includes: 2 Faux Silk Tier Panels Size 30\"Wide X 36\"Length (Each Tier)Same color Front & Back You can See Thru Perfect for Summer Weather Provide our Area Fresh, Clean and Fancy",
  "specifications": [
    {
      "name": "Material",
      "value": "Polyester"
    },
    {
      "name": "Curtain Panel Style",
      "value": "Grommet"
    },
    {
      "name": "Brand",
      "value": "SAMIMPORT-2011"
    },
    {
      "name": "Color",
      "value": "Bronze, Gray"
    },
    {
      "name": "Price",
      "value": "$10 USD"
    }
  ]
}
```

* Language Model Response:
* The language model provided the following response to determine product
  similarity:
  Comparison of Key Aspects:

1. Product Name:

* Walmart Product: 2 Piece N25 CHARCOAL Luxury Kitchen, Short Window Curtain Semi
  Sheer Panel, 2 Faux Silk Tier Panels with Bronze Grommets
* Amazon Product: GorgeousHomeLinen (N25) 2 Solid Faux Silk Bronze Grommet Curtain
  Panels for Small Windows (Charcoal)

2. Brand:

* Walmart Product: SAMIMPORT-2011
* Amazon Product: Brand: Gorgeous Home LINEN

3. Short Description:

* Walmart Product: 2 Piece Semi Sheer Bronze Antique Grommet Kitchen Window Curtain
  Set Includes: 2 Faux Silk Tier Panels Size 30"Wide X 36"Length (Each Tier) Same color Front & Back
  You can See Through Perfect for Summer Weather Provide Your Area Fresh, Clean and Fancy
* Amazon Product: These 2 Pieces Set Window Curtain Panels will look great in the kitchen,
  bedroom, bathroom, laundry room, basement or any window in the house. SIZE: 30"W x 36"H Each.
  The panels feature an attractive unique fabric very modern. Panels have bronze grommet opening for
  easy hanging. Good quality finishing will with stand years of use.

4. Additional Attributes:

* Walmart Product:

+ Material: Polyester
+ Curtain Panel Style: Grommet
+ Color: Bronze, Gray
+ Price: $10 USD

* Amazon Product:

+ Brand: Gorgeous Home LINEN
+ Color: Charcoal
+ Material: Faux Silk
+ Opacity: Blackout
+ Special Feature: blackout
  Based on the comparison above, the two products have some similarities and differences:
  Similarities:

* Both products are curtain panels for windows.
* Both products have bronze grommets for easy hanging.
* Both products have a modern and unique fabric design.
  Differences:
* Product names and brands are different.
* The short descriptions of the products highlight different features. The Walmart product
  emphasizes the semi-sheer and see-through feature, while the Amazon product highlights the
  modern and unique fabric design.
* The Amazon product has additional attributes such as color (Charcoal), material (Faux Silk), opacity
  (blackout), and special feature (blackout).
  Discussion
  Based on the data extracted and the response from the Language Model, we observed that the
  model identified specific attributes, such as brand/seller, model, color, material, size, and exact
  match, as criteria for assessing product similarity. However, further analysis is required to conclude
  whether the products from Amazon and Walmart are indeed the same based on these attributes.

#### Conclusion

In conclusion, this report outlines the methodology and results of a product comparison task
between Amazon and Walmart products. While we successfully collected and extracted relevant
attributes, the determination of product similarity requires more in-depth analysis. The Language
Model's response provides a starting point for assessment, but additional steps may be necessary for
a definitive conclusion.
Recommendations
It is recommended to conduct a more comprehensive analysis, possibly incorporating advanced
Natural Language Processing (NLP) techniques, to enhance the accuracy of product similarity
assessment. Additionally, considering user reviews and ratings could provide valuable insights into
product equivalency.

#### Appendix

* The code used for data collection and extraction can be found in the provided google colab
  link: [product_comparison_llm.ipynb](https://colab.research.google.com/drive/1N4BqINdOmxokVfmGYeAJa01J7ynrkwLB?usp=sharing)
* Additional data samples are saved as json file. Will present based on request