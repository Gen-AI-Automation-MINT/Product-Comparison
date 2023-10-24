## Product Comparison Automation

Walmart Component:
Based on the previously provided Walmart scraping code, I'll create a detailed report of the components involved in the
Walmart scraping process.

## **Walmart Scraping**

### **1. Overview:**

The Walmart scraping mechanism focuses on extracting product information from Walmart product pages using web
scraping techniques, specifically with the assistance of Selenium and BeautifulSoup.

### **2. Components and Their Functions:**

**a. Initialization and Setup:**

- **WebDriver:** A Chrome WebDriver is initiated, which is crucial for controlling a Chrome browser session. It aids in
  navigating to web pages, interacting with elements, and extracting page content.
- **Browser Options:** The headless option ensures the Chrome browser runs in the background without a visible UI.

**b. Data Collection Methods:**

- **fetch_walmart_data:** The main function for obtaining data. It navigates to the provided URL, waits until the page
  is fully loaded, and then extracts the HTML content.

**c. Data/Attributes Extraction:**

- **get_product_name:** Extracts the product's name from the webpage.
- **get_short_description:** Retrieves a concise description of the product.
- **get_product_specifications:** Compiles a list of the product's specifications, which includes both the
  specification's key (e.g., "Color") and its value (e.g., "Black").
- **get_brand_name:** Extracts the brand name associated with the product.
- **get_manufacturer_name:** Determines the manufacturer's name for the product.
- **specifications:** All the Specification with `key` and `value`

**d. Data Structure:**

- The collected data is structured into a dictionary with the following keys:
    - **id**: A unique identifier for the product.
    - **name**: The product's name.
    - **shortDescription**: A brief description of the product.
    - **specifications**: A list of the product's specifications.
    - **brand**: The product's brand name.
    - **manufacturer**: The product's manufacturer's name.
    - **additionalInfo:** About the product
    - **url_status**: The status of the scraping request (e.g., "200" indicating a successful request).

### **3. Improvement:**

**a. Scalability:**

- If scraping numerous product pages, it's beneficial to introduce mechanisms like rotating user agents or employing
  proxies to avoid IP bans.

**b. Data Storage:**

- The data is presently returned as a dictionary. Depending on the scale of the scraping project, consider storing the
  data in a more scalable solution like a database.

**c. Rate Limiting:**

- Introducing delays between requests can prevent triggering anti-scraping measures on Walmart's side.

**d. Data Enrichment:**

- If more detailed data is required, consider scraping other sections of the product page or integrating external data
  sources.

---

## **Amazon Scraping**

### **1. Overview:**

The code extracts specific details from Amazon product pages using both Selenium WebDriver and direct HTTP requests,
then saves the scraped data to a JSON file.

### **2. Components and Their Functions:**

**a. Initialization and Constants:**

- **STATUS_MAP:** A dictionary used for mapping status codes to strings.

**b. Data Collection Methods:**

- **get_amazon_soup:** Obtains a BeautifulSoup object of the provided Amazon URL. It supports two methods for fetching
  the content:
    - **"uc"** (Undetected Chrome): Uses a Chrome WebDriver to navigate and get the page source.
    - **"re"** (Requests): Directly fetches the page using the requests module.

**c. Page Status Checks:**

- **check_amazon_url_status:** Identifies the status of a page based on its title or content. If a page is protected,
  flagged, or invalid, this method determines its status.

**d. Data Extraction Methods:**

- **extract_product_details:** Extracts specifications and information about the item, especially from the product facts
  toggle section.
- **extract_product_table:** Gathers additional product information from the product details table.
- **extract_product_data:** Extracts comprehensive product data, which includes details like the product title, brand,
  manufacturer, short description, and more.

**e. Data Storage:**

- **push_the_data_to_json:** This method appends extracted data to an existing JSON file, or if it doesn't exist,
  creates a new one.

**f. Error Management:**

- **generate_error_data:** Produces a dictionary with error data based on the URL and status. It's useful for logging
  failed scrape attempts.

### **3. Improvement:**

**a. Scalability:**

- Rotating user agents or employing proxies can aid in avoiding blocks or bans.

**b. Rate Limiting:**

- Introducing delays between requests to prevent triggering anti-scraping measures from Amazon.

**c. Data Verification:**

- After extraction, validate the data to ensure its accuracy and completeness.

**d. Update and Maintenance:**

- Amazon frequently updates its website structure. Regularly reviewing and updating the scraper is crucial to ensure its
  effectiveness.

---

