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
import undetected_chromedriver as uc
from random import randint
import pyodbc
from datetime import datetime
import ssl
import psycopg2

ssl._create_default_https_context = ssl._create_unverified_context
import random, socket

# SQL conncetion
username = 'postgres'
password = 'Linux@18276'

System_Name = socket.gethostname()
User_Name = os.getlogin()


# SQL conncetion
def azcon():
    connection = psycopg2.connect(host='103.19.88.66', dbname='Walmart MINT - AZ', user=username, password=password,
                                  port='5432')
    cursor = connection.cursor()
    return connection, cursor


rs1 = "'" + "Processed" + "'"
rs2 = "'" + "" + "'"
rs3 = "'" + "Initiated" + "'"
sysname = System_Name.replace("-", "_")

Batch = input('Enter the Batch ID:')


def urlquery():
    connection, cursor = azcon()
    cursor.execute(
        'SELECT * FROM "ECHO_AE_AZ_In" WHERE "Batch_ID" = {} and "System_Name" = {} and "User_Name" = {} and ("Record_Status" is NULL or "Record_Status" = {})'.format(
            Batch, "'" + sysname + "'", "'" + User_Name + "'", rs2))
    return connection, cursor


def query():
    connection, cursor = azcon()
    cursor.execute(
        'WITH AZ_input AS(SELECT ROW_NUMBER() OVER (ORDER BY "Batch_ID") ID,"AZ_Record_ID","Batch_ID","AZ_URL","Input_Date","Record_Status" FROM "ECHO_AE_AZ_In" WHERE "Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" = {}  or "Record_Status" is NULL or "Record_Status" = {}))SELECT * FROM AZ_input WHERE ID Between {} and {} and ("Record_Status" = {} or "Record_Status" is NULL or "Record_Status" = {})'.format(
            Batch, rs1, rs3, rs2, Processcount, Processcount1, rs3, rs2))
    return connection, cursor


def reccount():
    connection, cursor = urlquery()
    relen = len(cursor.fetchall())
    return relen


relen = reccount()
if relen == 0:
    Processcount = int(input("Enter the number of record"))
    Processcount1 = int(input("Enter the number of record"))
    connection, cursor = query()
    for urllines in cursor.fetchall():
        connection, cursor = azcon()
        cursor.execute(
            'UPDATE "ECHO_AE_AZ_In" SET "System_Name" = (%s),"User_Name" = (%s) WHERE "Batch_ID" = (%s) and "AZ_URL" = (%s) and "System_Name" is NULL  and "User_Name" is NULL;',
            (sysname, User_Name, Batch, urllines[3]))
        connection.commit()


# install Browsec VPN
def browsecvpn():
    driver.get(
        "https://chrome.google.com/webstore/detail/browsec-vpn-free-vpn-for/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en")
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 11)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    pyautogui.press('left')
    time.sleep(2)
    pyautogui.press('enter')

    time.sleep(20)
    pyautogui.press('esc')
    driver.get('chrome-extension://omghfjlpggmjjaagoclmmobgdodcjboh/popup/popup.html')

    vpnstatus = 'No'

    while True:
        os.system('cls')
        vpnstatus = input('Type Yes if VPN is enabled:')
        if vpnstatus == 'Yes':
            break


def disVPN():
    driver.get(
        "https://chrome.google.com/webstore/detail/browsec-vpn-free-vpn-for/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en")
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 11)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    pyautogui.press('enter')


# Change AMZ location
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
        actions.send_keys(Keys.TAB * 4)
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
driver = uc.Chrome(enable_cdp_events=True, Options=chrome_options)

# browsecvpn()
amzlocchange()
# disVPN()

tcount = 0


def AttributeExtraction(lines):
    pgproblem = ''

    driver.get(lines[2])
    try:
        ele = WebDriverWait(driver, 15).until(  # using explicit wait for 10 seconds
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))  # checking for the element with 'h2'as its CSS
        )
    except:
        print("Timeout Exception: Page did not load within 15 seconds.")

    cursor.execute('UPDATE "ECHO_AE_AZ_In" SET "Record_Status" = (%s) WHERE "Batch_ID" = (%s) and "AZ_URL" = (%s);',
                   ('Initiated', Batch, lines[2]))
    connection.commit()

    pgproblem = ''
    temp = 0
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ransleep = random.randint(15, 25)
        # time.sleep(ransleep)
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
        pgproblem = ""

    try:
        pyautogui.press('alt')
    except:
        pass

    # Filename preparation
    itemid = ''
    lines = lines[2].replace('\n', "")
    itemid = "".join(lines.split('/', 4)[4])
    itemid = itemid.replace('?th=1&psc=1', '') + '.html'
    n = os.path.join(outpath, itemid)
    f = codecs.open(n, "w", "utf-8")
    h = driver.page_source
    f.write(h)

    screenshot_path = outpath + '\\' + itemid
    itemid = itemid.replace('.html', '')

    return pgproblem, itemid, screenshot_path

    os.system('cls')


relen = reccount()
if relen != 0:
    connection, cursor = urlquery()
    for url_lines in cursor.fetchall():
        pgproblem, itemid, screenshot_path = AttributeExtraction(url_lines)

        azid = url_lines[0]
        tooldate = datetime.now().strftime("%Y-%m-%d")
        tooltime = str(datetime.now().strftime("%H:%M:%S"))
        url = url_lines[2]
        batch_id = url_lines[1]

        pgproblem = pgproblem
        itemid = itemid
        screenshot_path = screenshot_path
        connection, cursor = azcon()
        cursor.execute(
            'INSERT INTO "ECHO_AE_AZ_Out"("AZ_Record_ID","Tool_Date","Tool_Time","Batch_ID","AZ_URL","URL_Status","Item_ID","Screenshot_Path") VALUES (%s,%s,%s,%s,%s,%s,%s,%s);',
            (azid, tooldate, tooltime, batch_id, url, pgproblem, itemid, screenshot_path))
        connection.commit()
        itemid = "'" + itemid + "'"
        cursor.execute(
            'SELECT "Batch_ID","Item_ID" FROM "ECHO_AE_AZ_Out" WHERE ("Batch_ID" = {} and "Item_ID" = {})'.format(Batch,
                                                                                                                  itemid))
        fetrecord = len(cursor.fetchall())
        if fetrecord != 0:
            cursor.execute(
                'UPDATE "ECHO_AE_AZ_In" SET "Record_Status" = (%s) WHERE "Batch_ID" = (%s) and "AZ_URL" = (%s);',
                ('Processed', Batch, url_lines[2]))
            connection.commit()
        tcount = tcount + 1
        print("Completed " + str(tcount) + " URLs out of " + str(relen))
        driver.quit

else:
    print("The Given range of URLs are Processed")
connection, cursor = azcon()
cursor.execute(
    'select count(*) from "ECHO_AE_AZ_In" WHERE ("Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" is NULL or "Record_Status" = {} ))'.format(
        Batch, rs1, rs2))
rows = cursor.fetchone()[0]
print("Remaining " + str(rows) + " URLs")
