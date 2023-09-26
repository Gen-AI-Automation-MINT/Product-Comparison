from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

amazon_url_list = [
    "https://www.amazon.com/dp/B075NSQ7LY?th=1&psc=1",
    "https://www.amazon.com/dp/B089GMJ8RS?th=1&psc=1",
    "https://www.amazon.com/dp/B07L2MW2VK?th=1&psc=1",
    "https://www.amazon.com/dp/B00K1PBYKE?th=1&psc=1",
    "https://www.amazon.com/dp/B00L76QUAK?th=1&psc=1",
    "https://www.amazon.com/dp/B072BC9LQG?th=1&psc=1",
    "https://www.amazon.com/dp/B089SPJZJW?th=1&psc=1",
    "https://www.amazon.com/dp/B07Q8RTRW3?th=1&psc=1",
    "https://www.amazon.com/dp/B099K1DP9P?th=1&psc=1",
    "https://www.amazon.com/dp/B00IKVS79C?th=1&psc=1",
    "https://www.amazon.com/dp/B00OEJZKIK?th=1&psc=1",
    "https://www.amazon.com/dp/B0B3XRT96M?th=1&psc=1",
    "https://www.amazon.com/dp/B007YT34VM?th=1&psc=1",
    "https://www.amazon.com/dp/B07VVMHHMP?th=1&psc=1",
    "https://www.amazon.com/dp/B00745BUGW?th=1&psc=1",
    "https://www.amazon.com/dp/B00B37ERSU?th=1&psc=1",
    "https://www.amazon.com/dp/B07MY8PWHN?th=1&psc=1",
    "https://www.amazon.com/dp/B08YZBK7N5?th=1&psc=1",
    "https://www.amazon.com/dp/B07SQL5L8W?th=1&psc=1",
]

walmart_url_list = [
    "https://www.walmart.com/ip/466185717?selected=true",
    "https://www.walmart.com/ip/1286642938?selected=true",
    "https://www.walmart.com/ip/736755300?selected=true",
    "https://www.walmart.com/ip/158741871?selected=true",
    "https://www.walmart.com/ip/925123195?selected=true",
    "https://www.walmart.com/ip/109999521?selected=true",
    "https://www.walmart.com/ip/314409680?selected=true",
    "https://www.walmart.com/ip/755983708?selected=true",
    "https://www.walmart.com/ip/674290295?selected=true",
    "https://www.walmart.com/ip/288150096?selected=true",
    "https://www.walmart.com/ip/377111281?selected=true",
    "https://www.walmart.com/ip/332498618?selected=true",
    "https://www.walmart.com/ip/116481628?selected=true",
    "https://www.walmart.com/ip/135821061?selected=true",
    "https://www.walmart.com/ip/931359?selected=true",
    "https://www.walmart.com/ip/1182714231?selected=true",
    "https://www.walmart.com/ip/666004175?selected=true",
    "https://www.walmart.com/ip/614858163?selected=true",
    "https://www.walmart.com/ip/937248769?selected=true",
]


def scrape_amazon_url(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            print("Scraping URL:", driver.current_url)
            print("Scraped Title:", driver.title)
            title_element = driver.find_element(By.XPATH, "//*[@id='title']")
            brand_name_element = driver.find_element(By.XPATH, "//*[@id='bylineInfo']")
            title = title_element.text.strip()
            brand_name = brand_name_element.text.strip()

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            about_item = []
            for items in soup.find_all("li", attrs={'class': 'a-spacing-mini'}):
                about_item.append(items.text.strip())
            return {
                'URL': url,
                'Page Title': title,
                'Brand Name': brand_name,
                'About Item': about_item,
            }
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None


def scrape_walmart_url(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            print("Page URL:", driver.current_url)
            print("Page Title:", driver.title)
            title_element = driver.find_element(By.XPATH, "//*[@id='product-overview']/div[1]/div[1]/h1")
            brand_name_element = driver.find_element(By.XPATH,
                                                     "//*[@id='product-overview']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")
            title = title_element.text.strip()
            brand_name = brand_name_element.text.strip()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            about_item = []
            for items in soup.find_all("li", attrs={'class': 'a-spacing-mini'}):
                about_item.append(items.text.strip())
            return {
                'URL': url,
                'Page Title': title,
                'Brand Name': brand_name,
                'About Item': about_item,
            }
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None


# scraped_data = [scrape_amazon_url(url) for url in amazon_url_list]
scraped_data = [scrape_amazon_url(amazon_url_list[2])]

print("\nScraped Data:")
for data in scraped_data:
    if data:
        print(f"URL: {data['URL']}")
        print(f"Page Title: {data['Page Title']}")
        print(f"Brand Name: {data['Brand Name']}\n")
        print(f"About the item: {data['About Item']}")
        # for bullets in data['About Item']:
        #     print(bullets)