### Main Without LLM:

The main file focuses on comparing the similarity of products retrieved from Amazon and Walmart. This similarity is
quantified using the cosine similarity metric applied to product attributes such as names, specifications, and short
descriptions. After comparing, the file stores the results, including similarity scores and product data, in JSON
format.

---

### Approach:

1. **Functions**:
    - `get_cosine_sim_n(str1, str2)`: Computes the cosine similarity between two input strings using the TF-IDF
      vectorization.

    - `compare_products_n(product_a, product_b)`: Computes the similarity score between two products based on their
      names, specifications, and short descriptions.

    - `get_vectors(*strs)`: Creates vectors from input strings using CountVectorizer.

    - `dump_the_data(p_data)` and `dump_the_score(p_data)`: These functions are responsible for appending data to
      JSON files. If the JSON file doesn't exist, it creates one. If the existing file has corrupted or incomplete JSON
      data, it reinitializes the data.

2. **Execution**:
    - Amazon and Walmart URLs are defined and then iterated over.
    - Products from both Amazon and Walmart are scraped using a function called `scrape_both` (which is not defined in
      the provided code but is presumably responsible for calling the scraping functions from the first context
      provided).
    - If the product details from both websites were successfully scraped, their similarity score is calculated.
    - All the scraped product data along with their similarity score is stored in 'data_new.json'.
    - Just the similarity score is stored separately in 'score_data.json'.

---

### Observations:

1. The main function retrieves product details for each URL from both Amazon and Walmart and compares them if the
   scraping was successful.

2. For comparison, it uses cosine similarity which is a metric to measure how similar two documents are, irrespective of
   their size.

3. Cosine similarity is used to compare the product name, combined product specifications, and short descriptions.

4. The final similarity score for each product pair is an average of these individual scores.

5. The results are saved in two JSON files. One (`data_new.json`) stores all the scraped data for both products and
   their similarity score. The other (`score_data.json`) stores only the product IDs and their similarity score.

---

Overall, the code takes a systematic approach to scrape product details, compare them, and store the results
efficiently. With a few refinements and optimizations, this script can be made even more robust and efficient.

Incorrect Match Score

