import csv
from turtle import goto
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui, time, os, codecs
from selenium.webdriver.common.by import By
import re, requests
import undetected_chromedriver.v2 as uc
from random import randint
import pyodbc
from datetime import datetime
import psycopg2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import random,socket
#SQL conncetion
username = 'postgres'
password = 'Linux@18276'

System_Name = socket.gethostname()
User_Name = os.getlogin()
#SQL conncetion
def azcon():
    connection = psycopg2.connect(host = '103.19.88.66', dbname = 'Walmart MINT - AZ', user=username, password=password, port='5432')
    cursor = connection.cursor()
    return connection,cursor

rs1 = "'"+"Processed"+"'"
rs2 = "'"+""+"'"
rs3 = "'"+"Initiated"+"'"
sysname = System_Name.replace("-","_")

Batch = input('Enter the Batch ID:')

def urlquery():
    connection,cursor = azcon()
    cursor.execute('SELECT * FROM "ECHO_AE_AZ_In" WHERE "Batch_ID" = {} and "System_Name" = {} and "User_Name" = {} and ("Record_Status" is NULL or "Record_Status" = {})'.format(Batch,"'"+sysname+"'","'"+User_Name+"'",rs2))
    return connection,cursor
def query():
    connection,cursor = azcon()
    cursor.execute('WITH AZ_input AS(SELECT ROW_NUMBER() OVER (ORDER BY "Batch_ID") ID,"AZ_Record_ID","Batch_ID","AZ_URL","Input_Date","Record_Status" FROM "ECHO_AE_AZ_In" WHERE "Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" = {}  or "Record_Status" is NULL or "Record_Status" = {}))SELECT * FROM AZ_input WHERE ID Between {} and {} and ("Record_Status" = {} or "Record_Status" is NULL or "Record_Status" = {})'.format(Batch, rs1, rs3, rs2 ,Processcount, Processcount1,rs3,rs2))
    return connection,cursor

def reccount():
    connection,cursor = urlquery()
    relen = len(cursor.fetchall())
    return relen

relen = reccount()
if relen == 0:
    Processcount = int(input("Enter the number of record"))
    Processcount1 = int(input("Enter the number of record"))
    connection,cursor = query()
    for urllines in cursor.fetchall():
        connection,cursor = azcon()
        cursor.execute('UPDATE "ECHO_AE_AZ_In" SET "System_Name" = (%s),"User_Name" = (%s) WHERE "Batch_ID" = (%s) and "AZ_URL" = (%s) and "System_Name" is NULL  and "User_Name" is NULL;',(sysname,User_Name,Batch,urllines[3]))
        connection.commit()
val = "'NULL'"
#All References for Colors and Sizes
cursor.execute('SELECT "Colors" FROM "All_References" Where "Colors" != {}'.format(val))
colorscolumn = cursor.fetchall()
colorslist = []
for i in range(len(colorscolumn)):
  colorslist.append(colorscolumn[i][0].lower().strip())

cursor.execute('SELECT "Sizes" FROM "All_References" Where "Sizes" != {}'.format(val))
sizescolumn = cursor.fetchall()
sizeslist = []
for i in range(len(sizescolumn)):
  sizeslist.append(sizescolumn[i][0].lower().strip())

#Platform list
cursor.execute('SELECT "VG_Platform" FROM "VG_Platforms" Where "VG_Platform" !={}'.format(val))
platform = cursor.fetchall()
platformlist = []
for i in range(len(platform)):
  platformlist.append(platform[i][0].lower())


#install Browsec VPN
def browsecvpn():

    driver.get("https://chrome.google.com/webstore/detail/browsec-vpn-free-vpn-for/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en")
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB*11)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    pyautogui.press('left')
    time.sleep(2)
    pyautogui.press('enter')

    time.sleep(20)
    pyautogui.press('esc')
    driver.get('chrome-extension://omghfjlpggmjjaagoclmmobgdodcjboh/popup/popup.html')

    vpnstatus='No'

    while True:
        os.system('cls')
        vpnstatus = input('Type Yes if VPN is enabled:')
        if vpnstatus=='Yes':
           break

def disVPN():
    
    driver.get("https://chrome.google.com/webstore/detail/browsec-vpn-free-vpn-for/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en")
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB*11)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    pyautogui.press('enter')

#Change AMZ location
def amzlocchange():

    driver.get('https://www.amazon.com/')
    driver.implicitly_wait
    try:
        loc = str(driver.find_element(By.ID, 'glow-ingress-line2').text).strip().replace(" ", "")
    except:
        time.sleep(5)

    if loc != "LosAngeles90001":
        try:
            driver.find_element(By.ID, 'glow-ingress-line1').click()
        except:
            pass
        time.sleep(3)
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * 2)
        actions.send_keys(90001)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB*4)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(10)

# Input Paths
with open("Inputpath.txt") as z:
    lines = z.read()
    outpath = lines.split('\n', 1)[0]
    z.close

chrome_options = Options()
chrome_options.add_argument('--headerless')
chrome_options.add_argument("--window-size=3200x20800")
driver = uc.Chrome(enable_cdp_events=True, Options = chrome_options)

#browsecvpn()
amzlocchange()
#disVPN()

def book(soup):
        titleISBN13 = ''
        titleISBN10 = ''
        prodetailISBN13 = ''
        prodetailISBN10 = ''
        titleformat = ''
        try:
            # ISBN
            wtitles = soup.find("span", attrs={"id": 'productTitle'}).text
            wtitles = wtitles.split(" ")
            for i in wtitles:
                if len(i) == 13 and i.isnumeric():
                    titleISBN13 = i

        except:
            pass

        try:
            # ISBN
            wtitles = soup.find("span", attrs={"id": 'productTitle'}).text
            wtitles = wtitles.split(" ")
            for i in wtitles:
                if len(i) == 10 and i.isnumeric():
                    titleISBN10 = i

        except:
            pass

        try:
            prodet = soup.find_all('div', class_='a-expander-content a-expander-partial-collapse-content')
            for i in prodet:
                prodet_text = i.text.split(" ")
                for j in prodet_text:
                    j = j.replace(".", "")
                    if len(j) == 13 and j.isnumeric():
                        prodetailISBN13 = j
        except:
            pass

        try:
            prodet = soup.find_all('div', class_='a-expander-content a-expander-partial-collapse-content')
            for i in prodet:
                prodet_text = i.text.split(" ")
                for j in prodet_text:
                    j = j.replace(".", "")
                    if len(j) == 10 and j.isnumeric():
                        prodetailISBN10 = j
        except:
            pass

        try:
            # title format
            searched_word_format = 'Mass Market Paperback'
            titlepapercls = soup.find("span", attrs={"id": 'productSubtitle'})
            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                recursive=True)
            if len(titlepaper) != 0:
                titleformat = "Mass Market Paperback"
            else:
                searched_word_format1 = 'Hardcover'
                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format1)),
                                                    recursive=True)
                if len(titlepaper) != 0:
                    titleformat = "Hardcover"
                else:
                    searched_word_format2 = 'Dvd'
                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format2)),
                                                        recursive=True)
                    if len(titlepaper) != 0:
                        titleformat = "Dvd"
                    else:
                        searched_word_format3 = 'Audiobook'
                        searched_word_format31 = 'Audio CD'
                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                                            recursive=True)
                        titlepaper1 = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format31)),
                                                            recursive=True)
                        if (len(titlepaper) != 0) and (len(titlepaper1) != 0):
                            if iformat != '' and highformat != '' and iformat == "Audiobook" and highformat == "Audiobook":
                                titleformat = "Audiobook"
                            elif iformat != '' and highformat != '' and iformat == "Audio CD" and highformat == "Audio CD":
                                titleformat = "Audio CD"
                            elif iformat == '' and highformat != '' and iformat == "Audio CD":
                                titleformat = "Audio CD"
                            elif iformat != '' and highformat != '' and highformat == "Audiobook":
                                titleformat ="Audiobook"
                        elif len(titlepaper) != 0:
                            titleformat = "Audiobook"
                        elif len(titlepaper1) != 0:
                            titleformat = "Audio CD"
                        else:
                            searched_word_format4 = 'Board book'
                            titlepaper = titlepapercls.find_all(
                                string=re.compile('.*{0}.*'.format(searched_word_format4)), recursive=True)
                            if len(titlepaper) != 0:
                                titleformat = "Board Book"
                            else:
                                searched_word_format5 = 'Picture Book'
                                titlepaper = titlepapercls.find_all(
                                    string=re.compile('.*{0}.*'.format(searched_word_format5)), recursive=True)
                                if len(titlepaper) != 0:
                                    titleformat = "Picture Book"
                                else:
                                    searched_word_format6 = 'Trade Paperback'
                                    titlepaper = titlepapercls.find_all(
                                        string=re.compile('.*{0}.*'.format(searched_word_format6)), recursive=True)
                                    if len(titlepaper) != 0:
                                        titleformat = "Trade Paperback"
                                    else:
                                        searched_word_format7 = 'Paperback'
                                        titlepaper = titlepapercls.find_all(
                                            string=re.compile('.*{0}.*'.format(searched_word_format7)), recursive=True)
                                        if len(titlepaper) != 0:
                                            titleformat = "Paperback"
                                        else:
                                            searched_word_format8 = 'Kindle'
                                            titlepaper = titlepapercls.find_all(
                                                string=re.compile('.*{0}.*'.format(searched_word_format8)),
                                                recursive=True)
                                            if len(titlepaper) != 0:
                                                titleformat = "Kindle"

                                            else:
                                                searched_word_format9 = 'Ebook'
                                                titlepaper = titlepapercls.find_all(
                                                    string=re.compile('.*{0}.*'.format(searched_word_format9)),
                                                    recursive=True)
                                                if len(titlepaper) != 0:
                                                    titleformat = "Ebook"

                                                else:
                                                    searched_word_format10 = 'Audio CD'
                                                    titlepaper = titlepapercls.find_all(
                                                        string=re.compile('.*{0}.*'.format(searched_word_format10)),
                                                        recursive=True)
                                                    if len(titlepaper) != 0:
                                                        titleformat = "Audio CD"

                                                    else:
                                                        searched_word_format11 = 'Soft Cover (Paperback)'
                                                        titlepaper = titlepapercls.find_all(
                                                            string=re.compile('.*{0}.*'.format(searched_word_format11)),
                                                            recursive=True)
                                                        if len(titlepaper) != 0:
                                                            titleformat = "Soft Cover (Paperback)"
                                                        else:
                                                            searched_word_format12 = 'DVD'
                                                            titlepaper = titlepapercls.find_all(string=re.compile(
                                                                '.*{0}.*'.format(searched_word_format12)),
                                                                recursive=True)
                                                            if len(titlepaper) != 0:
                                                                titleformat = "DVD"
                                                            else:
                                                                searched_word_format13 = 'Book'
                                                                titlepaper = titlepapercls.find_all(string=re.compile(
                                                                    '.*{0}.*'.format(searched_word_format13)),
                                                                    recursive=True)
                                                                if len(titlepaper) != 0:
                                                                    titleformat = "Book"
                                                                else:
                                                                    searched_word_format14 = 'Flexibound'
                                                                    titlepaper = titlepapercls.find_all(
                                                                        string=re.compile(
                                                                            '.*{0}.*'.format(searched_word_format14)),
                                                                        recursive=True)
                                                                    if len(titlepaper) != 0:
                                                                        titleformat = "Flexibound"
                                                                    else:
                                                                        searched_word_format15 = 'Calendar'
                                                                        titlepaper = titlepapercls.find_all(
                                                                            string=re.compile(
                                                                                '.*{0}.*'.format(
                                                                                    searched_word_format15)),
                                                                            recursive=True)
                                                                        if len(titlepaper) != 0:
                                                                            titleformat = "Calendar"
                                                                        else:
                                                                            searched_word_format16 = 'Cards'
                                                                            titlepaper = titlepapercls.find_all(
                                                                                string=re.compile(
                                                                                    '.*{0}.*'.format(
                                                                                        searched_word_format16)),
                                                                                recursive=True)
                                                                            if len(titlepaper) != 0:
                                                                                titleformat = "Cards"
                                                                            else:
                                                                                searched_word_format17 = 'Library Binding'
                                                                                titlepaper = titlepapercls.find_all(
                                                                                    string=re.compile(
                                                                                        '.*{0}.*'.format(
                                                                                            searched_word_format17)),
                                                                                    recursive=True)
                                                                                if len(titlepaper) != 0:
                                                                                    titleformat = "Library Binding"
                                                                                else:
                                                                                    searched_word_format18 = 'Map'
                                                                                    titlepaper = titlepapercls.find_all(
                                                                                        string=re.compile(
                                                                                            '.*{0}.*'.format(
                                                                                                searched_word_format18)),
                                                                                        recursive=True)
                                                                                    if len(titlepaper) != 0:
                                                                                        titleformat = "Map"
                                                                                    else:
                                                                                        searched_word_format19 = 'Spiral-bound'
                                                                                        titlepaper = titlepapercls.find_all(
                                                                                            string=re.compile(
                                                                                                '.*{0}.*'.format(
                                                                                                    searched_word_format19)),
                                                                                            recursive=True)
                                                                                        if len(titlepaper) != 0:
                                                                                            titleformat = "Spiral-bound"
                                                                                        else:
                                                                                            searched_word_format20 = 'Plastic Comb'
                                                                                            titlepaper = titlepapercls.find_all(
                                                                                                string=re.compile(
                                                                                                    '.*{0}.*'.format(
                                                                                                        searched_word_format20)),
                                                                                                recursive=True)
                                                                                            if len(titlepaper) != 0:
                                                                                                titleformat = "Plastic Comb"

        except:
            pass

        return titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, titleformat

def extraction(soup):
        titleISBN13 = ''
        titleISBN10 = ''
        prodetailISBN13 = ''
        prodetailISBN10 = ''
        titleformat = ''
        try:
            # ISBN
            wtitles = soup.find("span", attrs={"id": 'productTitle'}).text
            wtitles = wtitles.split(" ")
            for i in wtitles:
                if len(i) == 13 and i.isnumeric():
                    titleISBN13 = i

        except:
            pass

        try:
            # ISBN
            wtitles = soup.find("span", attrs={"id": 'productTitle'}).text
            wtitles = wtitles.split(" ")
            for i in wtitles:
                if len(i) == 10 and i.isnumeric():
                    titleISBN10 = i

        except:
            pass

        try:
            prodet = soup.find_all('div', class_='a-expander-content a-expander-partial-collapse-content')
            for i in prodet:
                prodet_text = i.text.split(" ")
                for j in prodet_text:
                    j = j.replace(".", "")
                    if len(j) == 13 and j.isnumeric():
                        prodetailISBN13 = j
        except:
            pass

        try:
            prodet = soup.find_all('div', class_='a-expander-content a-expander-partial-collapse-content')
            for i in prodet:
                prodet_text = i.text.split(" ")
                for j in prodet_text:
                    j = j.replace(".", "")
                    if len(j) == 10 and j.isnumeric():
                        prodetailISBN10 = j
        except:
            pass

        try:
            # title format
            searched_word_format = 'Mass Market Paperback'
            titlepapercls = soup.find("span", attrs={"id": 'productSubtitle'})
            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                recursive=True)
            if len(titlepaper) != 0:
                titleformat = "Mass Market Paperback"
            else:
                searched_word_format1 = 'Hardcover'
                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format1)),
                                                    recursive=True)
                if len(titlepaper) != 0:
                    titleformat = "Hardcover"
                else:
                    searched_word_format2 = 'Dvd'
                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format2)),
                                                        recursive=True)
                    if len(titlepaper) != 0:
                        titleformat = "Dvd"
                    else:
                        searched_word_format3 = 'Audiobook'
                        searched_word_format31 = 'Audio CD'
                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                                            recursive=True)
                        titlepaper1 = titlepapercls.find_all(
                            string=re.compile('.*{0}.*'.format(searched_word_format31)),
                            recursive=True)
                        if (len(titlepaper) != 0) and (len(titlepaper1) != 0):
                            if iformat != '' and highformat != '' and iformat == "Audiobook" and highformat == "Audiobook":
                                titleformat = "Audiobook"
                            elif iformat != '' and highformat != '' and iformat == "Audio CD" and highformat == "Audio CD":
                                titleformat = "Audio CD"
                            elif iformat == '' and highformat != '' and iformat == "Audio CD":
                                titleformat = "Audio CD"
                            elif iformat != '' and highformat != '' and highformat == "Audiobook":
                                titleformat = "Audiobook"
                        elif len(titlepaper) != 0:
                            titleformat = "Audiobook"
                        elif len(titlepaper1) != 0:
                            titleformat = "Audio CD"
                        else:
                            searched_word_format4 = 'Board book'
                            titlepaper = titlepapercls.find_all(
                                string=re.compile('.*{0}.*'.format(searched_word_format4)), recursive=True)
                            if len(titlepaper) != 0:
                                titleformat = "Board Book"
                            else:
                                searched_word_format5 = 'Picture Book'
                                titlepaper = titlepapercls.find_all(
                                    string=re.compile('.*{0}.*'.format(searched_word_format5)), recursive=True)
                                if len(titlepaper) != 0:
                                    titleformat = "Picture Book"
                                else:
                                    searched_word_format6 = 'Trade Paperback'
                                    titlepaper = titlepapercls.find_all(
                                        string=re.compile('.*{0}.*'.format(searched_word_format6)), recursive=True)
                                    if len(titlepaper) != 0:
                                        titleformat = "Trade Paperback"
                                    else:
                                        searched_word_format7 = 'Paperback'
                                        titlepaper = titlepapercls.find_all(
                                            string=re.compile('.*{0}.*'.format(searched_word_format7)), recursive=True)
                                        if len(titlepaper) != 0:
                                            titleformat = "Paperback"
                                        else:
                                            searched_word_format8 = 'Kindle'
                                            titlepaper = titlepapercls.find_all(
                                                string=re.compile('.*{0}.*'.format(searched_word_format8)),
                                                recursive=True)
                                            if len(titlepaper) != 0:
                                                titleformat = "Kindle"

                                            else:
                                                searched_word_format9 = 'Ebook'
                                                titlepaper = titlepapercls.find_all(
                                                    string=re.compile('.*{0}.*'.format(searched_word_format9)),
                                                    recursive=True)
                                                if len(titlepaper) != 0:
                                                    titleformat = "Ebook"

                                                else:
                                                    searched_word_format10 = 'Audio CD'
                                                    titlepaper = titlepapercls.find_all(
                                                        string=re.compile('.*{0}.*'.format(searched_word_format10)),
                                                        recursive=True)
                                                    if len(titlepaper) != 0:
                                                        titleformat = "Audio CD"

                                                    else:
                                                        searched_word_format11 = 'Soft Cover (Paperback)'
                                                        titlepaper = titlepapercls.find_all(
                                                            string=re.compile('.*{0}.*'.format(searched_word_format11)),
                                                            recursive=True)
                                                        if len(titlepaper) != 0:
                                                            titleformat = "Soft Cover (Paperback)"
                                                        else:
                                                            searched_word_format12 = 'DVD'
                                                            titlepaper = titlepapercls.find_all(string=re.compile(
                                                                '.*{0}.*'.format(searched_word_format12)),
                                                                recursive=True)
                                                            if len(titlepaper) != 0:
                                                                titleformat = "DVD"
                                                            else:
                                                                searched_word_format13 = 'Book'
                                                                titlepaper = titlepapercls.find_all(string=re.compile(
                                                                    '.*{0}.*'.format(searched_word_format13)),
                                                                    recursive=True)
                                                                if len(titlepaper) != 0:
                                                                    titleformat = "Book"
                                                                else:
                                                                    searched_word_format14 = 'Flexibound'
                                                                    titlepaper = titlepapercls.find_all(
                                                                        string=re.compile(
                                                                            '.*{0}.*'.format(searched_word_format14)),
                                                                        recursive=True)
                                                                    if len(titlepaper) != 0:
                                                                        titleformat = "Flexibound"
                                                                    else:
                                                                        searched_word_format15 = 'Calendar'
                                                                        titlepaper = titlepapercls.find_all(
                                                                            string=re.compile(
                                                                                '.*{0}.*'.format(
                                                                                    searched_word_format15)),
                                                                            recursive=True)
                                                                        if len(titlepaper) != 0:
                                                                            titleformat = "Calendar"
                                                                        else:
                                                                            searched_word_format16 = 'Cards'
                                                                            titlepaper = titlepapercls.find_all(
                                                                                string=re.compile(
                                                                                    '.*{0}.*'.format(
                                                                                        searched_word_format16)),
                                                                                recursive=True)
                                                                            if len(titlepaper) != 0:
                                                                                titleformat = "Cards"
                                                                            else:
                                                                                searched_word_format17 = 'Library Binding'
                                                                                titlepaper = titlepapercls.find_all(
                                                                                    string=re.compile(
                                                                                        '.*{0}.*'.format(
                                                                                            searched_word_format17)),
                                                                                    recursive=True)
                                                                                if len(titlepaper) != 0:
                                                                                    titleformat = "Library Binding"
                                                                                else:
                                                                                    searched_word_format18 = 'Map'
                                                                                    titlepaper = titlepapercls.find_all(
                                                                                        string=re.compile(
                                                                                            '.*{0}.*'.format(
                                                                                                searched_word_format18)),
                                                                                        recursive=True)
                                                                                    if len(titlepaper) != 0:
                                                                                        titleformat = "Map"
                                                                                    else:
                                                                                        searched_word_format19 = 'Spiral-bound'
                                                                                        titlepaper = titlepapercls.find_all(
                                                                                            string=re.compile(
                                                                                                '.*{0}.*'.format(
                                                                                                    searched_word_format19)),
                                                                                            recursive=True)
                                                                                        if len(titlepaper) != 0:
                                                                                            titleformat = "Spiral-bound"
                                                                                        else:
                                                                                            searched_word_format20 = 'Plastic Comb'
                                                                                            titlepaper = titlepapercls.find_all(
                                                                                                string=re.compile(
                                                                                                    '.*{0}.*'.format(
                                                                                                        searched_word_format20)),
                                                                                                recursive=True)
                                                                                            if len(titlepaper) != 0:
                                                                                                titleformat = "Plastic Comb"

        except:
            pass

        return titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, titleformat


