from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def scrape_amazon_url(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
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


# List of URLs to scrape
url_list = [
    "https://www.amazon.com/dp/B075NSQ7LY?th=1",
    "https://www.amazon.com/dp/B07L2N4QD6?th=1",
    "https://www.walmart.com/ip/466185717?selected=true"
]

# scraped_data = [scrape_amazon_url(url) for url in url_list]
scraped_data = [scrape_amazon_url(url_list[1])]

print("\nScraped Data:")
for data in scraped_data:
    if data:
        print(f"URL: {data['URL']}")
        print(f"Page Title: {data['Page Title']}")
        print(f"Brand Name: {data['Brand Name']}\n")
        for bullets in data['About Item']:
            print(bullets)
