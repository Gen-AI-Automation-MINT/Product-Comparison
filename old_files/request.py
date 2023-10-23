# importing libraries
from bs4 import BeautifulSoup
import requests


def main(URL):
    File = open("out.csv", "a")
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")

    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip().replace(',', '')

    except AttributeError:
        title_string = "NA"
    print("product Title = ", title_string)

    File.write(f"{title_string},")

    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
    except AttributeError:
        price = "NA"
    print("Products price = ", price)

    File.write(f"{price},")

    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')

    except:
        rating = "NA"
    print("Overall rating = ", rating)

    try:
        rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
    except:
        rating = "NA"
    print("Overall rating = ", rating)

    File.write(f"{rating},")

    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')

    except AttributeError:
        review_count = "NA"
    print("Total reviews = ", review_count)
    File.write(f"{review_count},")

    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip().replace(',', '')

    except AttributeError:
        available = "NA"
    print("Availability = ", available)

    # saving the availability and closing the line
    File.write(f"{available},\n")

    # closing the file
    File.close()


if __name__ == '__main__':
    main("https://www.amazon.com/dp/B075NSQ7LY?th=1")