def movies(soup):
        titleformat = ""
        try:
            # title format
            titlepapercls = soup.find("title")
            searched_word_format = 'Dvd'
            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),recursive=True)
            if len(titlepaper) != 0:
                    titleformat = "DVD"
            else:
                searched_word_format1 = 'DVD'
                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format1)),recursive=True)
                if len(titlepaper) != 0:
                    titleformat = "DVD"    
                else:
                    searched_word_format9 = 'CD'
                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format9)),recursive=True)
                    if len(titlepaper) != 0:
                        titleformat = "CD"
                    else:
                        searched_word_format2 = 'Blu-Ray'
                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format2)),recursive=True)
                        if len(titlepaper) != 0:
                            titleformat = "Blu-Ray"
                        else:
                            searched_word_format3 = 'Blu-ray'
                            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format3)),recursive=True)
                            if len(titlepaper) != 0:
                                titleformat = "Blu-ray"
                            else:
                                searched_word_format5 = 'Multiple Formats'
                                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format5)),recursive=True)
                                if len(titlepaper) != 0:
                                    titleformat = "Multi-Format"
                                else:
                                    searched_word_format6 = 'VHS Tape'
                                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format6)),recursive=True)
                                    if len(titlepaper) != 0:
                                        titleformat = "VHS Tape"
                                    else:
                                        searched_word_format7 = '4K Ultra HD'
                                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format7)),recursive=True)
                                        if len(titlepaper) != 0:
                                            titleformat = "4K Ultra HD"
                                        else:
                                            searched_word_format8 = '4K Ultra Hd'
                                            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format8)),recursive=True)
                                            if len(titlepaper) != 0:
                                                titleformat = "4K Ultra HD"
        except:
            pass

        return titleformat

def autotires(soup,size):
        titletiresize = ""
        aboutloadrange = ""
        swatchtiresize = ""
        swatchloadindexrating = ""
        swatchspeedrating = ""
        swatchhightiresize = ""
        titleloadrange = ""
        #Title Tire Size
        try:
            title_ex = soup.find("title").text.split(" ")
            count = 0
            for i in title_ex:
                count += 1
                if '/' in i or 'x' in i:
                    j = re.sub('\D', '', i)
                    if j == size :
                        titletiresize = j
                    else:
                        if len(j) == len(size):
                            titletiresize = j
                        else:
                            titletiresize = j
                
                if 'PLY' in i or '-ply' in i:
                    titleloadrange = i
                else:
                    if titletiresize != '':
                        j = re.sub('\D', '', title_ex[count])
                        titleloadrange = j
                        break           
        except:
            pass

        try:
            tagcount = 0
            abb = soup.find("div", attrs={"id": "feature-bullets"})
            if abb != None:
                about = abb.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
                if about != None:
                    about = about.find_all("span", class_="a-list-item")
                    if about != None:
                        for j in about:
                            prodet_text = j.text
                            if "Load Range" in prodet_text.strip():
                                if aboutloadrange == '':
                                    val = prodet_text.strip()
                                    val = val.replace("Load Range","").split(" ")
                                    for k in val:
                                        if '-Ply' in k: 
                                            aboutloadrange = k
                                            
        except:
            pass

        try:
            bd = soup.find("table", class_="a-normal a-spacing-micro")
            if bd != None:
                    title = bd.findAll('td', class_="a-span3")
                    if title != None:
                        value = bd.findAll('td', class_='a-span9')
                        if value != None:
                            for headeritem in bd.findAll('td', class_="a-span3"):
                                
                                infohead = title[tagcount]
                                infodata = value[tagcount]
                                tagcount = tagcount + 1
                                
                                if infohead.text.strip() == "Size":
                                    j = re.sub('\D', '', infodata.text.strip())
                                    if j == size:
                                        swatchtiresize = j
                                if infohead.text.strip() == "Load Index Rating":
                                    swatchloadindexrating = infodata.text.strip()
                                if infohead.text.strip() == "Speed Rating":
                                    swatchspeedrating = infodata.text.strip()
                                    
        except:

            pass

        try:
            title = soup.find("div", attrs={"id": "variation_size_name"})
            if title != None:
                title1 = title.find("div", class_="a-row")
                if title1 != None:
                    title1 = title1.find("label", class_="a-form-label")
                    if title1 != None:
                        c1 = title1.text.strip()
                        if c1 != None:
                            if c1 == 'Size:':
                                hsize = title1.find("span", class_="selection")
                                if hsize != None:
                                    j = re.sub('\D', '', hsize.text.strip())
                                    if j == size:
                                        swatchhightiresize = j
                                else:
                                    title = title.find("select", attrs={"id": "native_dropdown_selected_size_name"})
                                    if title != None:
                                        title = title.find("option", class_="dropdownSelect")
                                        if title != None:
                                            j = re.sub('\D', '', title.text.strip())
                                            if j == size:
                                                swatchhightiresize = j
                                           
        except:
            pass

        return titletiresize,aboutloadrange,swatchtiresize,swatchloadindexrating,swatchspeedrating,swatchhightiresize,titleloadrange

def videogames(soup):
    platform = ""
    swatchplatform = ""
    titleplatform = ""
    prodetplatformlist = []
    try:
        platfor = soup.find("div", attrs={"id":"platformInformation_feature_div"}).text.strip()
        if 'Platform : ' in platfor: 
            platform = platfor.replace("Platform : ","").replace("|","").strip()
    except:
        pass

    try:
            title = soup.find("div", attrs={"id": "variation_platform_for_display"})
            if title != None:
                title1 = title.find("div", class_="a-row")
                if 'Platform For Display:' in title1.text.strip():
                    swatchplatform = title1.text.replace("Platform For Display:","").strip()
                elif 'Platform' in title1.text.strip():
                    swatchplatform = title1.text.replace("Platform:","").strip()
    except:
        pass

    try:
        titleplatforms = soup.find("title")
        for titleform in titleplatforms:
            titleform = titleform.text.lower().replace(".","")
            for i in platformlist:
                if i in titleform:
                    titleplatform = i   
                    break 
    except:
        pass

    try:
        prodetpaperclss = soup.find_all('div', attrs={"id":"productDescription_feature_div"})
        for prodetpapercls in prodetpaperclss:
            prodetpapercls = prodetpapercls.text.lower()
            for i in platformlist:
                if i in prodetpapercls:
                    prodetplatformlist.append(i)
    except:
        pass

    return platform,swatchplatform,titleplatform,prodetplatformlist

#Clothing
def clothing(soup):
        titlecolorlist = []
        titleclothingsizelist = []
        prodetailcolor = ""
        prodetailclothingsize = ""

      #titlecolour
        try:
            if titlecolorlist == []:
                titep = soup.find("span", attrs={"id":"productTitle"})
                words = titep.text.replace("."," ").replace(","," ").replace("(","").replace(")","").split()
                for word in words:
                    titlecol = word.lower()
                    for i in colorslist:
                        if i == titlecol:
                            titlecolorlist.append(i)
            

        except:
            pass
        #titlesize
        try:
            titlepapercls = soup.find("span", attrs={"id": 'productTitle'})
            words = titlepapercls.text.replace("."," ").replace(","," ").replace("(","").replace(")","").split()
            for word in words:
                titlewords = word.lower()
                for j in sizeslist:
                    if j == titlewords:
                        titleclothingsizelist.append(j)
        except:
            pass
        #productdetail color - About this item
        try:
            prodet = soup.find_all('div', attrs={"id":"productDescription_feature_div"}) 
            for k in prodet:
                kk = k.find_all("p")
                for pp in kk:
                    p = pp.text.lower().replace("color: ","color:").replace("size: ","size:").replace("colorcolor","color").split(" ")
                    for cs in p:
                        if 'color:' in cs:
                            prodetailcoo = cs.replace("color:","").strip()
                            for prodetailcoll in colorslist:
                                if prodetailcoo == prodetailcoll:
                                    prodetailcolor = prodetailcoo
                        if 'size:' in cs:
                            prodetailcloths = cs.replace("size:","").strip()
                            for prodetailcols in sizeslist:
                                if prodetailcloths == prodetailcols:
                                    prodetailcolor = prodetailcols
            
            if prodetailcolor == '':
                count = 0
                for i in prodet:
                    i = i.text.lower().replace("color: ","color:").replace("color(","color:").replace("color:","color:").split(" ")
                    for j in i:
                        count += 1
                        if "color:" in j:
                                prodetailco = j.replace("color:","").replace(",","").strip()
                        elif 'color' in j:
                                prodetailco = i[count].replace(",","")
                        for prodetailcol in colorslist:
                            if prodetailco == prodetailcol:
                                prodetailcolor = prodetailcol
            
            if prodetailcolor == '':
                for word2 in prodet:
                    prodetailwords = word2.text.lower().replace("."," ").replace(","," ").split(" ")
                    for prodetailcol in colorslist:
                        for j in prodetailwords:
                            if j == prodetailcol:
                                prodetailcolor = j

        except:
            pass
#productdetail size
        try:
            prodet = soup.find_all('div', class_='a-unordered-list a-vertical a-spacing-mini')
            if prodetailclothingsize == '':
                    count = 0
                    for i in prodet:
                        i = i.text.lower().replace("size: ","size:").replace("sizes(","size:").replace("shoes size","shoessize").replace("size details:","size:").replace("size;","size:").replace("(size ","size:").split(" ")
                        for j in i:
                            count += 1
                            if "size:" in j:
                                    prodetailclothingsize = j.replace("size:","").replace(",","").strip()
                            elif "shoessize" in j:

                                prodetailclothingsize = i[count].replace(",","")
            if prodetailclothingsize == '':
                
                for word2 in prodet:
                    prodetailwords = word2.text.lower().replace("."," ").replace(","," ").split(" ")
                    for size in sizeslist:
                        for j in prodetailwords:
                            if j == size:
                                prodetailclothingsize = j
        except:
            pass
            
        return titlecolorlist, titleclothingsizelist, prodetailclothingsize, prodetailcolor



