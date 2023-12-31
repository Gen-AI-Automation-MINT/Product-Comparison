from dataclasses import replace
from turtle import st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv, pyautogui, time, os, codecs, threading
from selenium.webdriver.common.by import By
import re
import urllib.parse, urllib.request
import undetected_chromedriver.v2 as uc
from random import randint
import pyodbc
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from text2digits import text2digits
t2d = text2digits.Text2Digits()
import psycopg2

#SQL conncetion
username = 'postgres'
password = 'Linux@18276'

#SQL conncetion
connection = psycopg2.connect(host = '103.19.88.66', dbname = 'postgres', user=username, password=password, port='5432')
cursor = connection.cursor()

connection1 = pyodbc.connect(Driver='{SQL Server}',Server='{192.168.1.40\Walmart_MINT,5040}',Database='{References - All}',
            Trusted_Connection='no',UID='KNXW' ,PWD='Kriy@2707')
cursor1 = connection1.cursor()

Batch = input('Enter the Batch ID:')
Processcount = int(input("Enter the number of record"))
Processcount1 = int(input("Enter the number of record"))

#Input Paths
with open("Inputpath.txt") as z:
    lines = z.read()
    outpath = lines.split('\n', 1)[0]
    z.close

tcount=0

rs1 = "'Processed'"
rs2 = "''"
rs3 = "'Initiated'"

def query():
    cursor.execute('WITH WM_input AS(SELECT ROW_NUMBER() OVER (ORDER BY "Batch_ID") ID,"WM_Record_ID","Batch_ID","WM_URL","Input_Date","Record_Status" FROM "MIA_AE_WM_In" WHERE "Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" = {}  or "Record_Status" is NULL ))SELECT * FROM WM_input WHERE ID Between {} and {} and ("Record_Status" != {})'.format(Batch, rs1, rs3, Processcount, Processcount1,rs1))

def AttributeExtraction(lines):
        pgproblem = ''
        try:
            driver.get(lines[3])
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(15)
        except:
            pass
        cursor.execute('UPDATE "MIA_AE_WM_In" SET "Record_Status" = (%s) WHERE "Batch_ID" = (%s) and "WM_URL" = (%s);', ('Initiated',Batch ,lines[3]))
        connection.commit()
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
                    for val in range(0,3):
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

        

        if pgproblem == '':
            
            # Breadcrumb
            try:
                    breadcrumbtag = soup.find("nav", class_="ma3 mh0-m mh0-xl mb4-xl")
                    if breadcrumbtag == None:
                        breadcrumbtag = soup.find("nav", class_="mh3 mh0-m mh0-xl mb4-xl mv3")
                        if breadcrumbtag == None:
                            breadcrumbtag = soup.find("nav", class_="mh3 mh0-xl mb4-xl mh0-m mv3")
                            if breadcrumbtag == None:
                                breadcrumbtag = soup.find("nav", class_="mh3 mh0-xl mb4-xl mh0-m mv2 mv3-m lh-title lh-copy-m")


                    breadcrumb = breadcrumbtag.text

            except:
                pass

            
        lines = lines[3].replace('\n', "")
        itemid = "".join(lines.split('/', -1)[-1]).replace('?selected=true', '')
        screenshot_path = outpath + '\\' + itemid + '.html'
        itemid = itemid.replace('.html', '')

        try:
            pyautogui.press('alt')
        except:
            pass
        return pgproblem ,itemid, breadcrumb,screenshot_path
        


cursor.execute('WITH WM_input AS(SELECT ROW_NUMBER() OVER (ORDER BY "Batch_ID") ID,"WM_Record_ID","Batch_ID","WM_URL","Input_Date","Record_Status" FROM "MIA_AE_WM_In" WHERE "Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" = {}  or "Record_Status" is NULL ))SELECT * FROM WM_input WHERE ID Between {} and {} and ("Record_Status" != {})'.format(Batch, rs1, rs3, Processcount, Processcount1,rs1))
record = len(cursor.fetchall())

if record != 0:
    chrome_options = Options()
    chrome_options.add_argument('--headerless')
    chrome_options.add_argument("--window-size=3200x20800")
    driver = uc.Chrome(enable_cdp_events=True, Options = chrome_options)


if record != 0:
    query()
    for url_lines in cursor.fetchall():
        pgproblem, itemid, breadcrumb,screenshot_path = AttributeExtraction(url_lines)

        wmid = url_lines[1]
        tooldate = datetime.now().strftime("%Y-%m-%d")
        tooltime = datetime.now().strftime("%H:%M:%S")
        url = url_lines[3]
        batch_id = url_lines[2]
        pgproblem = pgproblem
        itemid = itemid
        breadcrumb = breadcrumb
        screenshot_path = screenshot_path
        
        # Filename
        filename = itemid + '.html'
        n = os.path.join(outpath, filename)

        # Offline Download
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
        
        cursor.execute('INSERT INTO "MIA_AE_WM_Out" (WM_Record_ID,Tool_Date,Tool_Time,Batch_ID,WM_URL,URL_Status,Item_ID,Breadcrumb,Screenshot_Path) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                        (wmid, tooldate, tooltime, batch_id, url, pgproblem, itemid, breadcrumb,screenshot_path))
        connection.commit()

        itemid = "'"+itemid+"'"
        
        cursor.execute('SELECT "batch_id","item_id" FROM "MIA_AE_WM_Out" WHERE ("batch_id" = {} and "item_id" = {})'.format(Batch,itemid))
        
        fetrecord = len(cursor.fetchall())
        if fetrecord != 0:
            cursor.execute('UPDATE "MIA_AE_WM_In" SET "Record_Status" = (%s) WHERE "Batch_ID" = (%s) and "WM_URL" = (%s)', ('Processed',Batch ,url_lines[3]))
            connection.commit()
            
        cursor.execute('WITH WM_input AS(SELECT ROW_NUMBER() OVER (ORDER BY "Batch_ID") ID,"WM_Record_ID","Batch_ID","WM_URL","Input_Date","Record_Status" FROM "MIA_AE_WM_In" WHERE "Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" = {}  or "Record_Status" is NULL ))SELECT * FROM WM_input WHERE ID Between {} and {} and ("Record_Status" != {})'.format(Batch, rs1, rs3, Processcount, Processcount1,rs1))
        record1 = len(cursor.fetchall())
        record = record1
        tcount = tcount + 1
        rows = (Processcount1-Processcount)+1
        print("Completed " + str(tcount) + " URLs out of " + str(rows))
        driver.quit

else:
    print("The Given range of URLs are Processed")

cursor.execute('select count(*) from "MIA_AE_WM_In" WHERE ("Batch_ID" = {} and ("Record_Status" != {} or "Record_Status" is NULL or "Record_Status" = {} ))'.format(Batch,rs1,rs2))

rows = cursor.fetchone()[0]
print("Remaining " + str(rows) + " URLs")
os.system("pause")