```json
[
  {
    "amazon_product_id": "B01HVBTNR6",
    "walmart_product_id": "534200054",
    "similarity_score": 0.031164924991789054
  },
  {
    "amazon_product_id": "B01HVBTNR6",
    "walmart_product_id": "534200054",
    "similarity_score": 0.031164924991789054
  },
  {
    "amazon_product_id": "B09BLTKRJH",
    "walmart_product_id": "999541784",
    "similarity_score": 0.23510844232804232
  },
  {
    "amazon_product_id": "B099P34NZ2",
    "walmart_product_id": "999237347",
    "similarity_score": 0.13825799747926087
  },
  {
    "amazon_product_id": "B01N0SS24N",
    "walmart_product_id": "999072742",
    "similarity_score": 0.0835809830645944
  },
  {
    "amazon_product_id": "B092CVLMQM",
    "walmart_product_id": "998907103",
    "similarity_score": 0.15221745727400612
  },
  {
    "amazon_product_id": "0486474259",
    "walmart_product_id": "997560727",
    "similarity_score": 0.16213856534700008
  },
  {
    "amazon_product_id": "B0BG4BKG62",
    "walmart_product_id": "995631538",
    "similarity_score": 0.23365215568890954
  },
  {
    "amazon_product_id": "B088D2T69R",
    "walmart_product_id": "995160301",
    "similarity_score": 0.10311302556598667
  },
  {
    "amazon_product_id": "B0B1467KZG",
    "walmart_product_id": "995130589",
    "similarity_score": 0.08004915690805804
  },
  {
    "amazon_product_id": "B009OXCRZ0",
    "walmart_product_id": "995107701",
    "similarity_score": 0.14947416395079716
  },
  {
    "amazon_product_id": "B09873RKGF",
    "walmart_product_id": "994944506",
    "similarity_score": 0.18054020480555014
  },
  {
    "amazon_product_id": "B00407TTPG",
    "walmart_product_id": "994331679",
    "similarity_score": 0.09890853865888509
  },
  {
    "amazon_product_id": "B0C3GK39MX",
    "walmart_product_id": "993589130",
    "similarity_score": 0.0
  },
  {
    "amazon_product_id": "B089748PT1",
    "walmart_product_id": "993487154",
    "similarity_score": 0.12752171820814615
  },
  {
    "amazon_product_id": "B0BKDJ4KP6",
    "walmart_product_id": "991573351",
    "similarity_score": 0.15980377911142177
  },
  {
    "amazon_product_id": "B073S36M4B",
    "walmart_product_id": "991216057",
    "similarity_score": 0.1204674659405106
  },
  {
    "amazon_product_id": "B09W5X6W3F",
    "walmart_product_id": "990772899",
    "similarity_score": 0.14943304449402997
  },
  {
    "amazon_product_id": "B07J6FTCL1",
    "walmart_product_id": "990772462",
    "similarity_score": 0.15254138742321086
  },
  {
    "amazon_product_id": "B014WBYY2W",
    "walmart_product_id": "990679630",
    "similarity_score": 0.13147100373463186
  },
  {
    "amazon_product_id": "B0BMWFCSR2",
    "walmart_product_id": "990649765",
    "similarity_score": 0.1625257107692615
  },
  {
    "amazon_product_id": "B0C9XM5K7P",
    "walmart_product_id": "989600979",
    "similarity_score": 0.19544888189671902
  },
  {
    "amazon_product_id": "B08L8CYX73",
    "walmart_product_id": "988809045",
    "similarity_score": 0.2351777332256747
  },
  {
    "amazon_product_id": "B07X1WF8X2",
    "walmart_product_id": "988045818",
    "similarity_score": 0.17329970125362457
  },
  {
    "amazon_product_id": "B00794WUTY",
    "walmart_product_id": "987697210",
    "similarity_score": 0.048624796940188175
  },
  {
    "amazon_product_id": "B07RX6VM3B",
    "walmart_product_id": "986933098",
    "similarity_score": 0.0
  },
  {
    "amazon_product_id": "B09MFDC8G4",
    "walmart_product_id": "986369879",
    "similarity_score": 0.16194267129395096
  },
  {
    "amazon_product_id": "B0778F15T2",
    "walmart_product_id": "985494044",
    "similarity_score": 0.11272450763090518
  },
  {
    "amazon_product_id": "B07BFGZCX2",
    "walmart_product_id": "984387161",
    "similarity_score": 0.19146045165356604
  },
  {
    "amazon_product_id": "B093H18NYD",
    "walmart_product_id": "982988213",
    "similarity_score": 0.23726167371219611
  },
  {
    "amazon_product_id": "B09J4QHL6M",
    "walmart_product_id": "982907796",
    "similarity_score": 0.0
  }
]
```

---

### Passing to the LLM:

**Report on the Alternative Approach**

---

### Introduction:

The alternative approach focuses on comparing the similarity of products retrieved from Amazon and Walmart using the
Anyscale API, which appears to employ a model named `meta-llama/Llama-2-13b-chat-hf`. Instead of directly calculating
the similarity score, this approach feeds product data to an API endpoint, which then returns a model-generated
response.

---

### Approach:

1. **Functions**:
    - `get_products_data_from_json(amazon_json, walmart_json, index_element)`: Fetches product data from specified JSON
      files for Amazon and Walmart using an index.

    - `conduct_product_comparison(amazon_product, walmart_product)`: Sends the product data to Anyscale API, which
      returns the result of the comparison.

2. **Execution**:
    - The code reads product details for specified indexes from both Amazon and Walmart using the `scrape_both`
      function.
    - It then checks if both products were successfully scraped.
    - If so, the details of both products are sent to the Anyscale API, which returns a model-generated response.
    - The result is extracted from the API's response using regex and is then printed out along with the token usage
      details.

---

### Observations:

1. Instead of using cosine similarity for comparison, this approach relies on the Anyscale API. The exact workings of
   the API and the underlying model (`meta-llama/Llama-2-13b-chat-hf`) are not detailed, but it seems to return a string
   containing a JSON result.

2. The function `conduct_product_comparison` sends a request to the API, passing the product data in a structured
   format. This suggests that the API (and underlying model) require the data in a specific format to conduct the
   comparison.

3. After obtaining the response from the API, the code attempts to extract a JSON object from the string. This is done
   using the `extract_json_from_string` function, which employs a regular expression.

4. The usage of tokens (prompt tokens, completion tokens, and total tokens) is printed out at the end, suggesting that
   there may be a cost or limit associated with the number of tokens used in each API call.

---

Overall, this alternative approach offloads the comparison task to an external API, simplifying the code's logic. It
does, however, introduce reliance on a third-party service, which may have associated costs and potential downtime.
Properly managing these dependencies and understanding the API's specifics will be crucial for the successful deployment
and operation of this approach.


---
