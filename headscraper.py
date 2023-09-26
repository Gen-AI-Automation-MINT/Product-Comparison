from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url_list = [
    "https://www.amazon.com/dp/B075NSQ7LY?th=1",
]

url = url_list[0]
options = webdriver.ChromeOptions()

with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
    driver.get(url)
    print("Page URL:", driver.current_url)
    # print("Page Title:", driver.title)
    title_element = driver.find_element(By.XPATH, "//*[@id='title']")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    about_item = []
    for item in soup.find_all("li", attrs={'class': 'a-spacing-mini'}):
        about_item.append(item.text.strip())

    print(about_item)