def bookmatchtype(isbn,isbn1,titleISBN13,titleISBN10,prodetailISBN13,prodetailISBN10,titleformat,highformat,iformat,pagecount):
        highformat = highformat.strip()
        matchtype = ""
        matchtypecomments = ""
        if isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat == '' and highformat == '' and iformat == '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat != '' and highformat == '' and iformat == '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat == '' and highformat != '' and iformat == '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat == '' and highformat == '' and iformat != '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat != '' and highformat != '' and iformat == '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat == '' and highformat != '' and iformat != '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif isbn == '' and isbn1 == '' and titleISBN13 == '' and titleISBN10 == '' and prodetailISBN13 == '' and prodetailISBN10 == '' and titleformat != '' and highformat == '' and iformat != '' and pagecount == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing"
        elif iformat != '' and titleformat != '' and highformat != '' and (iformat != titleformat) and (titleformat != highformat) and (highformat != iformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"

        return matchtype,matchtypecomments


def moviesandmusicmatchtype(director,actors,iformat,titleformat,titleformats,highformat,mediaformat,unhighlitedformat):
    matchtype = ""
    matchtypecomments = ""

    #1
    if director == '' and actors == '' and iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing"
    
    #2
    elif iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '' and unhighlitedformat == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Format"
    
    elif iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '' and unhighlitedformat != '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Swatch Format Unselected"
    
    elif highformat == '' and unhighlitedformat != '':
        
      if (director == '' and actors == '') and (iformat != '' and iformat != '4K') and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and (titleformat != '' and titleformat != '4K') and titleformats == '' and highformat == '' and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and (titleformats != '' and titleformats != '4K') and highformat == '' and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats == '' and (highformat != '' and highformat != '4K') and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and (mediaformat != '' and mediaformat != '4K'):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"

      #4
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K') and (iformat == titleformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K') and (iformat == titleformats):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and highformat != '4K') and (iformat == highformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and mediaformat != '4K') and (iformat == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K') and (titleformat == titleformats):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and highformat != '4K') and (titleformat == highformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and mediaformat != '4K') and (titleformat == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformats != '4K' and highformat != '4K') and (titleformats == highformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformats != '4K' and mediaformat != '4K') and (titleformats == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (highformat != '4K' and mediaformat != '4K') and (highformat == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      
      #5
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K') and (iformat == titleformat) and (iformat == titleformats):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K') and (iformat == titleformats) and (iformat == highformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat == highformat) and (iformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"   
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K') and (titleformat == titleformats) and (titleformat == highformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformat == highformat) and (titleformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"     
      elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformats == highformat) and (titleformats == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K') and (iformat == titleformat) and (iformat == highformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"     
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and mediaformat != '4K') and (iformat == titleformat) and (iformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (titleformat == titleformats) and (titleformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"     
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (iformat == titleformats ) and (iformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      
      #6
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K') and ((iformat == titleformat) or (iformat == titleformats) or (iformat == highformat)):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformats) or (iformat == highformat) or (iformat == mediaformat)):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected" 
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformat) or (iformat == highformat) or (iformat == mediaformat)):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((titleformat == titleformats) or (titleformat == highformat) or (titleformat == mediaformat)):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      
      #7 
      elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformat) or (iformat == mediaformat) or (iformat == titleformats) or (iformat == highformat)):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"

      elif (director != '' or actors != '') and (iformat != '' and iformat != '4K') and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and (titleformat != '' and titleformat != '4K') and titleformats == '' and highformat == '' and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and (titleformats != '' and titleformats != '4K') and highformat == '' and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats == '' and (highformat != '' and highformat != '4K') and mediaformat == '':
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and (mediaformat != '' and mediaformat != '4K'):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"

      #4
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K') and (iformat == titleformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K') and (iformat == titleformats):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and highformat != '4K') and (iformat == highformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and mediaformat != '4K') and (iformat == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K') and (titleformat == titleformats):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and highformat != '4K') and (titleformat == highformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and mediaformat != '4K') and (titleformat == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformats != '4K' and highformat != '4K') and (titleformats == highformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformats != '4K' and mediaformat != '4K') and (titleformats == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (highformat != '4K' and mediaformat != '4K') and (highformat == mediaformat):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      
      #5
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K') and (iformat == titleformat) and (iformat == titleformats):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K') and (iformat == titleformats) and (iformat == highformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat == highformat) and (iformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"   
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K') and (titleformat == titleformats) and (titleformat == highformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformat == highformat) and (titleformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"     
      elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformats == highformat) and (titleformats == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K') and (iformat == titleformat) and (iformat == highformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"     
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and mediaformat != '4K') and (iformat == titleformat) and (iformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (titleformat == titleformats) and (titleformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"     
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (iformat == titleformats ) and (iformat == mediaformat):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      
      #6
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K') and ((iformat == titleformat) or (iformat == titleformats) or (iformat == highformat)):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformats) or (iformat == highformat) or (iformat == mediaformat)):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected" 
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformat) or (iformat == highformat) or (iformat == mediaformat)):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      elif (director != '' or actors != '') and iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((titleformat == titleformats) or (titleformat == highformat) or (titleformat == mediaformat)):
              matchtype = "Not Sure"
              matchtypecomments = "Info Missing - Swatch Format Unselected"
      
      #7 
      elif (director != '' or actors != '') and iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformat) or (iformat == mediaformat) or (iformat == titleformats) or (iformat == highformat)):
          matchtype = "Not Sure"
          matchtypecomments = "Info Missing - Swatch Format Unselected"

    #3
    elif (director == '' and actors == '') and (iformat != '' and iformat != '4K') and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and (titleformat != '' and titleformat != '4K') and titleformats == '' and highformat == '' and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and (titleformats != '' and titleformats != '4K') and highformat == '' and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats == '' and (highformat != '' and highformat != '4K') and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and (mediaformat != '' and mediaformat != '4K'):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"

    #4
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K') and (iformat == titleformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K') and (iformat == titleformats):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and highformat != '4K') and (iformat == highformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and mediaformat != '4K') and (iformat == mediaformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K') and (titleformat == titleformats):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and highformat != '4K') and (titleformat == highformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and mediaformat != '4K') and (titleformat == mediaformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformats != '4K' and highformat != '4K') and (titleformats == highformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformats != '4K' and mediaformat != '4K') and (titleformats == mediaformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (highformat != '4K' and mediaformat != '4K') and (highformat == mediaformat):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    
    #5
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K') and (iformat == titleformat) and (iformat == titleformats):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K') and (iformat == titleformats) and (iformat == highformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat == highformat) and (iformat == mediaformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"   
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K') and (titleformat == titleformats) and (titleformat == highformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformat == highformat) and (titleformat == mediaformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"     
    elif (director == '' and actors == '') and iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformats == highformat) and (titleformats == mediaformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K') and (iformat == titleformat) and (iformat == highformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"     
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and mediaformat != '4K') and (iformat == titleformat) and (iformat == mediaformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (titleformat == titleformats) and (titleformat == mediaformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"     
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (iformat == titleformats ) and (iformat == mediaformat):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    
    #6
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K') and ((iformat == titleformat) or (iformat == titleformats) or (iformat == highformat)):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    elif (director == '' and actors == '') and iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformats) or (iformat == highformat) or (iformat == mediaformat)):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer" 
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformat) or (iformat == highformat) or (iformat == mediaformat)):
            matchtype = "Not Sure - Low confidence - Performer/Artist/Actor/Director/Singer"
            matchtypecomments = "Info Missing"
    elif (director == '' and actors == '') and iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((titleformat == titleformats) or (titleformat == highformat) or (titleformat == mediaformat)):
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"
    
    #7 
    elif (director == '' and actors == '') and iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and ((iformat == titleformat) or (iformat == mediaformat) or (iformat == titleformats) or (iformat == highformat)):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Performer/Artist/Actor/Director/Singer"

    #Unhighlited
    
    
    #8
    elif (director != '' or actors != '') and iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Format"

    #9
    elif (iformat != '' and iformat == '4K') and titleformat == '' and titleformats == '' and highformat == '' and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4k Format"
    elif iformat == '' and (titleformat != '' and titleformat == '4K') and titleformats == '' and highformat == '' and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4k Format"
    elif iformat == '' and titleformat == '' and (titleformats != '' and titleformats == '4K') and highformat == '' and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4k Format"
    elif iformat == '' and titleformat == '' and titleformats == '' and (highformat != '' and highformat == '4K') and mediaformat == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4k Format"
    elif iformat == '' and titleformat == '' and titleformats == '' and highformat == '' and (mediaformat != '' and mediaformat == '4K'):
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4k Format"

    #10
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat == '' and iformat == '4K' and titleformat == '4K':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4K Format"
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat == '' and iformat == '4K' and titleformats == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat == '' and iformat == '4K' and highformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat != '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat != '' and iformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and titleformat == '4K' and titleformats == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and titleformat == '4K' and highformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and titleformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and titleformats == '4K' and highformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and titleformats == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    
    #11
    elif  iformat != '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and iformat == '4K' and titleformat == '4K' and titleformats == '4K':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4K Format"
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and iformat == '4K' and titleformats == '4K' and highformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and iformat == '4K' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"   
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and titleformat == '4K' and titleformats == '4K' and highformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and titleformat == '4K' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"     
    elif  iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and titleformats == '4K' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and iformat == '4K' and titleformat == '4K' and highformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"     
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and iformat == '4K' and titleformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat != '' and titleformat == '4K' and titleformats == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"     
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and iformat == '4K' and titleformats == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    
    #12
    elif iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and iformat == '4K' and titleformat == '4K' and titleformats == '4K' and highformat == '4K':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4K Format"
    elif iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and iformat == '4K' and titleformats == '4K' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format" 
    elif iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and iformat == '4K' and titleformat == '4K' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    elif iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and titleformat == '4K' and titleformats == '4K' and highformat == '4K' and mediaformat == '4K':
            matchtype = "Not Sure - Low confidence"
            matchtypecomments = "4K Format"
    
    #13
    elif iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and iformat == '4K' and titleformat == '4K' and titleformats == '4K' and highformat == '4K' and mediaformat == '4K':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "4K Format"
        
    #14 MultiInfo
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K') and (iformat != titleformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K') and (iformat != titleformats):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and highformat != '4K') and (iformat != highformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat == '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and mediaformat != '4K') and (iformat != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K') and (titleformat != titleformats):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and highformat != '4K') and (titleformat != highformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and mediaformat != '4K') and (titleformat != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformats != '4K' and highformat != '4K') and (titleformats != highformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformats != '4K' and mediaformat != '4K') and (titleformats != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (highformat != '4K' and mediaformat != '4K') and (highformat != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"

    #15
    elif  iformat != '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K') and (iformat != titleformat) and (iformat != titleformats) and (titleformat != titleformats):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K') and (iformat != titleformats) and (iformat != highformat) and (titleformats != highformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat == '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat != highformat) and (iformat != mediaformat) and (highformat != mediaformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"   
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K') and (titleformat != titleformats) and (titleformat != highformat) and (titleformats != highformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformat != highformat) and (titleformat != mediaformat) and (highformat != mediaformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"     
    elif  iformat == '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformats != highformat) and (titleformats != mediaformat) and (highformat != mediaformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K') and (iformat != titleformat) and (iformat != highformat) and (titleformat != highformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"     
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and mediaformat != '4K') and (iformat != titleformat) and (iformat != mediaformat) and (titleformat != mediaformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat == '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (titleformat != titleformats) and (titleformat != mediaformat) and (titleformats != mediaformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"     
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat == '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and mediaformat != '4K') and (iformat != titleformats) and (iformat != mediaformat) and (titleformats != mediaformat):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
    
    #16
    elif iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat == '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K') and (iformat != titleformat != titleformats) and (iformat != titleformat != highformat) and (iformat != titleformats != highformat) and (titleformat != titleformats != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat != '' and titleformat == '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat != titleformats) and (iformat != titleformats != highformat) and (iformat != titleformats != mediaformat) and (iformat != highformat != mediaformat) and (titleformats != highformat != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info" 
    elif  iformat != '' and titleformat != '' and titleformats == '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat != titleformat != highformat) and (iformat != titleformat != mediaformat) and (titleformat != highformat != mediaformat) and (iformat != highformat != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  iformat == '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (titleformat != titleformats != highformat) and (titleformat != titleformats != mediaformat) and (titleformats != highformat != mediaformat) and(titleformat != highformat != mediaformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #17
    elif iformat != '' and titleformat != '' and titleformats != '' and highformat != '' and mediaformat != '' and (iformat != '4K' and titleformat != '4K' and titleformats != '4K' and highformat != '4K' and mediaformat != '4K') and (iformat == titleformat) and (iformat == mediaformat) and (iformat == titleformats) and (iformat == highformat):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    return matchtype,matchtypecomments


def autotiresmatchtype(model,partno,size,titletiresize,swatchtiresize,swatchhightiresize,loadrange,titleloadrange,aboutloadrange,speedrating,swatchspeedrating):
    matchtype = ""
    matchtypecomments = ""
    
    speedrating = speedrating.replace('\u200e', '')
    
    #1
    if model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Model/Size/Load Range/Speed Rating"
    

    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Size/Load Range/Speed Rating"
    
    #2
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and (loadrange != '' or titleloadrange != '' or aboutloadrange != '') and (speedrating != '' or swatchspeedrating != ''):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Size"
    
    #Load Range/Speed Rating
    #6
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    
    #7
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    
    #8
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    
    #9
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"

    #6
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    
    #7
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    
    #8
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or  (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    
    #9
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range/Speed Rating"
    

    #Speed Rating
    #10
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #11
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #12
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #13
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #14
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #15
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"

    #16
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #17
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    
    #18
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #19
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #20
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #21
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Speed Rating"

    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"

    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #11
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #12
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #13
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #14
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #15
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"

    #16
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize))and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #17
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (loadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (titleloadrange == aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    
    #18
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #19
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == titletiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchtiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size == swatchhightiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchtiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #20
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"
    
    #21
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and ((loadrange == titleloadrange) or (loadrange == aboutloadrange) or (titleloadrange == aboutloadrange)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Speed Rating"


        
    #load range
    
    #22
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #23
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #24
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #25
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size == titletiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #26
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #27
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #28
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    
    #29
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #30
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size == titletiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size == swatchtiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size == swatchhightiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize == swatchtiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize == swatchhightiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (swatchtiresize == swatchhightiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #31
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == swatchtiresize) or (size == swatchhightiresize) or(swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    elif (model != '' or partno != '') and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    
    #32
    elif (model != '' or partno != '') and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure - Low Confidence"
        matchtypecomments = "Info Missing - Load Range"
    #22
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #23
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '':
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #24
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size == titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #25
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size == titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize == swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (swatchtiresize == swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    ########################
    #26
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #27
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #28
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    
    #29
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #30
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size == titletiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size == swatchtiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size == swatchhightiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize == swatchtiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize == swatchhightiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (swatchtiresize == swatchhightiresize) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #31
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (titletiresize == swatchtiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchhightiresize) or (titletiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == swatchtiresize) or (size == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    elif model == '' and partno == '' and size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    #32
    elif model == '' and partno == '' and size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and ((size == titletiresize) or (size == swatchtiresize) or (size == swatchhightiresize) or (titletiresize == swatchtiresize) or (titletiresize == swatchhightiresize) or (swatchtiresize == swatchhightiresize)) and (speedrating == swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Info Missing - Load Range"
    
    
    
    #Multiple info
    #7
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #8
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #9
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
        
    #11
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #12
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #13
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #14
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #15
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"

    #16
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #17
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    
    #18
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #19
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #20
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #21
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange != '' and titleloadrange != '' and aboutloadrange != '' and speedrating == '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (loadrange != titleloadrange) and (loadrange != aboutloadrange) and (titleloadrange != aboutloadrange):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    
    
    #24
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #25
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != titletiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #26
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    ################
    #27
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #28
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating == '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating == '' and swatchspeedrating != '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    
    #29
    elif size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange != '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #30
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != titletiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != swatchtiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize != swatchtiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (swatchtiresize != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #31
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize == '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != titletiresize) and (size != swatchtiresize) and (titletiresize != swatchtiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize != '' and swatchtiresize == '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != titletiresize) and (size != swatchhightiresize) and (titletiresize != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size != '' and titletiresize == '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != swatchtiresize) and (size != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    elif  size == '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    #32
    elif  size != '' and titletiresize != '' and swatchtiresize != '' and swatchhightiresize != '' and loadrange == '' and titleloadrange == '' and aboutloadrange == '' and speedrating != '' and swatchspeedrating != '' and (size != titletiresize) and (size != swatchtiresize) and (size != swatchhightiresize) and (titletiresize != swatchtiresize) and (titletiresize != swatchhightiresize) and (swatchtiresize != swatchhightiresize) and (speedrating != swatchspeedrating):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple Info"
    
    return matchtype,matchtypecomments


def videogamesmatchtype(platform,titleplatform,prodetplatform,swatchplatform,hardwareplatform):
    matchtype = ""
    matchtypecomments = ""

    platform = platform.lower().strip()
    swatchplatform = swatchplatform.lower().replace("digital code","").strip()
    hardwareplatform = hardwareplatform.lower()
    
    if titleplatform == 'pc' and 'windows' in platform.lower():
            platform = 'pc'
    
    #1
    if platform == '' and titleplatform == '' and prodetplatform == '' and swatchplatform == '' and hardwareplatform == '':
        matchtype = "Not Sure - Low confidence"
        matchtypecomments = "Info Missing - Platform"

    #2
    elif platform != '' and titleplatform != '' and prodetplatform == '' and swatchplatform == '' and hardwareplatform == '' and (platform != titleplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform == '' and (platform != prodetplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform == '' and swatchplatform != '' and hardwareplatform == '' and (platform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform == '' and swatchplatform == '' and hardwareplatform != '' and (platform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform != '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform == '' and (titleplatform != prodetplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform != '' and prodetplatform == '' and swatchplatform != '' and hardwareplatform == '' and (titleplatform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform != '' and prodetplatform == '' and swatchplatform == '' and hardwareplatform != '' and (titleplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform == '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform == '' and (prodetplatform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform == '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform != '' and (prodetplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform == '' and prodetplatform == '' and swatchplatform != '' and hardwareplatform != '' and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    
    
    elif platform != '' and titleplatform != '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform == '' and (platform != titleplatform) and (platform != prodetplatform) and (titleplatform != prodetplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform != '' and prodetplatform == '' and swatchplatform != '' and hardwareplatform == '' and (platform != titleplatform) and (platform != swatchplatform) and (titleplatform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform != '' and prodetplatform == '' and swatchplatform == '' and hardwareplatform != '' and (platform != titleplatform) and (platform != hardwareplatform) and (titleplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform == '' and (platform != prodetplatform) and (platform != swatchplatform) and (prodetplatform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform != '' and (platform != prodetplatform) and (platform != hardwareplatform) and (prodetplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform == '' and swatchplatform != '' and hardwareplatform != '' and (platform != swatchplatform) and (platform != hardwareplatform) and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform != '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform == '' and (titleplatform != prodetplatform) and (titleplatform != swatchplatform) and (prodetplatform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform != '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform != '' and (titleplatform != prodetplatform) and (titleplatform != hardwareplatform) and (prodetplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform == '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform != '' and (prodetplatform != swatchplatform) and (prodetplatform != hardwareplatform) and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    
    
    elif platform != '' and titleplatform != '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform == '' and (platform != titleplatform) and (platform != prodetplatform) and (platform != swatchplatform) and (titleplatform != prodetplatform) and (titleformat != swatchplatform) and (prodetplatform != swatchplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform != '' and prodetplatform != '' and swatchplatform == '' and hardwareplatform != '' and (platform != titleplatform) and (platform != prodetplatform) and (platform != hardwareplatform) and (titleplatform != prodetplatform) and (titleformat != hardwareplatform) and (prodetplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform != '' and prodetplatform == '' and swatchplatform != '' and hardwareplatform != '' and (platform != titleplatform) and (platform != swatchplatform) and (platform != hardwareplatform) and (titleplatform != swatchplatform) and (titleformat != hardwareplatform) and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform != '' and titleplatform == '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform != '' and (platform != prodetplatform) and (platform != swatchplatform) and (platform != hardwareplatform) and (prodetplatform != swatchplatform) and (prodetplatform != hardwareplatform) and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"
    elif platform == '' and titleplatform != '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform != '' and (titleplatform != prodetplatform) and (titleplatform != swatchplatform) and (titleplatform != hardwareplatform) and (prodetplatform != swatchplatform) and (prodetplatform != hardwareplatform) and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"

    elif platform != '' and titleplatform != '' and prodetplatform != '' and swatchplatform != '' and hardwareplatform != '' and (platform != titleplatform) and (platform != prodetplatform) and (platform != swatchplatform) and (platform != hardwareplatform) and (titleplatform != prodetplatform) and (titleformat != swatchplatform) and (titleplatform != hardwareplatform) and (prodetplatform != swatchplatform) and (prodetplatform != hardwareplatform) and (swatchplatform != hardwareplatform):
        matchtype = "Not Sure"
        matchtypecomments = "Multiple info"

    return matchtype,matchtypecomments

def clothingmatchtype(titleclothingsizelist, titlecolorlist,swatchcolor,swatchsize,prodetailclothingsize, prodetailcolor, color, size):  
        
        matchtype = ""
        matchtypecomments = ""
        swatchsize = swatchsize.strip()
        color = color.strip().lower()
        swatchcolor = swatchcolor.strip().lower()
        prodetailcolor = prodetailcolor.strip().lower()
        titlecolor = ""
        titleclothingsize = ""

        if titlecolorlist != []:
            if prodetailcolor in titlecolorlist:
                titlecolor = prodetailcolor
            elif color in titlecolorlist:
                titlecolor = color
            elif swatchcolor in titlecolorlist:
                titlecolor = swatchcolor
            else:
                if len(set(titlecolorlist)) == 1:
                  titlecolor = titlecolorlist
        else:
                titlecolor = ""
        
        if titleclothingsizelist != []:
            if prodetailclothingsize in titleclothingsizelist:
                titleclothingsize = prodetailclothingsize
            elif size in titleclothingsizelist:
                titleclothingsize = size
            elif swatchsize in titleclothingsizelist:
                titleclothingsize = swatchsize
            elif prodetailclothingsize == '' and size == '' and swatchsize == '' and len(set(titleclothingsizelist)) != 1:
                titleclothingsize = titleclothingsizelist
            else:
                if len(set(titleclothingsizelist)) == 1:
                    titleclothingsize = titleclothingsizelist
        else:
                titleclothingsize = ""
        
        if  size == '' and color == '' and titlecolor == '' and titleclothingsize == '' and prodetailcolor == ''  and prodetailclothingsize == '' and swatchsize == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size/ Color"
        elif titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and size == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '' :
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        #1 Colour - No
        elif size != '' and titleclothingsize != '' and prodetailclothingsize != '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '' and (size == titleclothingsize) and (size == prodetailclothingsize) and (size == swatchsize):
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size != ''  and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == '' and titleclothingsize != '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == ''  and titleclothingsize == '' and prodetailclothingsize != '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        #2 
        elif size != '' and titleclothingsize != '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size != ''  and titleclothingsize == '' and prodetailclothingsize != '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size != '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == '' and titleclothingsize != '' and prodetailclothingsize != '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == '' and titleclothingsize != '' and prodetailclothingsize == '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == ''  and titleclothingsize == '' and prodetailclothingsize != '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"       
        #3
        elif size != '' and titleclothingsize != '' and prodetailclothingsize != '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size == '' and titleclothingsize != '' and prodetailclothingsize != '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size != '' and titleclothingsize == '' and prodetailclothingsize != '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        elif size != ''  and titleclothingsize != '' and prodetailclothingsize == '' and swatchsize != '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Color"
        #4 Size - No
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor != ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor != '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        #5
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor != ''  and prodetailcolor == '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor != ''  and prodetailcolor != '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor == ''  and prodetailcolor != '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor == ''  and prodetailcolor == '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == ''  and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor == ''  and prodetailcolor != '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor != ''  and prodetailcolor == '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        #5
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor != ''  and prodetailcolor != '' and swatchcolor == '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color == '' and titlecolor != ''  and prodetailcolor != '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor == ''  and prodetailcolor != '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        elif  size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor != ''  and prodetailcolor == '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"
        #6
        elif  size == '' and titleclothingsize == '' and prodetailclothingsize == '' and swatchsize == '' and color != '' and titlecolor != ''  and prodetailcolor != '' and swatchcolor != '':
            matchtype = "Not Sure"
            matchtypecomments = "Info Missing - Size"

        #7 - Multiple Info
        elif titleclothingsize == '' and prodetailclothingsize != '' and swatchsize == '' and size != ''  and (prodetailclothingsize != size):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titleclothingsize != '' and prodetailclothingsize != '' and swatchsize == '' and size != '' and (titleclothingsize != prodetailclothingsize) and (prodetailclothingsize != size) and (titleclothingsize != size):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titleclothingsize != '' and prodetailclothingsize == ''  and swatchsize == '' and size != '' and (titleclothingsize != size):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titleclothingsize != '' and prodetailclothingsize != '' and size != '' and swatchsize != '' and (titleclothingsize != swatchsize) and (prodetailclothingsize != size) and (size != swatchsize) and (titleclothingsize != prodetailclothingsize):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titleclothingsize != '' and prodetailclothingsize != '' and size != '' and swatchsize != '' and (prodetailclothingsize != titleclothingsize) and (titleclothingsize != size) and (titleclothingsize != swatchsize) and (prodetailclothingsize != size) and (prodetailclothingsize != swatchsize) and (size != swatchsize):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titlecolor == '' and prodetailcolor != '' and color != '' and swatchcolor == '' and (prodetailcolor != color):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titlecolor != '' and prodetailcolor != '' and color != '' and swatchcolor == '' and (prodetailcolor != color) and (titlecolor != color):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titlecolor != '' and prodetailcolor == '' and color != '' and swatchcolor == '' and (titlecolor != color):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titlecolor != '' and prodetailcolor != '' and color != '' and swatchcolor != '' and (prodetailcolor != color) and (titlecolor != swatchcolor) and (titlecolor != color):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif titlecolor != '' and prodetailcolor != '' and color != '' and swatchcolor != '' and (prodetailcolor != titlecolor) and (titlecolor != color) and (titlecolor != swatchcolor) and (prodetailcolor != color) and (prodetailcolor != swatchcolor) and (color != swatchcolor):
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        elif (titlecolor != '' or prodetailcolor != '' or color != '' or swatchcolor != '') and prodetailclothingsize == '' and size == '' and swatchsize == '' and len(set(titleclothingsize)) != 1:
            matchtype = "Not Sure"
            matchtypecomments = "Multiple Info"
        return matchtype,matchtypecomments

tcount = 0

def AttributeExtraction(lines):

    bbprice = bbprice1 = bprice1 = listprice = x = bp = bpp = sp = swatch = swatchhl = info_select = info_unselect = brand = gender = color = iformat = ""
    manuf = partno = model = pack = shape = dimen = size = titlecard = brandtitle = my_list = aboutitem = productoverview = productdetails = productinfo = ""
    imageurl = bd = titleformat = prodetailISBN13 = prodetailISBN10 = titleISBN13 = titleISBN10 = modelnumber = disman = fdate = asin = countryo = material = metalstamp = metal = gemtype = ""
    totalgemweight = unitcount = itemdim = pageinfo = biketype = agerange = wheelsize = pattern = numberofitems = batteries = capacity = covermat = style = ""
    fillmat = pillowtype = specialfeature = procar = season = fabrictype = itemthickness = finishtype = formfact = powersource = inoutusage = heatingmethod ="" 
    recomuseforpro = itvolume = breadcrumb = itemw = publisher = language = pagecount = matchtype = matchtypecomments = isbn = isbn1 = highformat = highprice = ""
    setting = width = numberofstones = stoneweight = ""
    mpaarating = director = duration = releasedate = actors = studio = numberofdisc = ""
    genre = contributor = audiodesc = dubbed = subtitles = producers = aspectratio = mediaformat = ""
    bodymaterial = materialtype = instrumentkey = label = titleformats = unhighlitedformat = ""

    rimsize = secwidth = tireaspectratio = loadindexrating = speedrating = loadcapacity = treaddepth = treadtype = ""
    rimwidth = tirediameter = oempartno = construction = titletiresize = swatchtiresize = swatchhightiresize = ""
    loadrange = titleloadrange = aboutloadrange = swatchspeedrating = swatchloadindexrating = ""
    review = ship = sold = ""

    hardwareinterface = compatibledevices = totalusbport = noofports = totalhdmiports = connectortype = ""
    cabletype =  modelname = hardwareplatform = ops = pricing = typeofitem = titleplatform = platform = swatchplatform = prodetplatform = ''
    prodetplatformlist = ''

    titlecolor = titleclothingsize = prodetailcolor = prodetailclothingsize = swatchcolor = swatchsize = ""

    titlecolorlist = []
    titleclothingsizelist = []

    driver.get(lines[3])
    try:
        ele = WebDriverWait(driver, 15).until( #using explicit wait for 10 seconds
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2")) #checking for the element with 'h2'as its CSS
    )
    except:
        print("Timeout Exception: Page did not load within 15 seconds.")

    cursor.execute('UPDATE "ECHO_AE_AZ_In" SET "Record_Status" = (%s) WHERE "Batch_ID" = (%s) and "AZ_URL" = (%s);',('Initiated',Batch ,lines[2]))
    connection.commit()

    pgproblem = ''
    temp = 0
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pgproblem = soup.find('title').get_text().strip()
        if pgproblem == "ERROR: The request could not be satisfied" and temp < 5:
            time.sleep(3)
            driver.refresh()
            temp = temp + 1
            print(temp)
        else:
            break

    search_music = 'Amazon Music'
    amazonmusic = soup.find('title')
    amazonmusic = amazonmusic.find_all(string=re.compile('.*{0}.*'.format(search_music)), recursive=True)
    if pgproblem == "Page Not Found":
        pgproblem = "Competitor page problem"
    elif pgproblem == "Amazon.com Page Not Found":
        pgproblem = "Competitor page problem"
    elif len(amazonmusic) != 0:
        pgproblem = "Amazon Music"
    else:
        pgproblem = "Not a page problem"

    if pgproblem == "Not a page problem":
        # retrieving product title
        try:
            title = soup.find("span", attrs={"id": 'productTitle'})
            title_value = title.string
            titlecard = title_value.strip().replace(',', '')
        except AttributeError:
            titlecard = "NA"

        # Brand
        stopwords = ['Visit the', 'Store', 'Brand:']
        br = soup.find("a", attrs={"id": "bylineInfo"})
        if br != None:
            br = br.text.strip()
            for i in stopwords:
                n = br.replace(i, '')
                br = n
            brandtitle = br
        else:
            br = soup.find("a", class_="a-link-normal contributorNameID")
            if br != None:
                br = br.text.strip()
            brandtitle = br

        # retrieving price
        try:
            price = soup.find("span", class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
            if price is None:
                price = soup.find("span", class_="a-color-price header-price a-text-normal")
                if price is None:
                    price = soup.find("span", class_="a-price a-text-price a-size-medium apexPriceToPay")
                    if price is None:
                        price = soup.find("span", class_="a-size-base a-color-price a-color-price")
                        if price is None:
                            price = soup.find("span", class_="audible_mm_price")
                            if price is None:
                                li = soup.find("li", class_="swatchElement selected")
                                price = li.find("span", class_="a-color-base")


            listprice = price.text.strip().replace("from","")
        except AttributeError:
            pass
            
        try:
            breadcrumbtag = soup.find("ul", class_="a-unordered-list a-horizontal a-size-small")
            breadcrumb = breadcrumbtag.text
            #print("Breadcrumb=", breadcrumb)
        except:
            pass
            
        #Product Information
        try:
            abb = soup.find("table", attrs={"id": "productDetails_detailBullets_sections1"})
            if abb != None:
                i = abb.find_all("tr")
                for j in i:
                    p = j.find_all("th", class_="a-color-secondary a-size-base prodDetSectionEntry")
                    p1 = j.find_all("td", class_="a-size-base prodDetAttrValue")
                    if p != None or p1 != None:
                        for j in p:
                            p = j.text.replace('\u200f\n', '')
                            p = p.replace('\u200e\n', '')
                            p = p.replace('\n', '')
                            p = p.replace(':', '')
                            p = p.strip()

                        for k in p1:
                            p1 = k.text.strip()
                            if p == "Brand" or p == "Brand Name":
                                brand = p1
                                brand = brand.replace("\â€”", '')
                                #print("brand =", brand)
                            if p == "Gender":
                                gender = p1
                                #print("gender =", gender)
                            if p == "Color" or p == "Color Name":
                                color = p1
                                #print("color =",color)
                            if p == "Format":
                                iformat = p1
                                #print("iformat =",iformat )
                            if p == "Manufacturer":
                                manuf = p1
                                #print("manuf =",manuf )
                            if p == "Manufacturer Part Number":
                                partno = p1
                                #print("partno =",partno )
                            if p == "Model":
                                model = p1
                                #print("model =", model)
                            if p == "Count Per Pack":
                                pack = p1
                                #print("pack =", pack)
                            if p == "Shape":
                                shape = p1
                                #print("shape=", shape)
                            if p == "Product Dimensions" or p == "Package Dimensions":
                                dimen = p1
                                #print("dimen =", dimen)
                            if p == "Size":
                                size = p1
                                #print("size=", size)
                            if p == "ASIN":
                                asin = p1
                                #print("Asin =", asin)
                            if p == "Item Weight":
                                itemw = p1
                                #print("Item Weight =", itemw)
                            if p == "Department":
                                gender = p1
                                if gender == "unisex-adult":
                                    gender = "Unisex"
                                    #print("Gender =", gender)
                            if p == "Bike Type":
                                biketype = p1
                                #print("Bike Type =", biketype)
                            if p == "Age Range (Description)":
                                agerange = p1
                                #print("Age Range =", agerange )
                            if p == "Wheel Size":
                                wheelsize = p1
                                #print("Wheel Size =", wheelsize)
                            if p == "Pattern":
                                pattern = p1
                                #print("Pattern =", pattern)
                            if p == "Material":
                                material = p1
                                #print("Material =", material)
                            if p == "Unit Count":
                                unitcount = p1
                                #print("Unit Count =", unitcount)
                            if p == "Number of Items":
                                numberofitems = p1
                                #print("Number of Items=", numberofitems)
                            if p == "Batteries":
                                batteries = p1
                                #print("Batteries =", batteries)
                            if p == "Date First Available":
                                fdate = p1
                                #print("Date First Available =", fdate)
                            if p == "Country of Origin":
                                countryo = p1
                                #print("Country of Origin =", countryo)
                            if p == "Cover Material":
                                covermat = p1
                                #print("Cover Material =", covermat)
                            if p == "Style":
                                style = p1
                                #print("Style =", style)
                            if p == "Fill Material":
                                fillmat = p1
                                #print("Fill Material =", fillmat)
                            if p == "Pillow Type":
                                pillowtype = p1
                                #print("Pillow Type =", pillowtype)
                            if p == "Special Feature":
                                specialfeature = p1
                                #print("Special Feature =", specialfeature)
                            if p == "Product Care Instructions":
                                procar = p1
                                #print("Product Care Instructions =", procar)
                            if p == "Seasons":
                                season = p1
                                #print("Seasons =", season)
                            if p == "Fabric Type":
                                fabrictype = p1
                                #print("Fabric Type =", fabrictype)
                            if p == "Item Thickness":
                                itemthickness = p1
                                #print("Item Thickness =", itemthickness)
                            if p == "Finish Type":
                                finishtype = p1
                                #print("Finish Type =", finishtype)
                            if p == "Form Factor":
                                formfact = p1
                                #print("Form Factor =", formfact)
                            if p == "Indoor/Outdoor Usage":
                                inoutusage = p1
                                #print("Indoor/Outdoor Usage =", inoutusage)
                            if p == "Power Source":
                                powersource = p1
                                #print("Power Source =", powersource)
                            if p == "Heating Method":
                                heatingmethod = p1
                                #print("Heating Method =", heatingmethod)
                            if p == "Recommended Uses For Product":
                                recomuseforpro = p1
                                #print("Recommended Uses For Product =", recomuseforpro)
                            if p == "Item model number":
                                modelnumber = p1
                                #print("Item model number =", modelnumber)
                            #Movies & TV 
                            if p == "MPAA rating":
                                mpaarating = p1
                                #print("MPAA rating=", mpaarating)
                            if p == "Director":
                                director = infodata.exte.strip()
                                #print("Director=",director) 
                            if p == "Run time":
                                duration = p1
                                #print("Run time=",duration)
                            if p == "Release date" or p == "Original Release Date":
                                releasedate = p1
                                #print("Release date=",releasedate)
                            if p == "Actors":
                                actors = p1
                                #print("Actors=",actors)
                            if p == "Studio":
                                studio = p1
                                #print("Studio=",studio)
                            if p == "Number of discs":
                                numberofdisc = p1
                                #print("Number of discs=",numberofdisc)   
                            if p == "Genre":
                                genre = p1
                                #print("Genre=",genre)
                            if p == "Contributor":
                                contributor = p1
                                #print("Contributor=",contributor)
                            if p == "Audio Description":
                                audiodesc= p1
                                #print("Audio Description=",audiodesc)   
                            if p == "Dubbed":
                                dubbed = p1
                                #print("Dubbed=",dubbed)   
                            if p == "Subtitles":
                                subtitles = p1
                                #print("Subtitles=",subtitles)   
                            if p == "Producers":
                                producers = p1
                                #print("Producers=",producers)   
                            if p == "Aspect Ratio":
                                aspectratio = p1
                                #print("Aspect Ratio=",aspectratio) 
                            if p == "Media Format":
                                mediaformat = p1
                                #print("Media Format=",mediaformat) 
                            #Music
                            if p == "Body Material":
                                bodymaterial = p1
                                #print("Body Material=",bodymaterial)  
                            if p == "Material Type":
                                materialtype = p1
                                #print("Material Type=",materialtype)
                            if p == "Instrument Key":
                                instrumentkey = p1
                                #print("Instrument Key=",instrumentkey)   
                            if p == "Label":
                                label = p1
                                #print("Label=",label)
                            if p == "Ply Rating":
                                loadrange = p1
                             #Video Games
                            if p == "Pricing":
                                pricing = p1
                            if p == "Type of item":
                                typeofitem = p1

        except:
            pass

          #Product Information
        try:
            abb = soup.find("table", attrs={"id": "productDetails_techSpec_section_1"})
            if abb != None:
                i = abb.find_all("tr")
                for j in i:
                    p = j.find_all("th", class_="a-color-secondary a-size-base prodDetSectionEntry")
                    p1 = j.find_all("td", class_="a-size-base prodDetAttrValue")
                    if p != None or p1 != None:
                        for j in p:
                            p = j.text.replace('\u200f\n', '')
                            p = p.replace('\u200e\n', '')
                            p = p.replace('\n', '')
                            p = p.replace(':', '')
                            p = p.strip()
                            
                        for k in p1:
                            p1 = k.text.strip()
                            if p == "Brand" or p == "Brand Name":
                                brand = p1
                                brand = brand.replace("\â€”", '')
                                #print("brand =", brand)
                            if p == "Gender":
                                gender = p1
                                #print("gender =", gender)
                            if p == "Color" or p == "Color Name":
                                color = p1
                                #print("color =",color)
                            if p == "Format":
                                iformat = p1
                                #print("iformat =",iformat )
                            if p == "Manufacturer":
                                manuf = p1
                                #print("manuf =",manuf )
                            if p == "Manufacturer Part Number":
                                partno = p1
                                #print("partno =",partno )
                            if p == "Model":
                                model = p1
                                #print("model =", model)
                            if p == "Count Per Pack":
                                pack = p1
                                #print("pack =", pack)
                            if p == "Shape":
                                shape = p1
                                #print("shape=", shape)
                            if p == "Product Dimensions" or p == "Package Dimensions" or p == "Item Dimensions LxWxH":
                                dimen = p1
                                #print("dimen =", dimen)
                            if p == "Size":
                                size = p1
                                #print("size=", size)
                            if p == "ASIN":
                                asin = p1
                                #print("Asin =", asin)
                            if p == "Item Weight":
                                itemw = p1
                                #print("Item Weight =", itemw)
                            if p == "Department":
                                gender = p1
                                if gender == "unisex-adult":
                                    gender = "Unisex"
                                    #print("Gender =", gender)
                            if p == "Bike Type":
                                biketype = p1
                                #print("Bike Type =", biketype)
                            if p == "Age Range (Description)":
                                agerange = p1
                                #print("Age Range =", agerange )
                            if p == "Wheel Size":
                                wheelsize = p1
                                #print("Wheel Size =", wheelsize)
                            if p == "Pattern":
                                pattern = p1
                                #print("Pattern =", pattern)
                            if p == "Material":
                                material = p1
                                #print("Material =", material)
                            if p == "Unit Count":
                                unitcount = p1
                                #print("Unit Count =", unitcount)
                            if p == "Number of Items":
                                numberofitems = p1
                                #print("Number of Items=", numberofitems)
                            if p == "Batteries":
                                batteries = p1
                                #print("Batteries =", batteries)
                            if p == "Date First Available":
                                fdate = p1
                                #print("Date First Available =", fdate)
                            if p == "Country of Origin":
                                countryo = p1
                                #print("Country of Origin =", countryo)
                            if p == "Cover Material":
                                covermat = p1
                                #print("Cover Material =", covermat)
                            if p == "Style":
                                style = p1
                                #print("Style =", style)
                            if p == "Fill Material":
                                fillmat = p1
                                #print("Fill Material =", fillmat)
                            if p == "Pillow Type":
                                pillowtype = p1
                                #print("Pillow Type =", pillowtype)
                            if p == "Special Feature":
                                specialfeature = p1
                                #print("Special Feature =", specialfeature)
                            if p == "Product Care Instructions":
                                procar = p1
                                #print("Product Care Instructions =", procar)
                            if p == "Seasons":
                                season = p1
                                #print("Seasons =", season)
                            if p == "Fabric Type":
                                fabrictype = p1
                                #print("Fabric Type =", fabrictype)
                            if p == "Item Thickness":
                                itemthickness = p1
                                #print("Item Thickness =", itemthickness)
                            if p == "Finish Type":
                                finishtype = p1
                                #print("Finish Type =", finishtype)
                            if p == "Form Factor":
                                formfact = p1
                                #print("Form Factor =", formfact)
                            if p == "Indoor/Outdoor Usage":
                                inoutusage = p1
                                #print("Indoor/Outdoor Usage =", inoutusage)
                            if p == "Power Source":
                                powersource = p1
                                #print("Power Source =", powersource)
                            if p == "Heating Method":
                                heatingmethod = p1
                                #print("Heating Method =", heatingmethod)
                            if p == "Recommended Uses For Product":
                                recomuseforpro = p1
                                #print("Recommended Uses For Product =", recomuseforpro)
                            if p == "Item model number":
                                modelnumber = p1
                                #print("Item model number =", modelnumber)
                            #Movies & TV 
                            if p == "MPAA rating":
                                mpaarating = p1
                                #print("MPAA rating=", mpaarating)
                            if p == "Director":
                                director = infodata.exte.strip()
                                #print("Director=",director) 
                            if p == "Run time":
                                duration = p1
                                #print("Run time=",duration)
                            if p == "Release date" or p == "Original Release Date":
                                releasedate = p1
                                #print("Release date=",releasedate)
                            if p == "Actors":
                                actors = p1
                                #print("Actors=",actors)
                            if p == "Studio":
                                studio = p1
                                #print("Studio=",studio)
                            if p == "Number of discs":
                                numberofdisc = p1
                                #print("Number of discs=",numberofdisc)   
                            if p == "Genre":
                                genre = p1
                                #print("Genre=",genre)
                            if p == "Contributor":
                                contributor = p1
                                #print("Contributor=",contributor)
                            if p == "Audio Description":
                                audiodesc= p1
                                #print("Audio Description=",audiodesc)   
                            if p == "Dubbed":
                                dubbed = p1
                                #print("Dubbed=",dubbed)   
                            if p == "Subtitles":
                                subtitles = p1
                                #print("Subtitles=",subtitles)   
                            if p == "Producers":
                                producers = p1
                                #print("Producers=",producers)   
                            if p == "Aspect Ratio":
                                aspectratio = p1
                                #print("Aspect Ratio=",aspectratio) 
                            if p == "Media Format":
                                mediaformat = p1
                                #print("Media Format=",mediaformat) 
                            #Music
                            if p == "Body Material":
                                bodymaterial = p1
                                #print("Body Material=",bodymaterial)  
                            if p == "Material Type":
                                materialtype = p1
                                #print("Material Type=",materialtype)
                            if p == "Instrument Key":
                                instrumentkey = p1
                                #print("Instrument Key=",instrumentkey)   
                            if p == "Label":
                                label = p1
                                #print("Label=",label)
                            
                            #Auto & Tires
                            if p == "Rim Size":
                                rimsize = p1
                                #print("Rim Size= ",rimsize)
                            if p == "Section Width":
                                secwidth = p1
                                #print("Section Width= ",secwidth)
                            if p == "Tire Aspect Ratio":
                                tireaspectratio = p1
                                #print("Tire Aspect Ratio=",tireaspectratio)
                            if p == "Load Index Rating":
                                loadindexrating = p1
                                #print("Load Index Rating =",loadindexrating)
                            if p == "Speed Rating":
                                speedrating = p1
                                #print("Speed Rating =",speedrating)
                            if p == "Load Capacity":
                                loadcapacity = p1
                                #print("Load Capacity =",loadcapacity)
                            if p == "Tread Depth":
                                treaddepth = p1
                                #print("Tread Depth =",treaddepth)
                            if p == "Tread Type":
                                treadtype = p1
                                #print("Tread Type =",treadtype)
                            if p == "Rim Width":
                                rimwidth = p1
                                #print("Rim Width =",rimwidth)
                            if p == "Tire Diameter":
                                tirediameter= p1
                                #print("Tire Diameter =",tirediameter)
                            if p == "OEM Part Number":
                                oempartno= p1
                                #print("OEM Part Number =",oempartno)
                            if p == "Construction":
                                construction = p1
                                #print("Construction =",construction)
                            if p == "Ply Rating":
                                loadrange = p1
                                #print("Ply Rating =", loadrange)
                            #Videogames
                            if p == "Hardware Platform":
                                hardwareplatform = p1
        except:
            pass
        
        #Swatch Color name
        if color == '':
            title = soup.find("div", attrs={"id": "variation_color_name"})
            if title != None:
                title1 = title.find("div", class_="a-row")
                if title1 != None:
                    col = title1.find("label", class_="a-form-label")
                    if col != None:
                        colorname = col.text.strip()
                        if colorname != None:
                            if colorname == 'Color:':
                                color = title1.find("span", class_="selection")
                                if color != None:
                                    color = color.text.strip()
                                    # print("Color1 =", color)
                                else:
                                    title = title.find("select",
                                                       attrs={"id": "native_dropdown_selected_color_name"})
                                    if title != None:
                                        title = title.find("option", class_="dropdownSelect")
                                        if title != None:
                                            color = title.text.strip()
                                            # print("Color1 =", color)
        #Swatch Details size
        if size == '':
            title = soup.find("div", attrs={"id": "variation_size_name"})
            if title != None:
                title1 = title.find("div", class_="a-row")
                if title1 != None:
                    title1 = title1.find("label", class_="a-form-label")
                    if title1 != None:
                        c1 = title1.text.strip()
                        if c1 != None:
                            if c1 == 'Size:':
                                size = title1.find("span", class_="selection")
                                if size != None:
                                    size = size.text.strip()
                                    # print("Size1 =", size)
                                else:
                                    title = title.find("select", attrs={"id": "native_dropdown_selected_size_name"})
                                    if title != None:
                                        title = title.find("option", class_="dropdownSelect")
                                        if title != None:
                                            size = title.text.strip()
                                            # print("Size1 =", size)
        #Swatch Details Style                                   
        if style == '':
            title = soup.find("div", attrs={"id": "variation_style_name"})
            if title != None:
                title1 = title.find("div", class_="a-row")
                if title1 != None:
                    title1 = title1.find("label", class_="a-form-label")
                    if title1 != None:
                        c1 = title1.text.strip()
                        if c1 != None:
                            if c1 == 'Size:':
                                style = title1.find("span", class_="selection")
                                if style != None:
                                    style = style.text.strip()
                                    # print("Style1 =", style)
                                else:
                                    title = title.find("select", attrs={"id": "native_dropdown_selected_size_name"})
                                    if title != None:
                                        title = title.find("option", class_="dropdownSelect")
                                        if title != None:
                                            style = title.text.strip()
                                            # print("Style1 =", style)

        if gender == '':
            abb = soup.find("div", attrs={"id": "feature-bullets"})
            if abb != None:
                about = abb.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
                if about != None:
                    about = about.find_all("span", class_="a-list-item")
                    if about != None:
                        for ab in about:
                            aboutt = ab.text.strip()
                            if aboutt == 'Gender: Women':
                                gender = "Female"
                                # print("gender = ", gender)

        #Product Details
        abb = soup.find("div", attrs={"id": "detailBullets_feature_div"})
        if abb != None:
            abb = abb.find_all("span", class_="a-list-item")
            if abb != None:
                for i in abb:
                    p = i.find_all("span", class_="a-text-bold")
                    p1 = i.find_all("span")
                    if p != None or p1 != None:
                        for j in p:
                            p = j.text.replace('\u200f\n', '')
                            p = p.replace('\u200e\n', '')
                            p = p.replace('\n', '')
                            p = p.replace(':', '')
                            p = p.strip()

                        for k in p1:
                            p1 = k.text.strip()
                        if modelnumber == '':
                            if p == "Item model number":
                                modelnumber = p1
                                # print("model =", modelnumber)
                        if gender == '':
                            if p == "Department":
                                if p1 == 'Womens' or p1 == 'womens':
                                    gender = 'Female'
                                    # print("Gender =", gender)
                                elif p1 == 'Mens' or p1 == 'mens':
                                    gender = 'Male'
                                    # print("Gender =", gender)
                        if dimen == '':
                            if p == "Package Dimensions":
                                dimen = p1
                                # print("Dimension =", dimen)
                        if manuf == '':
                            if p == "Manufacturer":
                                manuf = p1
                                # print("manuf =",manuf )
                        if disman == '':
                            if p == "Is Discontinued By Manufacturer":
                                disman = p1
                                # print("Is Discontinued By Manufacturer=", disman)
                        if fdate == '':
                            if p == "Date First Available":
                                fdate = p1
                                # print("Date First Available=", fdate)
                        if asin == '':
                            if p == "ASIN":
                                asin = p1
                                # print("ASIN =", asin)
                        if countryo == '':
                            if p == "Country of Origin":
                                countryo = p1
                                # print("Country of Origin =", countryo)
                        if publisher == '':
                            if p == "Publisher":
                                publisher = p1
                                # print("Publisher =", publisher)
                        if language == '':
                            if p == "Language":
                                language = p1
                                # print("Language =", language)
                        if pagecount == '':
                            if p == "Paperback" or p == "Print length" or p == "Hardcover" or p == "Board Book" or p == "Calendar" or p == "Library Binding" or p == "Spiral-bound":
                                pagecount = p1
                                #print("Paperback =", paperpack)
                        if itemw == '':
                            if p == "Item Weight":
                                itemw = p1
                                # print("Item Weight =", itemw)
                        if isbn == '':
                            if p == "ISBN-10":
                                isbn = p1
                                # print("ISBN-10 =", isbn)
                        if isbn1 == '':
                            if p == "ISBN-13":
                                isbn1 = p1
                                # print("ISBN-13 =", isbn1)
                        #Movies & TV 
                        if mpaarating == '':
                            if p == "MPAA rating":
                                mpaarating = p1
                                #print("MPAA rating=", mpaarating)
                        if dimen == '':
                            if p == "Product Dimensions" or p == "Package Dimensions":
                                dimen = p1
                                #print("dimen =", dimen)
                        if director == '':
                            if p == "Director":
                                director = p1
                                #print("Director=",director)
                        if iformat == '':
                            if p == "Format":
                                iformat = p1
                                #print("Format=",iformat)
                        if mediaformat == '':
                            if p == "Media Format":
                                mediaformat = p1
                                #print("Media Format=",mediaformat)
                        if duration == '':
                            if p == "Run time":
                                duration = p1
                                #print("Run time=",duration)
                        if releasedate == '':
                            if p == "Release date":
                                releasedate = p1
                                #print("Release date=",releasedate)
                        if actors == '':
                            if p == "Actors":
                                actors = p1
                                #print("Actors=",actors)
                        if studio == '':
                            if p == "Studio":
                                studio = p1
                                #print("Studio=",studio)
                        if numberofdisc == '':
                            if p == "Number of discs":
                                numberofdisc = p1
                                #print("Number of discs=",numberofdisc)
                        if genre == '':
                            if p == "Genre":
                                genre = p1
                                #print("Genre=",genre)
                        if contributor == '':
                            if p == "Contributor":
                                contributor = p1
                                #print("Contributor=",contributor)
                        if audiodesc == '':
                            if p == "Audio Description":
                                audiodesc  = p1
                                #print("Audio Description=",audiodesc)
                        if dubbed == '':
                            if p == "Dubbed":
                                dubbed = p1
                                #print("Dubbed=",dubbed)
                        if subtitles == '':
                            if p == "Subtitles":
                                subtitles = p1
                                #print("Subtitles=",subtitles)
                        if producers == '':
                            if p == "Producers":
                                producers = p1
                                #print("Producers=",producers)
                        if aspectratio == '':
                            if p == "Aspect Ratio":
                                aspectratio = p1
                                #print("Aspect Ratio=",aspectratio)
                        if label == '':
                            if p == "Label":
                                label = p1
                                #print("Label=",label)
                        #Auto & Tires
                        if loadrange == '':
                            if p == "Ply Rating":
                                loadrange = p1

        #Product Details
        tagcount = 0
        bdd = soup.find("div", attrs={"id": "productOverview_feature_div"})
        if bdd != None:
            bd = bdd.find("table", class_="a-normal a-spacing-none a-spacing-top-base")
            if bd != None:
                title = bd.findAll('td', class_="a-span4")
                if title != None:
                    value = bd.findAll('td', class_='a-span6')
                    if value != None:
                        for headeritem in bd.findAll('td', class_="a-span4"):

                            infohead = title[tagcount]
                            infodata = value[tagcount]
                            tagcount = tagcount + 1
                            # print(infohead.text)
                            if brand == '':
                                if infohead.text.strip() == "Brand":
                                    brand = infodata.text.strip()
                                    # print("Brand1 =", brand)
                            if pageinfo == '':
                                if infohead.text.strip() == "Package Information" or infohead.text.strip() == "Package Dimensions":
                                    paginfo = infodata.text.strip()
                                    # print("Package Information =", paginfo)
                            if color == '':
                                if infohead.text.strip() == "Color" or infohead.text.strip() == "Ink Color":
                                    color = infodata.text.strip()
                                    # print("Color =",color)
                            if itvolume == '':
                                if infohead.text.strip() == "Item Volume":
                                    itvolume = infodata.text.strip()
                                    # print("Item Volume =", itvolume )
                            if material == '':
                                if infohead.text.strip() == "Material":
                                    material = infodata.text.strip()
                                    # print("Material =", material )
                            if size == '':
                                if infohead.text.strip() == "Size":
                                    size = infodata.text.strip()
                                    # print("Size =", size )
                            if unitcount == '':
                                if infohead.text.strip() == "Unit Count":
                                    unitcount = infodata.text.strip()
                                    # print("Unit Count =", unitcount)
                            if biketype == '':
                                if infohead.text.strip() == "Bike Type":
                                    biketype = infodata.text.strip()
                                    # print("Bike Type1 =", biketype)
                            if agerange == '':
                                if infohead.text.strip() == "Age Range (Description)":
                                    agerange = infodata.text.strip()
                                    # print("Age Range =", agerange )
                            if wheelsize == '':
                                if infohead.text.strip() == "Wheel Size":
                                    wheelsize = infodata.text.strip()
                                    # print("Wheel Size =", wheelsize)
                            if shape == '':
                                if infohead.text.strip() == "Shape":
                                    shape = infodata.text.strip()
                                    # print("Shape =", shape)
                            if pattern == '':
                                if infohead.text.strip() == "Pattern":
                                    pattern = infodata.text.strip()
                                    # print("Pattern =", pattern)
                            if capacity == '':
                                if infohead.text.strip() == "Capacity":
                                    capacity = infodata.text.strip()
                                    # print("Capacity =", capacity)
                            if fillmat == '':
                                if infohead.text.strip() == "Fill Material":
                                    fillmat = infodata.text.strip()
                                    # print("Fill Material =", fillmat)
                            if pillowtype == '':
                                if infohead.text.strip() == "Pillow Type":
                                    pillowtype = infodata.text.strip()
                                    # print("Pillow Type =", pillowtype)
                            if finishtype == '':
                                if infohead.text.strip() == "Finish Type":
                                    finishtype = infodata.text.strip()
                                    # print("Finish Type =", finishtype)
                            if formfact == '':
                                if infohead.text.strip() == "Form Factor":
                                    formfact = infodata.text.strip()
                                    # print("Form Factor =", formfact)
                            if inoutusage == '':
                                if infohead.text.strip() == "Indoor/Outdoor Usage":
                                    inoutusage = infodata.text.strip()
                                    # print("Indoor/Outdoor Usage =", inoutusage)
                            if powersource == '':
                                if infohead.text.strip() == "Power Source":
                                    powersource = infodata.text.strip()
                                    # print("Power Source =", powersource)
                            if heatingmethod == '':
                                if infohead.text.strip() == "Heating Method":
                                    heatingmethod = infodata.text.strip()
                                    # print("Heating Method =", heatingmethod)
                            if recomuseforpro == '':
                                if infohead.text.strip() == "Recommended Uses For Product":
                                    recomuseforpro = infodata.text.strip()
                                    # print("Recommended Uses For Product =", recomuseforpro)
                            if modelnumber == '':
                                if infohead.text.strip() == "Item model number":
                                    modelnumber = infodata.text.strip()
                                    # print("Item model number =", modelnumber)
                            if genre == '':
                                if infohead.text.strip() == "Genre":
                                    genre = infodata.text.strip()
                                    #print("Genre=",genre)
                            if contributor == '':
                                if infohead.text.strip() == "Contributor":
                                    contributor = infodata.text.strip()
                                    #print("Contributor=",contributor)
                            if duration == '':
                                if infohead.text.strip() == "Runtime":
                                    duration = infodata.text.strip()
                                    #print("Runtime=",duration)
                            if language == '':
                                if infohead.text.strip() == "Language":
                                    language = infodata.text.strip()
                                    #print("Language=",language)
                            if numberofdisc == '':
                                if infohead.text.strip() == "Number Of Discs":
                                    numberofdisc = infodata.text.strip()
                                    #print("Number Of Discs=",numberofdisc)
                            if instrumentkey == '':
                                if infohead.text.strip() == "Instrument Key":
                                    instrumentkey = infodata.text.strip()
                                    #print("Instrument Key=",instrumentkey) 

                            #Auto Tires
                            if rimsize == '':
                                if infohead.text.strip() == "Rim Size":
                                    rimsize = infodata.text.strip()
                                    #print("Rim Size= ",rimsize)
                            if secwidth == '':
                                if infohead.text.strip() == "Section Width":
                                    secwidth = infodata.text.strip()
                                    #print("Section Width= ",secwidth)
                            if tireaspectratio == '':
                                if infohead.text.strip() == "Tire Aspect Ratio":
                                    tireaspectratio = infodata.text.strip()
                                    #print("Tire Aspect Ratio=",tireaspectratio)
                            if loadindexrating == '':
                                if infohead.text.strip() == "Load Index Rating":
                                    loadindexrating = infodata.text.strip()
                                    #print("Load Index Rating =",loadindexrating)
                            if speedrating == '':
                                if infohead.text.strip() == "Speed Rating":
                                    speedrating = infodata.text.strip()
                                    #print("Speed Rating =",speedrating)
                            if loadcapacity == '':
                                if infohead.text.strip() == "Load Capacity":
                                    loadcapacity = infodata.text.strip()
                                    #print("Load Capacity =",loadcapacity)
                            if treaddepth == '':
                                if infohead.text.strip() == "Tread Depth":
                                    treaddepth = infodata.text.strip()
                                    #print("Tread Depth =",treaddepth)
                            if treadtype == '':
                                if infohead.text.strip() == "Tread Type":
                                    treadtype = infodata.text.strip()
                                    #print("Tread Type =",treaddepth)
                            if rimwidth == '':
                                if infohead.text.strip() == "Rim Width":
                                    rimwidth = infodata.text.strip()
                                    #print("Rim Width =",rimwidth)
                            if tirediameter == '':
                                if infohead.text.strip() == "Tire Diameter":
                                    tirediameter= infodata.text.strip()
                                    #print("Tire Diameter =",tirediameter)
                            if oempartno == '':
                                if infohead.text.strip() == "OEM Part Number":
                                    oempartno= infodata.text.strip()
                                    #print("OEM Part Number =",oempartno)
                            if construction == '':
                                if infohead.text.strip() == "Construction":
                                    construction = infodata.text.strip()
                                    #print("Construction =",construction)    
                            if season == '':
                                if infohead.text.strip() == "Seasons":
                                    season = infodata.text.strip()
                                    #print("Seasons =",season)  
                            if loadrange == '':
                                if infohead.text.strip() == "Ply Rating":
                                    loadrange = infodata.text.strip() 
                            #Videogames
                            if hardwareinterface == '':
                                if infohead.text.strip() == "Hardware Interface":
                                    hardwareinterface = infodata.text.strip()
                            if compatibledevices == '':
                                if infohead.text.strip() == "Compatible Devices":
                                    compatibledevices = infodata.text.strip()
                            if totalusbport == '':
                                if infohead.text.strip() == "Total USB Ports":
                                    totalusbport = infodata.text.strip()
                            if noofports == '':
                                if infohead.text.strip() == "Number of Ports":
                                    noofports = infodata.text.strip()
                            if totalhdmiports == '':
                                if infohead.text.strip() == "Total HDMI Ports":
                                    totalhdmiports = infodata.text.strip()
                            if itemw == '':
                                if infohead.text.strip() == "Item Weight":
                                    itemw = infodata.text.strip()
                            if connectortype == '':
                                if infohead.text.strip() == "Connector Type":
                                    connectortype = infodata.text.strip()
                            if cabletype == '':
                                if infohead.text.strip() == "Cable Type":
                                    cabletype = infodata.text.strip()
                            if specialfeature == '':
                                if infohead.text.strip() == "Special Feature":
                                    specialfeature = infodata.text.strip()
                            if modelname == '':
                                if infohead.text.strip() == "Model Name":
                                    modelname = infodata.text.strip()
                            if hardwareplatform == '':
                                if infohead.text.strip() == "Hardware Platform":
                                    hardwareplatform = infodata.text.strip()
                            if ops == '':
                                if infohead.text.strip() == "Operating System":
                                    ops = infodata.text.strip()           
        
        try:
                bd = bdd.find("table", class_="a-normal a-spacing-micro")
                tagcount = 0
                if bd != None:
                    title = bd.findAll('td', class_="a-span3")
                    if title != None:
                        value = bd.findAll('td', class_='a-span9')
                        if value != None:
                            for headeritem in bd.findAll('td', class_="a-span3"):

                                infohead = title[tagcount]
                                infodata = value[tagcount]
                                tagcount = tagcount + 1
                                # print(infohead.text)
                                if brand == '':
                                    if infohead.text.strip() == "Brand":
                                        brand = infodata.text.strip()
                                        # print("Brand1 =", brand)
                                if pageinfo == '':
                                    if infohead.text.strip() == "Package Information" or infohead.text.strip() == "Package Dimensions":
                                        paginfo = infodata.text.strip()
                                        # print("Package Information =", paginfo)
                                if color == '':
                                    if infohead.text.strip() == "Color" or infohead.text.strip() == "Ink Color":
                                        color = infodata.text.strip()
                                        # print("Color =",color)
                                if itvolume == '':
                                    if infohead.text.strip() == "Item Volume":
                                        itvolume = infodata.text.strip()
                                        # print("Item Volume =", itvolume )
                                if material == '':
                                    if infohead.text.strip() == "Material":
                                        material = infodata.text.strip()
                                        # print("Material =", material )
                                if size == '':
                                    if infohead.text.strip() == "Size":
                                        size = infodata.text.strip()
                                        # print("Size =", size )
                                if unitcount == '':
                                    if infohead.text.strip() == "Unit Count":
                                        unitcount = infodata.text.strip()
                                        # print("Unit Count =", unitcount)
                                if biketype == '':
                                    if infohead.text.strip() == "Bike Type":
                                        biketype = infodata.text.strip()
                                        # print("Bike Type1 =", biketype)
                                if agerange == '':
                                    if infohead.text.strip() == "Age Range (Description)":
                                        agerange = infodata.text.strip()
                                        # print("Age Range =", agerange )
                                if wheelsize == '':
                                    if infohead.text.strip() == "Wheel Size":
                                        wheelsize = infodata.text.strip()
                                        # print("Wheel Size =", wheelsize)
                                if shape == '':
                                    if infohead.text.strip() == "Shape":
                                        shape = infodata.text.strip()
                                        # print("Shape =", shape)
                                if pattern == '':
                                    if infohead.text.strip() == "Pattern":
                                        pattern = infodata.text.strip()
                                        # print("Pattern =", pattern)
                                if capacity == '':
                                    if infohead.text.strip() == "Capacity":
                                        capacity = infodata.text.strip()
                                        # print("Capacity =", capacity)
                                if fillmat == '':
                                    if infohead.text.strip() == "Fill Material":
                                        fillmat = infodata.text.strip()
                                        # print("Fill Material =", fillmat)
                                if pillowtype == '':
                                    if infohead.text.strip() == "Pillow Type":
                                        pillowtype = infodata.text.strip()
                                        # print("Pillow Type =", pillowtype)
                                if finishtype == '':
                                    if infohead.text.strip() == "Finish Type":
                                        finishtype = infodata.text.strip()
                                        # print("Finish Type =", finishtype)
                                if formfact == '':
                                    if infohead.text.strip() == "Form Factor":
                                        formfact = infodata.text.strip()
                                        # print("Form Factor =", formfact)
                                if inoutusage == '':
                                    if infohead.text.strip() == "Indoor/Outdoor Usage":
                                        inoutusage = infodata.text.strip()
                                        # print("Indoor/Outdoor Usage =", inoutusage)
                                if powersource == '':
                                    if infohead.text.strip() == "Power Source":
                                        powersource = infodata.text.strip()
                                        # print("Power Source =", powersource)
                                if heatingmethod == '':
                                    if infohead.text.strip() == "Heating Method":
                                        heatingmethod = infodata.text.strip()
                                        # print("Heating Method =", heatingmethod)
                                if recomuseforpro == '':
                                    if infohead.text.strip() == "Recommended Uses For Product":
                                        recomuseforpro = infodata.text.strip()
                                        # print("Recommended Uses For Product =", recomuseforpro)
                                if modelnumber == '':
                                    if infohead.text.strip() == "Item model number":
                                        modelnumber = infodata.text.strip()
                                        # print("Item model number =", modelnumber)
                                if genre == '':
                                    if infohead.text.strip() == "Genre":
                                        genre = infodata.text.strip()
                                        #print("Genre=",genre)
                                if contributor == '':
                                    if infohead.text.strip() == "Contributor":
                                        contributor = infodata.text.strip()
                                        #print("Contributor=",contributor)
                                if duration == '':
                                    if infohead.text.strip() == "Runtime":
                                        duration = infodata.text.strip()
                                        #print("Runtime=",duration)
                                if language == '':
                                    if infohead.text.strip() == "Language":
                                        language = infodata.text.strip()
                                        #print("Language=",language)
                                if numberofdisc == '':
                                    if infohead.text.strip() == "Number Of Discs":
                                        numberofdisc = infodata.text.strip()
                                        #print("Number Of Discs=",numberofdisc)
                                if instrumentkey == '':
                                    if infohead.text.strip() == "Instrument Key":
                                        instrumentkey = infodata.text.strip()
                                        #print("Instrument Key=",instrumentkey)  
                                #Auto Tires
                                if rimsize == '':
                                    if infohead.text.strip() == "Rim Size":
                                        rimsize = infodata.text.strip()
                                        #print("Rim Size= ",rimsize)
                                if secwidth == '':
                                    if infohead.text.strip() == "Section Width":
                                        secwidth = infodata.text.strip()
                                        #print("Section Width= ",secwidth)
                                if tireaspectratio == '':
                                    if infohead.text.strip() == "Tire Aspect Ratio":
                                        tireaspectratio = infodata.text.strip()
                                        #print("Tire Aspect Ratio=",tireaspectratio)
                                if loadindexrating == '':
                                    if infohead.text.strip() == "Load Index Rating":
                                        loadindexrating = infodata.text.strip()
                                        #print("Load Index Rating =",loadindexrating)
                                if speedrating == '':
                                    if infohead.text.strip() == "Speed Rating":
                                        speedrating = infodata.text.strip()
                                        #print("Speed Rating =",speedrating)
                                if loadcapacity == '':
                                    if infohead.text.strip() == "Load Capacity":
                                        loadcapacity = infodata.text.strip()
                                        #print("Load Capacity =",loadcapacity)
                                if treaddepth == '':
                                    if infohead.text.strip() == "Tread Depth":
                                        treaddepth = infodata.text.strip()
                                        #print("Tread Depth =",treaddepth)
                                if treadtype == '':
                                    if infohead.text.strip() == "Tread Type":
                                        treadtype = infodata.text.strip()
                                        #print("Tread Type =",treaddepth)
                                if rimwidth == '':
                                    if infohead.text.strip() == "Rim Width":
                                        rimwidth = infodata.text.strip()
                                        #print("Rim Width =",rimwidth)
                                if tirediameter == '':
                                    if infohead.text.strip() == "Tire Diameter":
                                        tirediameter= infodata.text.strip()
                                        #print("Tire Diameter =",tirediameter)
                                if oempartno == '':
                                    if infohead.text.strip() == "OEM Part Number":
                                        oempartno= infodata.text.strip()
                                        #print("OEM Part Number =",oempartno)
                                if construction == '':
                                    if infohead.text.strip() == "Construction":
                                        construction = infodata.text.strip()
                                        #print("Construction =",construction)
                                if season == '':
                                    if infohead.text.strip() == "Seasons":
                                        season = infodata.text.strip()
                                        #print("Seasons =",season)
                                if loadrange == '':
                                    if infohead.text.strip() == "Ply Rating":
                                        loadrange = infodata.text.strip()
                                #Videogames

                                if hardwareinterface == '':
                                    if infohead.text.strip() == "Hardware Interface":
                                        hardwareinterface = infodata.text.strip()
                                if compatibledevices == '':
                                    if infohead.text.strip() == "Compatible Devices":
                                        compatibledevices = infodata.text.strip()
                                if totalusbport == '':
                                    if infohead.text.strip() == "Total USB Ports":
                                        totalusbport = infodata.text.strip()
                                if noofports == '':
                                    if infohead.text.strip() == "Number of Ports":
                                        noofports = infodata.text.strip()
                                if totalhdmiports == '':
                                    if infohead.text.strip() == "Total HDMI Ports":
                                        totalhdmiports = infodata.text.strip()
                                if itemw == '':
                                    if infohead.text.strip() == "Item Weight":
                                        itemw = infodata.text.strip()
                                if connectortype == '':
                                    if infohead.text.strip() == "Connector Type":
                                        connectortype = infodata.text.strip()
                                if cabletype == '':
                                    if infohead.text.strip() == "Cable Type":
                                        cabletype = infodata.text.strip()
                                if specialfeature == '':
                                    if infohead.text.strip() == "Special Feature":
                                        specialfeature = infodata.text.strip()
                                if modelname == '':
                                    if infohead.text.strip() == "Model Name":
                                        modelname = infodata.text.strip()
                                if hardwareplatform == '':
                                    if infohead.text.strip() == "Hardware Platform":
                                        hardwareplatform = infodata.text.strip()
                                if ops == '':
                                    if infohead.text.strip() == "Operating System":
                                        ops = infodata.text.strip()
        except:
            pass

        # if material == '' or countryo == '' or unitcount == '':
        tagcount = 0
        mt = soup.find_all("div", class_="a-fixed-left-grid product-facts-detail")
        if mt != None:
            for i in mt:
                title = i.findAll('div', class_="a-fixed-left-grid-col a-col-left")
                if title != None:
                    value = i.findAll('div', class_='a-fixed-left-grid-col a-col-right')
                    if value != None:
                        for headeritem in i.findAll('div', class_="a-fixed-left-grid-col a-col-left"):
                            infohead = title[tagcount]
                            infodata = value[tagcount]
                            # tagcount = tagcount + 1
                            if material == '':
                                if infohead.text.strip() == "Material":
                                    material = infodata.text.strip()
                                    # print("Material =", material)
                            if countryo == '':
                                if infohead.text.strip() == "Country of Origin":
                                    countryo = infodata.text.strip()
                                    # print("Country of Origin =", countryo)

        # Product Specification
        # if size == '':
        tagcount = 0
        se = soup.find("div", attrs={"id": "technicalSpecifications_feature_div"})
        if se != None:
            se = se.find("table", attrs={"id": "technicalSpecifications_section_1"})
            if se != None:
                title = se.findAll('th', class_="a-span5 a-size-base")
                if title != None:
                    value = se.findAll('td', class_='a-span7 a-size-base')
                    if value != None:
                        for headeritem in se.findAll('th', class_="a-span5 a-size-base"):

                            infohead = title[tagcount]
                            infodata = value[tagcount]
                            tagcount = tagcount + 1
                            # print(infohead.text)
                            if brand == '':
                                if infohead.text.strip() == "Brand, Seller, or Collection Name":
                                    brand = infodata.text.strip()
                                    # print("Brand =", brand)
                            if metalstamp == '':
                                if infohead.text.strip() == "Metal stamp":
                                    metalstamp = infodata.text.strip()
                                    # print("Metal stamp =", metalstamp)
                            if metal == '':
                                if infohead.text.strip() == "Metal":
                                    metal = infodata.text.strip()
                                    # print("Metal =", metal)
                            if material == '':
                                if infohead.text.strip() == "Material":
                                    material = infodata.text.strip()
                                    # print("Material =", material)
                            if gemtype == '':
                                if infohead.text.strip() == "Gem Type":
                                    gemtype = infodata.text.strip()
                                    # print("Gem Type =", gemtype)
                            if totalgemweight == '':
                                if infohead.text.strip() == "Minimum total gem weight":
                                    totalgemweight = infodata.text.strip()
                                    # print("Minimum total gem weight =", totalgemweight)
                            if size == '':
                                if infohead.text.strip() == "Ring size" or infohead.text.strip() == "size":
                                    size = infodata.text.strip()
                                    # print("Size =", size)
                            if setting == '':
                                if infohead.text.strip() == "Setting":
                                    setting = infodata.text.strip()
                                    #print("Setting =", setting)
                            if width == '':
                                if infohead.text.strip() == "Width":
                                    width = infodata.text.strip()
                                   
                            if numberofstones == '':
                                if infohead.text.strip() == "Number of stones":
                                    numberofstones = infodata.text.strip()
                               
                            if stoneweight == '':
                                if infohead.text.strip() == "Stone Weight":
                                    stoneweight = infodata.text.strip()
                                   

        # specification for items
        tagcount = 0
        bdd = soup.find("div", class_="a-section a-spacing-large pzr-features-containers")
        if bdd != None:
            bd = bdd.find("table", attrs={"id": "product-specification-table"})
            if bd != None:
                title = bd.findAll('th', class_="a-span4 a-text-right")
                if title != None:
                    value = bd.findAll('td')
                    if value != None:
                        for headeritem in bd.findAll('th', class_="a-span4 a-text-right"):

                            infohead = title[tagcount]
                            infodata = value[tagcount]
                            tagcount = tagcount + 1
                            # print(infohead.text)
                            if brand == '':
                                if infohead.text.strip() == "Brand" or infohead.text.strip() == "Brand Name":
                                    brand = infodata.text.strip()
                                    # print("Brand1 =", brand)
                            if pageinfo == '':
                                if infohead.text.strip() == "Package Information" or infohead.text.strip() == "Package Dimensions":
                                    paginfo = infodata.text.strip()
                                    # print("Package Information =", paginfo)
                            if color == '':
                                if infohead.text.strip() == "Color" or infohead.text.strip() == "Ink Color":
                                    color = infodata.text.strip()
                                    # print("Color =",color)
                            if itvolume == '':
                                if infohead.text.strip() == "Item Volume":
                                    itvolume = infodata.text.strip()
                                    # print("Item Volume =", itvolume )
                            if material == '':
                                if infohead.text.strip() == "Material":
                                    material = infodata.text.strip()
                                    # print("Material =", material )
                            if size == '':
                                if infohead.text.strip() == "Size":
                                    size = infodata.text.strip()
                                    # print("Size =", size )
                            if unitcount == '':
                                if infohead.text.strip() == "Unit Count":
                                    unitcount = infodata.text.strip()
                                    # print("Unit Count =", unitcount)
                            if biketype == '':
                                if infohead.text.strip() == "Bike Type":
                                    biketype = infodata.text.strip()
                                    # print("Bike Type1 =", biketype)
                            if agerange == '':
                                if infohead.text.strip() == "Age Range (Description)":
                                    agerange = infodata.text.strip()
                                    # print("Age Range =", agerange )
                            if wheelsize == '':
                                if infohead.text.strip() == "Wheel Size":
                                    wheelsize = infodata.text.strip()
                                    # print("Wheel Size =", wheelsize)
                            if shape == '':
                                if infohead.text.strip() == "Shape":
                                    shape = infodata.text.strip()
                                    # print("Shape =", shape)
                            if pattern == '':
                                if infohead.text.strip() == "Pattern":
                                    pattern = infodata.text.strip()
                                    # print("Pattern =", pattern)
                            if capacity == '':
                                if infohead.text.strip() == "Capacity":
                                    capacity = infodata.text.strip()
                                    # print("Capacity =", capacity)
                            if fillmat == '':
                                if infohead.text.strip() == "Fill Material":
                                    fillmat = infodata.text.strip()
                                    # print("Fill Material =", fillmat)
                            if pillowtype == '':
                                if infohead.text.strip() == "Pillow Type":
                                    pillowtype = infodata.text.strip()
                                    # print("Pillow Type =", pillowtype)
                            if finishtype == '':
                                if infohead.text.strip() == "Finish Type":
                                    finishtype = infodata.text.strip()
                                    # print("Finish Type =", finishtype)
                            if itemw == '':
                                if infohead.text.strip() == "Item Weight":
                                    itemw = infodata.text.strip()
                                    # print("Item Weight =", itemw)
                            if formfact == '':
                                if infohead.text.strip() == "Form Factor":
                                    formfact = infodata.text.strip()
                                    # print("Form Factor =", formfact)
                            if inoutusage == '':
                                if infohead.text.strip() == "Indoor/Outdoor Usage":
                                    inoutusage = infodata.text.strip()
                                    # print("Indoor/Outdoor Usage =", inoutusage)
                            if powersource == '':
                                if infohead.text.strip() == "Power Source":
                                    powersource = infodata.text.strip()
                                    # print("Power Source =", powersource)
                            if heatingmethod == '':
                                if infohead.text.strip() == "Heating Method":
                                    heatingmethod = infodata.text.strip()
                                    # print("Heating Method =", heatingmethod)
                            if recomuseforpro == '':
                                if infohead.text.strip() == "Recommended Uses For Product":
                                    recomuseforpro = infodata.text.strip()
                                    # print("Recommended Uses For Product =", recomuseforpro)
                            if modelnumber == '':
                                if infohead.text.strip() == "Item model number":
                                    modelnumber = infodata.text.strip()
                                    # print("Item model number =", modelnumber)
                            #Auto & Tires
                            if loadrange == '':
                                if infodata.text.strip() == "Ply Rating":
                                    loadrange = infodata.text.strip()

        #title below format
        tifor = soup.find_all("div", class_="a-section a-spacing-micro bylineHidden feature")
        if tifor != None:
            for i in tifor:
                p = i.find_all("span", class_="a-color-secondary")
                p1 = i.find_all("span")
                if p != None or p1 != None:
                  for j in p:
                    p = j.text.replace('\u200f\n', '')
                    p = p.replace('\u200e\n', '')
                    p = p.replace('\n', '')
                    p = p.replace(':', '')
                    p = p.strip()
                  for k in p1:
                    p1 = k.text.strip()
                  if p == "Format":
                    tiformat = p1
                    if tiformat == 'Dvd' or tiformat == 'Multi-Format' or tiformat == 'VHS Tape' or tiformat == 'HD DVD' or tiformat == 'DVD' or tiformat == 'CD' or tiformat == 'Blu-Ray' or tiformat == 'Blu-ray' or tiformat == '4K Ultra HD' or tiformat == '4K Ultra HD':
                        titleformats = tiformat

        # Buybox price
        try:
            my_list = []
            d = soup.find_all("div", class_="a-box-group a-accordion a-spacing-large")
            for item in d:
                x = item.find_all("span", class_="a-price a-text-normal aok-align-center reinventPriceAccordionT2")
                for it in x:
                    y = it.find_all("span", class_="a-offscreen")
                    for t in y:
                        bbprice = t.text.strip()

                        my_list.append(bbprice)
                        # print("Buybox price = ", my_list)

            if len(d) == 0:
                d = soup.find_all("div", class_="a-box-group")
                for item in d:
                    x = item.find_all("span", class_="a-price aok-align-center")
                    z = item.find_all("span", class_="a-size-medium a-color-price header-price a-text-normal")
                    w = item.find_all("span", class_="a-price a-text-price a-size-medium")
                    for it in x:
                        y = it.find_all("span", class_="a-offscreen")
                        for t in y:
                            bbprice = t.text.strip()
                            # print("Buybox price = ", bbprice)
                            my_list.append(bbprice)
                    if len(z) != 0:
                        for it1 in z:
                            bbprice1 = it1.text.strip()
                            # print("BuyBox Price = ",bbprice1)
                            my_list.append(bbprice1)
                    if len(w) != 0:
                        for it in w:
                            y = it.find_all("span", class_="a-offscreen")
                            for t in y:
                                bbprice2 = t.text.strip()
                                # print("BuyBox price =",bbprice2)
                                my_list.append(bbprice2)

            if len(x) == 0:
                for item in d:
                    x = item.find_all("span", class_="a-price a-text-price header-price a-size-base a-text-normal")
                    z = item.find_all("span", class_="a-color-price header-price a-text-normal")
                    w = item.find_all("span", class_="a-color-secondary header-price a-text-normal")
                    for it in x:
                        y = it.find_all("span", class_="a-offscreen")
                        for t in y:
                            bbprice = t.text.strip()
                            # print("Buybox price = ", bbprice)
                            my_list.append(bbprice)
                    if len(z) != 0:
                        for it1 in z:
                            a = it1.find_all("span", {"id": "sns-base-price"})
                            for t1 in a:
                                bbprice1 = t1.text.strip()
                                # print("Buybox Price =", bbprice1)
                                my_list.append(bbprice1)
                    if len(w) != 0:
                        for it1 in w:
                            a = it1.find_all("span", {"id": "sns-base-price"})
                            for t1 in a:
                                bbprice2 = t1.text.strip()
                                # print("Buybox Price =", bbprice2)
                                my_list.append(bbprice2)

        except AttributeError:
            pass

        # Buybox selected & selected price
        try:

            bb = soup.find("div", attrs={"aria-checked": 'true'})
            if bb is None:
                bb = soup.find("div", attrs={"id": "booksHeaderSection"})
                if bb is None:
                    bb = soup.find("div", attrs={"id": "apex_offerDisplay_desktop"})
                    bp = 'NA'
                    sp = 'NA'
                    # print("Buybox Selected =", bp)
                    # print("Selected Price =", sp)
                    bpp = bb.find("span", class_="a-price aok-align-center")
                    sp = bpp.find("span", class_="a-offscreen").text.strip()
                    # print("Selected Price =", sp)

                b = bb.find("div", class_="a-column a-span4 a-text-left")
                bp = b.find("span", attrs={"id": 'newBuyingOption'}).text.strip()
                # print("Buybox Selected =", bp)
                sp = bb.find("span", class_="a-size-medium a-color-price header-price a-text-normal").text.strip()
                # print("Selected Price =", sp)

            b = bb.find("div", class_="a-column a-span6 accordion-caption")
            if b is None:
                b = bb.find("div", class_="a-section a-spacing-none a-padding-none accordion-caption")
                if b is None:
                    b = bb.find("div", class_="a-column a-span12 accordion-caption")

            bp = b.find("span", class_="a-text-bold").text.strip()
            # print("Buybox Selected =", bp)

            # selected price
            bpp = bb.find("span", class_="a-price a-text-normal aok-align-center reinventPriceAccordionT2")
            if bpp is None:
                bpp = bb.find("span", class_="a-color-price header-price a-text-normal")
                if bpp is None:
                    bpp = bb.find("span", class_="a-price a-text-price header-price a-size-base a-text-normal")

            sp = bpp.find("span", class_="a-offscreen")
            if sp is None:
                sp = bpp.find("span", attrs={"id": 'sns-base-price'})

            sp = sp.text.strip()
            # print("Selected Price =", sp)

        except AttributeError:
            pass

        # Swatch Details
        try:
            swatch = []
            info = soup.find("div", attrs={"id": 'tmmSwatches'})
            info1 = info.find("ul", class_="a-unordered-list a-nostyle a-button-list a-horizontal")
            if info is None:
                inf1 = soup.find("ul",
                                 class_="a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches")
                inf1 = inf1.find_all("span", class_="a-button-inner")
                for inf in inf1:
                    info_select = inf.text.strip()
                    # print("Swatch Details =", info_select)
                    swatch.append(info_select)
            else:

                inf1 = info1.find("li", class_="swatchElement selected resizedSwatchElement")
                if inf1 is None:
                    inf1 = info1.find("li", class_="swatchElement selected")
                    info_select = inf1.find("span", class_="a-button-inner").text.strip()
                    # print("Swatch Details =", info_select)
                    swatch.append(info_select)
                    if inf1 is None:
                        info_select = 'NA'
                        # print("Swatch Details =", info_select)
                        swatch.append(info_select)
                else:
                    info_select = inf1.find("span", class_="a-button-inner").text.strip()
                    # print("Swatch Details =", info_select)
                    swatch.append(info_select)

            inf = info1.find_all("li", class_="swatchElement unselected resizedSwatchElement")
            if len(inf) == 0:
                inf = info1.find_all("li", class_="swatchElement unselected")

                for inff in inf:
                    y = inff.find("span", class_="a-button-inner")
                    for t in y:
                        info_select = t.text.strip()
                        # print("Swatch Details =", info_select)
                        swatch.append(info_select)
                if inf is None:
                    info_select = 'NA'
                    # print("Swatch Details =", info_select)
                    swatch.append(info_select)
            else:
                for inff in inf:
                    y = inff.find("span", class_="a-button-inner")
                    for t in y:
                        info_select = t.text.strip()
                        # print("Swatch Details =", info_select)
                        swatch.append(info_select)


        except AttributeError:
            pass

        # Swatch Details Highlighted
        try:
            highlited = soup.find("div", attrs={"id": 'tmmSwatches'})
            highlited1 = highlited.find("ul", class_="a-unordered-list a-nostyle a-button-list a-horizontal")

            if highlited is None:
                highlited = soup.find("ul",class_="a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches")

                high = highlited.find("li", class_="swatchSelect")
                highformat = high.find_all("a", class_="a-button-text")
                highformat = highformat[0].find("span").text
                highprice = high.find("span", class_="a-color-base").text.strip()
                """print("format=", highformat)
                print("price=", highprice)"""

            else:

                hig = highlited1.find("li", class_="swatchElement selected resizedSwatchElement")

                if hig is None:
                    highlited = highlited1.find("li", class_="swatchElement selected")
                    highformat = highlited.find_all("a", class_="a-button-text")
                    highformat = highformat[0].find("span").text
                    highprice = highlited.find("span", class_="a-color-base").text.strip()
                    """print("format=", highformat)
                    print("price=", highprice)"""
                else:
                    highformat = hig.find_all("a", class_="a-button-text")
                    highformat = highformat[0].find("span").text
                    highprice = hig.find("span", class_="a-color-base").text.strip()
                    """print("format1=", highformat)
                    print("price1=", highprice)"""

        except AttributeError:
            pass
        
        #Swatch Details unselected
        try:
            unhighlited = soup.find("li", class_="swatchElement unselected")
            unhighlited = unhighlited.find_all("a", class_="a-button-text")
            unhighlitedformat = unhighlited[0].find("span").text
        except:
            pass

        # About this item
        try:
            aboutitem = []
            abb = soup.find("div", attrs={"id": "feature-bullets"})
            if abb != None:
                about = abb.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
                about = about.find_all("span", class_="a-list-item")
                for ab in about:
                    aboutt = ab.text.strip()
                    # print("About this Item =", aboutt)
                    aboutitem.append(aboutt)

                about1 = abb.find("div", class_="a-row a-expander-container a-expander-inline-container")
                about1 = about1.find("ul", class_="a-unordered-list a-vertical a-spacing-none")
                about1 = about1.find_all("span", class_="a-list-item")
                for ab in about1:
                    aboutt1 = ab.text.strip()
                    # print("About this Item =", aboutt1)
                    aboutitem.append(aboutt1)
            else:
                abb = soup.find_all("ul", class_="a-unordered-list a-vertical a-spacing-small")
                if abb != None:
                    for ab in abb:
                        aboutt = ab.text.strip()
                        aboutitem.append(aboutt)

        except AttributeError:
            pass

        # Product Overview
        try:
            productoverview = []
            product = soup.find("div", attrs={"id": "productOverview_feature_div"}).text.strip()
            productoverview = [product]
            # print("Product Overview =", productoverview)

        except AttributeError:
            pass

        # Product Details
        try:
            productdetails = soup.find("div", attrs={"id": "detailBulletsWrapper_feature_div"})
            productdetails = productdetails.find("div", attrs={"id": "detailBullets_feature_div"})
            productdetails = productdetails.find("ul",
                                                 class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").text.strip()
            # print("Product Details =", productdetails)
            productdetails = ''.join(c for c in productdetails if ord(c) < 128)

        except AttributeError:
            pass

        # Product Information
        try:
            productinfo = soup.find("div", class_="a-row a-spacing-top-base")
            # print(productinfo)
            if productinfo is None:
                productinfo = 'NA'
                # print("Product Information =", productinfo)
            else:
                productinfo = productinfo.text.strip()
                # print("Product Information =", productinfo)
                productinfo = ''.join(c for c in productinfo if ord(c) < 128)

        except AttributeError:
            pass

        # ImageURL
        try:
            imageurl = []
            imgurl = soup.find("div", attrs={"id": "altImages"})
            imgurl = imgurl.find_all("li", class_="a-spacing-small item imageThumbnail a-declarative")
            for i in imgurl:
                i = i.find_all('img', attrs={'src': re.compile("^https:/")})
                for li in i:
                    lin = li.get('src')
                    imageurl.append(lin)

        except AttributeError:
            pass
        
        #Customer Review
        try:
            review = soup.find("div", attrs={"id":"averageCustomerReviews"})
            review = review.find("span", class_="a-icon-alt").text.replace(" out of 5 stars","")
            
        except AttributeError:
            pass
        
        #Sold And Shipped
        try:
            p = soup.find("div", attrs={"tabular-attribute-name":"Ships from"}).text.strip()
            p1 = soup.find_all("div", attrs={"tabular-attribute-name":"Ships from"})
             
            for j in p1:
                if p == "Ships from":
                 if j.text.strip() != "Ships from":
                    ship = j.text.strip()

            p2 = soup.find("div", attrs={"tabular-attribute-name":"Sold by"}).text.strip()
            p3 = soup.find_all("div", attrs={"tabular-attribute-name":"Sold by"})
             
            for j in p3:
                if p2 == "Sold by":
                 if j.text.strip() != "Sold by":
                    sold = j.text.strip()
        except AttributeError:
            pass


        breadcrumbsplit = breadcrumb.replace("›", "/").replace("\n", "").replace("                         ",                                                                                 "").strip()
        breadcrumbsplit = list(breadcrumbsplit.split("/"))
        if breadcrumbsplit[0] == "Books":
            titleISBN13,titleISBN10,prodetailISBN13,prodetailISBN10,titleformat = book(soup)
        elif breadcrumbsplit[0] == "Movies & TV":
            titleformat = movies(soup)
        elif 'Automotive' in breadcrumbsplit and ('Tires & Accessories' in breadcrumbsplit or 'Tires' in breadcrumbsplit):
            if size != None:
                size = re.sub('\D', '', size)
            titletiresize,aboutloadrange,swatchtiresize,swatchloadindexrating,swatchspeedrating,swatchhightiresize,titleloadrange = autotires(soup,size)
        elif breadcrumbsplit[0] == "Video Games" and 'Accessories' not in breadcrumb:
            platform,swatchplatform,titleplatform,prodetplatformlist = videogames(soup)
        elif breadcrumbsplit[0] == "Clothing" or 'Clothing' in breadcrumbsplit[0]:
            titlecolorlist, titleclothingsizelist, prodetailclothingsize, prodetailcolor = clothing(soup)
        else:
            titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, titleformat = extraction(soup)

        titleISBN13 = titleISBN13
        titleISBN10 = titleISBN10
        prodetailISBN13 = prodetailISBN13
        prodetailISBN10 = prodetailISBN10
        titleformat = titleformat

        titletiresize = titletiresize
        aboutloadrange = aboutloadrange
        swatchtiresize = swatchtiresize
        swatchloadindexrating = swatchloadindexrating
        swatchspeedrating = swatchspeedrating
        swatchhightiresize = swatchhightiresize
        titleloadrange = titleloadrange
        
        titlecolorlist = titlecolorlist
        titleclothingsizelist = titleclothingsizelist
        prodetailclothingsize = prodetailclothingsize
        prodetailcolor = prodetailcolor

        platform = platform
        swatchplatform = swatchplatform
        titleplatform = titleplatform
        prodetplatformlist = prodetplatformlist

        mediaformatlist = mediaformat.split(",")
        
        for i in mediaformatlist:
                i = i.replace("Multiple Formats","Multi-Format").strip()
                if  i == iformat and i == titleformat:
                    mediaformat = i
                if  i == iformat and i == titleformats:
                    mediaformat = i
                if  i == iformat and i == highformat:
                    mediaformat = i
                if i == titleformat and i == titleformats:
                    mediaformat = i
                if i == titleformat and i == highformat:
                    mediaformat = i
                if i == titleformats and i == highformat:
                    mediaformat = i
                elif titleformat != '' or iformat != '' or titleformats != '' or highformat != '':
                    if i == titleformat:
                        mediaformat = i
                    elif i == iformat:
                        mediaformat = i
                    elif i == titleformats:
                        mediaformat = i
                    elif i == highformat:
                        mediaformat = i

        if mediaformat == 'Dvd' or mediaformat == 'VHS Tape' or mediaformat == "Multiple-Format" or mediaformat == "HD DVD" or mediaformat == 'DVD' or mediaformat == 'CD' or mediaformat == 'Blu-Ray' or mediaformat == 'Blu-ray' or mediaformat == '4K Ultra HD' or mediaformat == '4K Ultra HD':
                mediaformat = mediaformat
        else:
            mediaformat = ""

        if ',' in platform:
            platform = platform.split(",") 
            for i in platform:
                i = i.lower().replace("vista","").strip()
                if titleplatform != '':
                    if i.strip() == titleplatform:
                        platform = i
                    elif titleplatform == 'pc' and 'windows' in i.strip():
                        platform = 'pc'
                else:
                    platform = platform
                    
        if titleplatform != '' and platform != '' and (titleplatform == 'ps4' or titleplatform == 'playstation 4' or titleplatform == 'ps5' or titleplatform == 'playstation 5'):
                if platform.lower().strip() == 'playstation 4' and titleplatform == 'ps4':
                    platform = 'ps4'
                elif platform.lower().strip() =='ps4' and titleplatform == 'playstation 4':
                    platform = 'playstation 4'
                elif platform.lower().strip() == 'playstation 5' and titleplatform == 'ps5':
                    platform = 'ps5'
                elif platform.lower().strip() =='ps5' and titleplatform == 'playstation 5':
                    platform = 'playstation 5'
    
        
        if platform != '' or titleplatform != '' or swatchplatform:
                for i in prodetplatformlist:
                    if  i == platform.lower() and i == titleplatform.lower():
                        prodetplatform = i
                    elif  i == platform.lower() and i == swatchplatform.lower():
                        prodetplatform = i
                    elif  i == titleplatform.lower() and i == swatchplatform.lower():
                        prodetplatform = i
                    elif i == platform.lower():
                        prodetplatform = i
                    elif i == titleplatform.lower():
                        prodetplatform = i
                    elif i == swatchplatform.lower():
                        prodetplatform = i
        else:
            for i in prodetplatformlist:
                prodetplatform = i
        
        # Match Type
        if breadcrumbsplit[0] == "Books":
            matchtype,matchtypecomments = bookmatchtype(isbn,isbn1,titleISBN13,titleISBN10,prodetailISBN13,prodetailISBN10,titleformat,highformat,iformat,pagecount)
        elif breadcrumbsplit[0] == "Movies & TV" or breadcrumbsplit[0] == "Musical Instruments":
             matchtype,matchtypecomments = moviesandmusicmatchtype(director,actors,iformat,titleformat,titleformats,highformat,mediaformat,unhighlitedformat)
        elif 'Automotive' in breadcrumbsplit and ('Tires & Accessories' in breadcrumbsplit or 'Tires' in breadcrumbsplit):
             matchtype,matchtypecomments = autotiresmatchtype(model,partno,size,titletiresize,swatchtiresize,swatchhightiresize,loadrange,titleloadrange,aboutloadrange,speedrating,swatchspeedrating)
        elif breadcrumbsplit[0] == "Video Games" and 'Accessories' not in breadcrumb:
             matchtype,matchtypecomments = videogamesmatchtype(platform,titleplatform,prodetplatform,swatchplatform,hardwareplatform)
        elif breadcrumbsplit[0] == "Clothing" or 'Clothing' in breadcrumbsplit[0]:
            matchtype,matchtypecomments = clothingmatchtype(titleclothingsizelist, titlecolorlist,swatchcolor,swatchsize,prodetailclothingsize, prodetailcolor, color, size)
        
        
        matchtype = matchtype
        matchtypecomments = matchtypecomments

    try:
        pyautogui.press('alt')
    except:
        pass

    # Filename preparation
    itemid = ''
    lines = lines[3].replace('\n', "")
    itemid = "".join(lines.split('/', 4)[4])
    itemid = itemid.replace('?th=1&psc=1', '') + '.html'
    n = os.path.join(outpath, itemid)
    f = codecs.open(n, "w", "utf-8")
    h = driver.page_source
    f.write(h)

    screenshot_path = outpath + '\\' + itemid
    itemid = itemid.replace('.html', '')
    my_list = str(my_list)
    swatch = str(swatch)
    imageurl = str(imageurl)
    aboutitem = str(aboutitem)
    productoverview = str(productoverview)
    
    return pgproblem, matchtype, matchtypecomments, itemid, breadcrumb, brandtitle,titlecard, listprice, my_list, bp, sp, titleformat, brand, gender, color, iformat, manuf, partno, model, pack, shape, titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, dimen, size, asin, itemw, biketype, agerange,wheelsize, pattern, material, unitcount, publisher, language, pagecount, isbn, isbn1, numberofitems, batteries, fdate, countryo,covermat, style, fillmat, pillowtype, specialfeature, procar, season, fabrictype, itemthickness,finishtype, formfact, inoutusage, powersource, heatingmethod, recomuseforpro, modelnumber, disman,itvolume, metalstamp, metal, gemtype, totalgemweight, swatch, highformat, highprice, aboutitem,productoverview, productdetails, productinfo, imageurl, screenshot_path, setting , width , numberofstones , stoneweight , mpaarating , director , duration , releasedate , actors , studio , numberofdisc , genre , contributor , audiodesc , dubbed , subtitles , producers , aspectratio , mediaformat , bodymaterial , materialtype , instrumentkey , label ,titleformats, rimsize,secwidth,tireaspectratio,loadindexrating,speedrating,loadcapacity,treaddepth,treadtype,rimwidth,tirediameter,oempartno,construction,loadrange,titletiresize,swatchtiresize,swatchhightiresize,titleloadrange,aboutloadrange,swatchspeedrating,swatchloadindexrating, review, ship, sold, hardwareinterface,compatibledevices,totalusbport,noofports,totalhdmiports,connectortype,cabletype,modelname,hardwareplatform,ops,pricing,typeofitem,titleplatform,platform,swatchplatform,prodetplatform

    os.system('cls')

relen = reccount()


if relen != 0:
    connection,cursor = urlquery()
    for url_lines in cursor.fetchall():
        pgproblem, matchtype, matchtypecomments, itemid, breadcrumb, brandtitle,titlecard, listprice, my_list, bp, sp, titleformat, brand, gender, color, iformat, manuf, partno, model, pack, shape, titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, dimen, size, asin, itemw, biketype, agerange,wheelsize, pattern, material, unitcount, publisher, language, pagecount, isbn, isbn1, numberofitems, batteries, fdate, countryo,covermat, style, fillmat, pillowtype, specialfeature, procar, season, fabrictype, itemthickness,finishtype, formfact, inoutusage, powersource, heatingmethod, recomuseforpro, modelnumber, disman,itvolume, metalstamp, metal, gemtype, totalgemweight, swatch, highformat, highprice, aboutitem,productoverview, productdetails, productinfo, imageurl, screenshot_path,setting , width , numberofstones , stoneweight , mpaarating , director , duration , releasedate , actors , studio , numberofdisc , genre , contributor , audiodesc , dubbed , subtitles , producers , aspectratio , mediaformat , bodymaterial , materialtype , instrumentkey , label ,titleformats, rimsize,secwidth,tireaspectratio,loadindexrating,speedrating,loadcapacity,treaddepth,treadtype,rimwidth,tirediameter,oempartno,construction,loadrange,titletiresize,swatchtiresize,swatchhightiresize,titleloadrange,aboutloadrange,swatchspeedrating,swatchloadindexrating, review, ship, sold, hardwareinterface,compatibledevices,totalusbport,noofports,totalhdmiports,connectortype,cabletype,modelname,hardwareplatform,ops,pricing,typeofitem,titleplatform,platform,swatchplatform,prodetplatform = AttributeExtraction(url_lines)

        azid = url_lines[1]
        tooldate = datetime.now().strftime("%Y-%m-%d")
        tooltime = datetime.now().strftime("%H:%M:%S")
        url = url_lines[3]
        batch_id = url_lines[2]

        pgproblem = pgproblem
        itemid = itemid
        breadcrumb = breadcrumb
        brandtitle = brandtitle
        titlecard = titlecard
        listprice = listprice
        my_list = my_list
        bp = bp
        sp = sp
        brand = brand
        gender = gender
        color = color
        iformat = iformat
        manuf = manuf
        partno = partno
        model = model
        pack = pack
        shape = shape
        dimen = dimen
        size = size
        asin = asin
        itemw = itemw
        biketype = biketype
        agerange = agerange
        wheelsize = wheelsize
        pattern = pattern
        material = material
        unitcount = unitcount
        publisher = publisher
        language = language
        pagecount = pagecount
        isbn = isbn
        isbn1 = isbn1
        numberofitems = numberofitems
        batteries = batteries
        fdate = fdate
        countryo = countryo
        covermat = covermat
        style = style
        fillmat = fillmat
        pillowtype = pillowtype
        specialfeature = specialfeature
        procar = procar
        season = season
        fabrictype = fabrictype
        itemthickness = itemthickness
        finishtype = finishtype
        formfact = formfact
        inoutusage = inoutusage
        powersource = powersource
        heatingmethod = heatingmethod
        recomuseforpro = recomuseforpro
        modelnumber = modelnumber
        disman = disman
        itvolume = itvolume
        metalstamp = metalstamp
        metal = metal
        gemtype = gemtype
        totalgemweight = totalgemweight
        swatch = swatch
        highformat = highformat
        highprice = highprice
        aboutitem = aboutitem
        productoverview = productoverview
        productdetails = productdetails
        productinfo = productinfo
        imageurl = imageurl
        titleISBN13 = titleISBN13
        titleISBN10 = titleISBN10
        prodetailISBN13 = prodetailISBN13
        prodetailISBN10 = prodetailISBN10
        titleformat = titleformat
        matchtype = matchtype
        matchtypecomments = matchtypecomments
        setting = setting
        width = width
        numberofstones = numberofstones 
        stoneweight = stoneweight
        mpaarating = mpaarating
        director = director
        duration = duration
        releasedate = releasedate
        actors = actors
        studio = studio
        numberofdisc = numberofdisc
        genre = genre
        contributor = contributor
        audiodesc = audiodesc
        dubbed = dubbed
        subtitles = subtitles
        producers = producers
        aspectratio = aspectratio
        mediaformat = mediaformat
        bodymaterial = bodymaterial
        materialtype = materialtype 
        instrumentkey  = instrumentkey
        label = label
        titleformats = titleformats
        rimsize = rimsize
        secwidth = secwidth
        tireaspectratio = tireaspectratio
        loadindexrating = loadindexrating
        speedrating = speedrating
        loadcapacity = loadcapacity
        treaddepth = treaddepth
        treadtype = treadtype
        rimwidth = rimwidth
        tirediameter = tirediameter
        oempartno = oempartno
        construction = construction
        loadrange = loadrange
        titletiresize = titletiresize
        swatchtiresize = swatchtiresize
        swatchhightiresize = swatchhightiresize
        titleloadrange = titleloadrange
        aboutloadrange = aboutloadrange
        swatchspeedrating = swatchspeedrating
        swatchloadindexrating = swatchloadindexrating
        review = review
        ship = ship
        sold = sold
        hardwareinterface = hardwareinterface
        compatibledevices = compatibledevices
        totalusbport = totalusbport
        noofports = noofports
        totalhdmiports = totalhdmiports
        connectortype = connectortype
        cabletype = cabletype
        modelname = modelname
        hardwareplatform = hardwareplatform
        ops = ops
        pricing = pricing
        typeofitem = typeofitem
        titleplatform = titleplatform
        platform = platform
        swatchplatform = swatchplatform
        prodetplatform = prodetplatform
        
        cursor.execute('INSERT INTO "ECHO_AE_AZ_Out" ("AZ_Record_ID","Tool_Date","Tool_Time","Batch_ID","AZ_URL","URL_Status","Match_Type","Match_Type_Comments","Item_ID","Breadcrumb","Brand_Title","Title","List_Price","Buybox_Price","BuyBox_Selected","Selected_Price","Title_Format","Brand","Gender","Color","Format","Manufacturer","Manufacturer_Part_Number","Model","Count_Per_Pack","Shape","Title_ISBN13","Title_ISBN10","Prodetail_ISBN13","Prodetail_ISBN10","Product_Dimensions","Size","Asin","Item_Weight","Bike_Type","Age_Range","Wheel_Size","Pattern","Material","Unit_Count","Publisher","Language","Pagecount","ISBN_10","ISBN_13","Number_of_Items","Batteries","Date_First_Available","Country_of_Origin","Cover_Material","Style","Fill_Material","Pillow_Type","Special_Feature","Product_Care_Instructions","Seasons","Fabric_Type","Item_Thickness","Finish_Type","Form_Factor","Indoor_Outdoor_Usage","Power_Source","Heating_Method","Recommended_Uses_For_Product","Item_model_number","Is_Discontinued_By_Manufacturer","Item_Volume","Metal_stamp","Metal","Gem_Type","Minimum_total_gem_weight","Swatch_Details","Swatch_Format","Swatch_Price","About_this_Item","Product_Overview","Product_Details","Product_Information","Image_URL","Screenshot_Path","Setting","Width","Number_of_Stones","Stone_Weight","MPAA_Rating","Director","Run_Time","Release_Date","Actors","Studio","Number_of_Discs","Genre","Contributor","Audio_Description","Dubbed","Subtitles","Producers","Aspect_Ratio","Media_Format","Body_Material","Material_Type","Instrument_Key","Label","Title_Formats","Rim_Size","Section_Width","Tire_Aspect_Ratio","Load_Index_Rating","Speed_Rating","Load_Capacity","Tread_Depth","Tread_Type","Rim_Width","Tire_Diameter","OEM_Part_Number","Construction","Ply_Rating","Title_Tire_Size","Swatch_Tire_Size","Swatch_High_Tire_Size","Title_Load_Range","About_Load_Range","Swatch_Speed_Rating","Swatch_Load_Index_Rating","Review","Ship","Sold","Hardware_Interface","Compatible_Devices","Total_USB_Ports","Number_of_Ports","Total_HDMI_Ports","Connector_Type","Cable_Type","Model_Name","Hardware_Platform","Operating_System","Pricing","Type_of_item","Title_Platform","Platform","Swatch_Platform","Prodet_Platform") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                    (azid,tooldate, tooltime, batch_id, url, pgproblem, matchtype, matchtypecomments, itemid, breadcrumb, brandtitle,
                     titlecard, listprice,my_list, bp, sp, titleformat, brand, gender, color, iformat, manuf, partno, model, pack, shape,titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, dimen, size, asin, itemw, biketype, agerange,
                     wheelsize, pattern, material,unitcount, publisher, language, pagecount, isbn, isbn1, numberofitems, batteries, fdate, countryo,
                              covermat, style, fillmat, pillowtype, specialfeature, procar, season, fabrictype, itemthickness,
                              finishtype,formfact, inoutusage, powersource, heatingmethod, recomuseforpro, modelnumber, disman,
                              itvolume, metalstamp, metal, gemtype, totalgemweight, swatch, highformat, highprice, aboutitem,
                              productoverview, productdetails, productinfo, imageurl, screenshot_path,
                            setting , width , numberofstones , stoneweight , mpaarating , director , duration , releasedate , actors , studio , 
                            numberofdisc , genre , contributor , audiodesc , dubbed , subtitles , producers , aspectratio , 
                            mediaformat , bodymaterial , materialtype , instrumentkey , label, titleformats,rimsize,secwidth,
                            tireaspectratio,loadindexrating,speedrating,loadcapacity,treaddepth,treadtype,rimwidth,tirediameter,
                            oempartno,construction,loadrange,titletiresize,swatchtiresize,swatchhightiresize,
                            titleloadrange,aboutloadrange,swatchspeedrating,swatchloadindexrating,review,ship,sold,
                            hardwareinterface,compatibledevices,totalusbport,noofports,totalhdmiports,connectortype,cabletype,
                            modelname,hardwareplatform,ops,pricing,typeofitem,titleplatform,platform,swatchplatform,
                            prodetplatform ))
        cursor.commit()
        itemid = "'"+itemid+"'"
        cursor.execute('SELECT "Batch_ID","Item_ID" FROM "ECHO_AE_AZ_Out" WHERE ("Batch_ID" = {} and "Item_ID" = {})'.format(Batch,itemid))
        fetrecord = len(cursor.fetchall())
        if fetrecord != 0:
            cursor.execute('UPDATE "ECHO_AE_AZ_In" SET "Record_Status" = (%s) WHERE "Batch_ID" = (%s) and "AZ_URL" = (%s);', ('Processed',Batch ,url_lines[2]))
            connection.commit()
        tcount = tcount + 1
        print("Completed " + str(tcount) + " URLs out of " + str(relen))
        driver.quit

else:
    print("The Given range of URLs are Processed")
connection,cursor = azcon()
cursor.execute('select count(*) from "ECHO_AE_AZ_In" WHERE ("Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" is NULL or "Record_Status" = {} ))'.format(Batch,rs1,rs2))
rows = cursor.fetchone()[0]
print("Remaining " + str(rows) + " URLs")