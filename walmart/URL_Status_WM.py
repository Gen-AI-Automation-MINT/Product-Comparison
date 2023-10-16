from dataclasses import replace
from turtle import st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv, pyautogui, time, os, codecs, threading
from selenium.webdriver.common.by import By
import urllib.parse, urllib.request
import undetected_chromedriver as uc
from datetime import datetime

tcount = 0

get_walmart_url_list = ['https://www.walmart.com/ip/999541784?selected=true']


def AttributeExtraction(get_walmart_url_list):
    pgproblem = ''
    try:
        driver.get(get_walmart_url_list[0])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(15)
    except:
        pass

    # Page Problem
    pgproblem = ''
    try:
        bb = soup.find("title")
        if bb is None:
            pgproblem = "Walmart Page Problem"
        else:
            title = bb.text.strip()
            if title == "Prints Builder | Walmart Photo":
                pgproblem = "Walmart Page Problem"
            elif title == "Walmart.com | Save Money. Live Better":
                pgproblem = "Walmart Page Problem"
            elif title == "Request Rejected":
                for val in range(0, 3):
                    time.sleep(10)
                    driver.refresh()
                    time.sleep(10)
                    title = soup.find("title").text.strip()
                    if title == "Request Rejected":
                        pgproblem = "Request Rejected"

        rp = soup.find("h1", class_="w_kKCe w_PadE mb5 w-60 tc")
        if rp != None:
            if rp.text.strip() == "Sorry...":
                driver.refresh()
    except:
        pass

    lines = get_walmart_url_list[0]
    itemid = "".join(lines.split('/', -1)[-1]).replace('?selected=true', '')
    screenshot_path = "output_files" + '\\' + itemid + '.html'
    itemid = itemid.replace('.html', '')

    try:
        pyautogui.press('alt')
    except:
        pass
    return pgproblem, itemid, screenshot_path


record = len(get_walmart_url_list)

if record:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=3200x20800")
    driver = uc.Chrome(enable_cdp_events=True, Options=chrome_options)

if record != 0:
    for url_lines in get_walmart_url_list:
        pgproblem, itemid, screenshot_path = AttributeExtraction(url_lines)
        wmid = url_lines[1]
        tooldate = datetime.now().strftime("%Y-%m-%d")
        tooltime = datetime.now().strftime("%H:%M:%S")
        url = url_lines[3]
        batch_id = url_lines[2]
        pgproblem = pgproblem
        itemid = itemid
        screenshot_path = screenshot_path
        filename = itemid + '.html'
        n = os.path.join("output_files", filename)
        if pgproblem == 'Walmart Page Problem':
            f = codecs.open(n, "w", "utf-8")
            h = driver.page_source
            f.write(h)
        else:
            while True:
                try:
                    urllib.request.urlretrieve(url_lines[3], n)
                    break
                except:
                    time.sleep(1)

        print("Downloaded " + itemid + " URL")

        itemid = "'" + itemid + "'"

        fetrecord = len(get_walmart_url_list)
        if fetrecord != 0:
            print("Updating " + itemid + " URL")

        print("Completed " + str(tcount) + " URLs out of " + str(record))
        driver.quit

else:
    print("The Given range of URLs are Processed")

print("Completed " + str(tcount) + " URLs out of " + str(record))

rows = len(get_walmart_url_list) - tcount
print("Remaining " + str(rows) + " URLs")
os.system("pause")
