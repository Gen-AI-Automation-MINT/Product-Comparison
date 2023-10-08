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

val = "''NULL'"
#Private Brand
cursor.execute('SELECT "PVT_Brand" FROM "MIA_AE_PVT_BRAND"')
privatebrand = cursor.fetchall()
privatebrandlist = []
for i in range(len(privatebrand)):
  privatebrandlist.append(privatebrand[i][0].lower())

#Color List
cursor.execute('SELECT "Colors" FROM "All_References" Where "Colors" != {}'.format(val))
colorscolumn = cursor.fetchall()
colorslist = []
for i in range(len(colorscolumn)):
  colorslist.append(colorscolumn[i][0].lower().strip())

#Platform list
cursor.execute('"SELECT "VG_Platform" FROM "VG_Platforms"')
platform = cursor.fetchall()
platformlist = []
for i in range(len(platform)):
  platformlist.append(platform[i][0].lower())


#Input Paths
with open("Inputpath.txt") as z:
    lines = z.read()
    outpath = lines.split('\n', 1)[0]
    z.close

tcount=0

rs1 = "'Processed'"
rs2 = "''"
rs3 = "'Initiated'"

def book(soup):
        titleISBN13 = ""
        titleISBN10 = ""
        prodetailISBN13 = ""
        prodetailISBN10 = ""
        titleformat = ""
        prodetformat = ""
        wmcondition = ""
        dspagecount = ""
        try:
            # Title ISBN13
            wtitles = soup.find("title").text
            wtitles = wtitles.replace(")", " ")
            wtitles = wtitles.split(" ")
            for i in wtitles:
                if len(i) == 13 and i.isnumeric():
                    titleISBN13 = i
        except:
            pass

        try:
            # Title ISBN10
            wtitles = soup.find("title").text
            wtitles = wtitles.replace(")", " ")
            wtitles = wtitles.split(" ")
            for i in wtitles:
                if len(i) == 10 and i.isnumeric():
                    titleISBN10 = i
                elif 'X' in i:
                    val = i[-1]
                    val1 = i.replace(i[-1], "")
                    if len(val1) == 9 and val1.isnumeric():
                        i = val1 + val
                        titleISBN10 = i
        except:
            pass

        try:
            # Product details ISBN
            prodet = soup.find_all('div', class_='dangerous-html mb3')
            for i in prodet:
                prodet_text = i.text.split(" ")
                for j in prodet_text:
                    j = j.replace(',', "").replace('-', "").replace(".", "")
                    if len(j) == 13 and j.isnumeric():
                        prodetailISBN13 = j
        except:
            pass

        try:
            # Product details ISBN
            prodet = soup.find_all('div', class_='dangerous-html mb3')
            for i in prodet:
                prodet_text = i.text.split(" ")
                for j in prodet_text:
                    j = j.replace(',', "").replace('-', "").replace(".", "")
                    if len(j) == 10 and j.isnumeric():
                        prodetailISBN10 = j
                    elif 'X' in j:
                        val = j[-1]
                        val1 = j.replace(j[-1], "")
                        if len(val1) == 9 and val1.isnumeric():
                            j = val1 + val
                            prodetailISBN10 = j
        except:
            pass

        #Product details Pagecount
        try:
            prodet = soup.find_all('div', class_='dangerous-html mb3')
            for i in prodet:
                    prodet_text = i.text.split(".")
                    ran = len(prodet_text)
                    for j in range(0,ran):
                        if "Pages:" in prodet_text[j].strip():
                            val = prodet_text[j].strip()
                            val = val.replace("Pages: ","")
                            if val.isnumeric():
                                dspagecount = val
                        elif "pages," in prodet_text[j].strip():
                            val = prodet_text[j].strip()
                            val = val.replace("pages,","").replace("soft","").replace("cover","")
                            if val.isnumeric():
                                dspagecount = val
                        else:
                            j = j+1
        except:
                pass

        try:
            # title format
            searched_word_format = 'Paperback'
            titlepapercls = soup.find("title")
            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                recursive=True)

            if len(titlepaper) != 0:
                titleformat = "Paperback"
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
                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                                            recursive=True)
                        if len(titlepaper) != 0:
                            titleformat = "Audiobook"
                        else:
                            searched_word_format4 = 'Board book'
                            titlepaper = titlepapercls.find_all(
                                string=re.compile('.*{0}.*'.format(searched_word_format4)),
                                recursive=True)
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
                                        searched_word_format7 = 'Mass Market Paperback'
                                        titlepaper = titlepapercls.find_all(
                                            string=re.compile('.*{0}.*'.format(searched_word_format7)), recursive=True)
                                        if len(titlepaper) != 0:
                                            titleformat = "Mass Market Paperback"
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
                                                                        searched_word_format15 = 'CD-Audio'
                                                                        titlepaper = titlepapercls.find_all(
                                                                            string=re.compile(
                                                                                '.*{0}.*'.format(
                                                                                    searched_word_format15)),
                                                                            recursive=True)

                                                                        if len(titlepaper) != 0:
                                                                            titleformat = "Audio CD"
        except:
            pass

        try:
            # prodet format
            searched_word_format = 'Paperback'
            prodetpaperclss = soup.find_all('div', class_='dangerous-html mb3')
            for prodetpapercls in prodetpaperclss:
                prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                    recursive=True)
                if len(prodetpaper) != 0:
                    prodetformat = "Paperback"
                else:
                    searched_word_format1 = 'Hardcover'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format1)),
                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetformat = "Hardcover"
                    else:
                        searched_word_format2 = 'Dvd'
                        prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format2)),
                                                            recursive=True)
                        if len(prodetpaper) != 0:
                            prodetformat = "DVD"
                        else:
                            searched_word_format3 = 'Audiobook'
                            prodetpaper = prodetpapercls.find_all(
                                string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                recursive=True)
                            if len(prodetpaper) != 0:
                                prodetformat = "Audiobook"
                            else:
                                searched_word_format4 = 'Board book'
                                prodetpaper = prodetpapercls.find_all(
                                    string=re.compile('.*{0}.*'.format(searched_word_format4)),
                                    recursive=True)
                                if len(prodetpaper) != 0:
                                    prodetformat = "Board Book"
                                else:
                                    searched_word_format5 = 'Picture Book'
                                    prodetpaper = prodetpapercls.find_all(
                                        string=re.compile('.*{0}.*'.format(searched_word_format5)),
                                        recursive=True)
                                    if len(prodetpaper) != 0:
                                        prodetformat = "Picture Book"
                                    else:
                                        searched_word_format6 = 'Trade Paperback'
                                        prodetpaper = prodetpapercls.find_all(
                                            string=re.compile('.*{0}.*'.format(searched_word_format6)), recursive=True)
                                        if len(prodetpaper) != 0:
                                            prodetformat = "Trade Paperback"
                                        else:
                                            searched_word_format7 = 'Mass Market Paperback'
                                            prodetpaper = prodetpapercls.find_all(
                                                string=re.compile('.*{0}.*'.format(searched_word_format7)), recursive=True)
                                            if len(prodetpaper) != 0:
                                                prodetformat = "Mass Market Paperback"
                                            else:
                                                searched_word_format8 = 'Kindle'
                                                prodetpaper = prodetpapercls.find_all(
                                                    string=re.compile('.*{0}.*'.format(searched_word_format8)),
                                                    recursive=True)
                                                if len(prodetpaper) != 0:
                                                    prodetformat = "Kindle"
                                                else:
                                                    searched_word_format9 = 'Ebook'
                                                    prodetpaper = prodetpapercls.find_all(
                                                        string=re.compile('.*{0}.*'.format(searched_word_format9)),
                                                        recursive=True)
                                                    if len(prodetpaper) != 0:
                                                        prodetformat = "Ebook"
                                                    else:
                                                        searched_word_format10 = 'Audio CD'
                                                        prodetpaper = prodetpapercls.find_all(
                                                            string=re.compile('.*{0}.*'.format(searched_word_format10)),
                                                            recursive=True)
                                                        if len(prodetpaper) != 0:
                                                            prodetformat = "Audio CD"
                                                        else:
                                                            searched_word_format11 = 'Soft Cover (Paperback)'
                                                            prodetpaper = prodetpapercls.find_all(
                                                                string=re.compile('.*{0}.*'.format(searched_word_format11)),
                                                                recursive=True)
                                                            if len(prodetpaper) != 0:
                                                                prodetformat = "Soft Cover (Paperback)"
                                                            else:
                                                                searched_word_format12 = 'DVD'
                                                                prodetpaper = prodetpapercls.find_all(string=re.compile(
                                                                    '.*{0}.*'.format(searched_word_format12)),
                                                                    recursive=True)
                                                                if len(prodetpaper) != 0:
                                                                    prodetformat = "DVD"
                                                                else:
                                                                    searched_word_format13 = 'Book'
                                                                    prodetpaper = prodetpapercls.find_all(string=re.compile(
                                                                        '.*{0}.*'.format(searched_word_format13)),
                                                                        recursive=True)
                                                                    if len(prodetpaper) != 0:
                                                                        prodetformat = "Book"
                                                                    else:
                                                                        searched_word_format14 = 'Flexibound'
                                                                        prodetpaper = prodetpapercls.find_all(
                                                                            string=re.compile(
                                                                                '.*{0}.*'.format(searched_word_format14)),
                                                                            recursive=True)
                                                                        if len(prodetpaper) != 0:
                                                                            prodetformat = "Flexibound"
                                                                        else:
                                                                            searched_word_format15 = 'CD-Audio'
                                                                            titlepaper = titlepapercls.find_all(
                                                                                string=re.compile(
                                                                                    '.*{0}.*'.format(
                                                                                        searched_word_format15)),
                                                                                recursive=True)

                                                                            if len(titlepaper) != 0:
                                                                                titleformat = "Audio CD"
        except:
            pass

        try:
            searched_word = 'USED - VERY GOOD Condition'
            title_con = soup.find("title")
            condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
            if (len(condition) != 0):
                wmcondition = 'USED - VERY GOOD Condition'
            else:
                searched_word = 'Used'
                condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
                if (len(condition) != 0):
                    wmcondition = 'Used'
                else:
                    searched_word = 'Pre-Owned'
                    condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
                    if (len(condition) != 0):
                        wmcondition = 'Pre-Owned'
                    else:
                        searched_word = 'Refurbished'
                        condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                       recursive=True)
                        if (len(condition) != 0):
                            wmcondition = 'Refurbished'
                        else:
                            searched_word = 'Renewed'
                            condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                           recursive=True)
                            if (len(condition) != 0):
                                wmcondition = 'Renewed'
                            else:
                                searched_word = 'Used / Pre-owned'
                                condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                               recursive=True)
                                if (len(condition) != 0):
                                    wmcondition = 'Used / Pre-owned'
        except:
            pass

        return titleISBN13,titleISBN10,prodetailISBN13,prodetailISBN10,titleformat,prodetformat,wmcondition,dspagecount

def extraction(soup):
            titleISBN13 = ""
            titleISBN10 = ""
            prodetailISBN13 = ""
            prodetailISBN10 = ""
            titleformat = ""
            prodetformat = ""
            wmcondition = ""
            dspagecount = ""
            try:
                # Title ISBN13
                wtitles = soup.find("title").text
                wtitles = wtitles.replace(")", " ")
                wtitles = wtitles.split(" ")
                for i in wtitles:
                    if len(i) == 13 and i.isnumeric():
                        titleISBN13 = i
            except:
                pass

            try:
                # Title ISBN10
                wtitles = soup.find("title").text
                wtitles = wtitles.replace(")", " ")
                wtitles = wtitles.split(" ")
                for i in wtitles:
                    if len(i) == 10 and i.isnumeric():
                        titleISBN10 = i
                    elif 'X' in i:
                        val = i[-1]
                        val1 = i.replace(i[-1],"")
                        if len(val1) == 9 and val1.isnumeric():
                            i = val1+val
                            titleISBN10 = i
            except:
                pass

            try:
                # Product details ISBN
                prodet = soup.find_all('div', class_='dangerous-html mb3')
                for i in prodet:
                    prodet_text = i.text.split(" ")
                    for j in prodet_text:
                        j = j.replace(',', "").replace('-', "").replace(".", "")
                        if len(j) == 13 and j.isnumeric():
                            prodetailISBN13 = j
            except:
                pass

            try:
                # Product details ISBN
                prodet = soup.find_all('div', class_='dangerous-html mb3')
                for i in prodet:
                    prodet_text = i.text.split(" ")
                    for j in prodet_text:
                        j = j.replace(',', "").replace('-', "").replace(".", "")
                        if len(j) == 10 and j.isnumeric():
                            prodetailISBN10 = j
                        elif 'X' in j:
                            val = j[-1]
                            val1 = j.replace(j[-1], "")
                            if len(val1) == 9 and val1.isnumeric():
                                j = val1 + val
                                prodetailISBN10 = j
            except:
                pass

            # Product details Pagecount
            try:
                prodet = soup.find_all('div', class_='dangerous-html mb3')
                for i in prodet:
                    prodet_text = i.text.split(".")
                    ran = len(prodet_text)
                    for j in range(0, ran):
                        if "Pages:" in prodet_text[j].strip():
                            val = prodet_text[j].strip()
                            val = val.replace("Pages: ", "")
                            if val.isnumeric():
                                dspagecount = val
                        elif "pages," in prodet_text[j].strip():
                            val = prodet_text[j].strip()
                            val = val.replace("pages,","").replace("soft","").replace("cover","")
                            if val.isnumeric():
                                dspagecount = val
                        else:
                            j = j + 1

            except:
                pass

            try:
                # title format
                searched_word_format = 'Paperback'
                titlepapercls = soup.find("title")
                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                    recursive=True)

                if len(titlepaper) != 0:
                    titleformat = "Paperback"
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
                            titlepaper = titlepapercls.find_all(
                                string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                recursive=True)
                            if len(titlepaper) != 0:
                                titleformat = "Audiobook"
                            else:
                                searched_word_format4 = 'Board book'
                                titlepaper = titlepapercls.find_all(
                                    string=re.compile('.*{0}.*'.format(searched_word_format4)),
                                    recursive=True)
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
                                            searched_word_format7 = 'Mass Market Paperback'
                                            titlepaper = titlepapercls.find_all(
                                                string=re.compile('.*{0}.*'.format(searched_word_format7)),
                                                recursive=True)
                                            if len(titlepaper) != 0:
                                                titleformat = "Mass Market Paperback"
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
                                                                string=re.compile(
                                                                    '.*{0}.*'.format(searched_word_format11)),
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
                                                                    titlepaper = titlepapercls.find_all(
                                                                        string=re.compile(
                                                                            '.*{0}.*'.format(searched_word_format13)),
                                                                        recursive=True)
                                                                    if len(titlepaper) != 0:
                                                                        titleformat = "Book"
                                                                    else:
                                                                        searched_word_format14 = 'Flexibound'
                                                                        titlepaper = titlepapercls.find_all(
                                                                            string=re.compile(
                                                                                '.*{0}.*'.format(
                                                                                    searched_word_format14)),
                                                                            recursive=True)
                                                                        if len(titlepaper) != 0:
                                                                            titleformat = "Flexibound"
            except:
                pass

            try:
                # prodet format
                searched_word_format = 'Paperback'
                prodetpaperclss = soup.find_all('div', class_='dangerous-html mb3')
                for prodetpapercls in prodetpaperclss:
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetformat = "Paperback"
                    else:
                        searched_word_format1 = 'Hardcover'
                        prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format1)),
                                                            recursive=True)
                        if len(prodetpaper) != 0:
                            prodetformat = "Hardcover"
                        else:
                            searched_word_format2 = 'Dvd'
                            prodetpaper = prodetpapercls.find_all(
                                string=re.compile('.*{0}.*'.format(searched_word_format2)),
                                recursive=True)
                            if len(prodetpaper) != 0:
                                prodetformat = "Dvd"
                            else:
                                searched_word_format3 = 'Audiobook'
                                prodetpaper = prodetpapercls.find_all(
                                    string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                    recursive=True)
                                if len(prodetpaper) != 0:
                                    prodetformat = "Audiobook"
                                else:
                                    searched_word_format4 = 'Board book'
                                    prodetpaper = prodetpapercls.find_all(
                                        string=re.compile('.*{0}.*'.format(searched_word_format4)),
                                        recursive=True)
                                    if len(prodetpaper) != 0:
                                        prodetformat = "Board Book"
                                    else:
                                        searched_word_format5 = 'Picture Book'
                                        prodetpaper = prodetpapercls.find_all(
                                            string=re.compile('.*{0}.*'.format(searched_word_format5)),
                                            recursive=True)
                                        if len(prodetpaper) != 0:
                                            prodetformat = "Picture Book"
                                        else:
                                            searched_word_format6 = 'Trade Paperback'
                                            prodetpaper = prodetpapercls.find_all(
                                                string=re.compile('.*{0}.*'.format(searched_word_format6)), recursive=True)
                                            if len(prodetpaper) != 0:
                                                prodetformat = "Trade Paperback"
                                            else:
                                                searched_word_format7 = 'Mass Market Paperback'
                                                prodetpaper = prodetpapercls.find_all(
                                                    string=re.compile('.*{0}.*'.format(searched_word_format7)),
                                                    recursive=True)
                                                if len(prodetpaper) != 0:
                                                    prodetformat = "Mass Market Paperback"
                                                else:
                                                    searched_word_format8 = 'Kindle'
                                                    prodetpaper = prodetpapercls.find_all(
                                                        string=re.compile('.*{0}.*'.format(searched_word_format8)),
                                                        recursive=True)
                                                    if len(prodetpaper) != 0:
                                                        prodetformat = "Kindle"
                                                    else:
                                                        searched_word_format9 = 'Ebook'
                                                        prodetpaper = prodetpapercls.find_all(
                                                            string=re.compile('.*{0}.*'.format(searched_word_format9)),
                                                            recursive=True)
                                                        if len(prodetpaper) != 0:
                                                            prodetformat = "Ebook"
                                                        else:
                                                            searched_word_format10 = 'Audio CD'
                                                            prodetpaper = prodetpapercls.find_all(
                                                                string=re.compile('.*{0}.*'.format(searched_word_format10)),
                                                                recursive=True)
                                                            if len(prodetpaper) != 0:
                                                                prodetformat = "Audio CD"
                                                            else:
                                                                searched_word_format11 = 'Soft Cover (Paperback)'
                                                                prodetpaper = prodetpapercls.find_all(
                                                                    string=re.compile(
                                                                        '.*{0}.*'.format(searched_word_format11)),
                                                                    recursive=True)
                                                                if len(prodetpaper) != 0:
                                                                    prodetformat = "Soft Cover (Paperback)"
                                                                else:
                                                                    searched_word_format12 = 'DVD'
                                                                    prodetpaper = prodetpapercls.find_all(string=re.compile(
                                                                        '.*{0}.*'.format(searched_word_format12)),
                                                                        recursive=True)
                                                                    if len(prodetpaper) != 0:
                                                                        prodetformat = "DVD"
                                                                    else:
                                                                        searched_word_format13 = 'Book'
                                                                        prodetpaper = prodetpapercls.find_all(
                                                                            string=re.compile(
                                                                                '.*{0}.*'.format(searched_word_format13)),
                                                                            recursive=True)
                                                                        if len(prodetpaper) != 0:
                                                                            prodetformat = "Book"
                                                                        else:
                                                                            searched_word_format14 = 'Flexibound'
                                                                            prodetpaper = prodetpapercls.find_all(
                                                                                string=re.compile(
                                                                                    '.*{0}.*'.format(
                                                                                        searched_word_format14)),
                                                                                recursive=True)
                                                                            if len(prodetpaper) != 0:
                                                                                prodetformat = "Flexibound"
            except:
                pass

            try:
                searched_word = 'USED - VERY GOOD Condition'
                title_con = soup.find("title")
                condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
                if (len(condition) != 0):
                    wmcondition = 'USED - VERY GOOD Condition'
                else:
                    searched_word = 'Used'
                    condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
                    if (len(condition) != 0):
                        wmcondition = 'Used'
                    else:
                        searched_word = 'Pre-Owned'
                        condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                       recursive=True)
                        if (len(condition) != 0):
                            wmcondition = 'Pre-Owned'
                        else:
                            searched_word = 'Refurbished'
                            condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                           recursive=True)
                            if (len(condition) != 0):
                                wmcondition = 'Refurbished'
                            else:
                                searched_word = 'Renewed'
                                condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                               recursive=True)
                                if (len(condition) != 0):
                                    wmcondition = 'Renewed'
                                else:
                                    searched_word = 'Used / Pre-owned'
                                    condition = title_con.find_all(string=re.compile('.*{0}.*'.format(searched_word)),
                                                                   recursive=True)
                                    if (len(condition) != 0):
                                        wmcondition = 'Used / Pre-owned'
            except:
                pass

            return titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, titleformat, prodetformat, wmcondition, dspagecount
#Movies EX

def movies(soup):
        prodetduration = ""
        titleformat = ""
        prodetepisodes = ""
        prodetseasons = ""
        prodetvolumes = ""
        #Product Details
        try:
                prodetlist = []
                # Product details Format
                searched_word_format = 'CD'
                prodetpaperclss = soup.find_all('div', class_='dangerous-html mb3')
                for prodetpapercls in prodetpaperclss:
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format)),
                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('CD')
                        
                    searched_word_format8 = 'Vinyl'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format8)),
                                                                                                recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('Vinyl')
                        
                    searched_word_format1 = 'Dvd'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format1)),
                                                                            recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('DVD')
                        
                    searched_word_format5 = 'DVD'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format5)),
                                                                                recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('DVD')

                    searched_word_format2 = 'Blu-ray'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format2)),
                                                                                    recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('Blu-Ray')

                    searched_word_format3 = 'Blu-Ray'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format3)),
                                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('Blu-Ray')
                    
                    searched_word_format11 = 'Bd'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format11)),
                                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('Blu-Ray')

                    searched_word_format12 = 'BD'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format12)),
                                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('Blu-Ray')
                                    
                    searched_word_format7 = 'NTSC'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format7)),
                                                                                            recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('NTSC')
                                        
                    searched_word_format8 = 'Vinyl'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format8)),
                                                                                                recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('Vinyl')
                                            
                    searched_word_format4 = '4K Ultra HD'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format4)),
                                                                                                    recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('4K Ultra HD') 
                                                
                    searched_word_format6 = '4K Ultra Hd'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format6)),
                                                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('4K Ultra HD')

                    searched_word_format9 = '4K Uhd'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format9)),
                                                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('4K Ultra HD')

                    searched_word_format10 = '4K UHD'
                    prodetpaper = prodetpapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format10)),
                                                                                                        recursive=True)
                    if len(prodetpaper) != 0:
                        prodetlist.append('4K Ultra HD')    
                    
                                                        
        except:
            pass
        try:
                # Product details duration
                prodet = soup.find_all('div', class_='dangerous-html mb3')
                for i in prodet:
                    prodet_text = i.text.replace("Runtime","Runtime:").replace(": ",":")
                    prodet_text = prodet_text.split(" ")
                    for j in prodet_text:
                        if 'runtime:' in j.lower():
                            prodetduration = j.replace("Runtime:","").replace(":","")
                            
        except:
            pass
        
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
                    searched_word_format2 = 'CD'
                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format2)),recursive=True)
                    if len(titlepaper) != 0:
                        titleformat = "CD"
                    else:
                        searched_word_format3 = 'Blu-Ray'
                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format3)),recursive=True)
                        if len(titlepaper) != 0:
                            titleformat = "Blu-Ray"
                        else:
                            searched_word_format4 = 'Blu-ray'
                            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format4)),recursive=True)
                            if len(titlepaper) != 0:
                                titleformat = "Blu-Ray"
                            else:
                                searched_word_format11 = 'Bd'
                                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format11)),recursive=True)
                                if len(titlepaper) != 0:
                                    titleformat = "Blu-Ray"
                                else:
                                    searched_word_format11 = 'BD'
                                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format11)),recursive=True)
                                    if len(titlepaper) != 0:
                                        titleformat = "Blu-Ray"
                                    else:
                                        searched_word_format5 = 'NTSC'
                                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format5)),recursive=True)
                                        if len(titlepaper) != 0:
                                            titleformat = "NTSC"
                                        else:
                                            searched_word_format8 = 'Vinyl'
                                            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format8)),recursive=True)
                                            if len(titlepaper) != 0:
                                                titleformat = "Vinyl"
                                            else:
                                                searched_word_format6 = '4K Ultra HD'
                                                titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format6)),recursive=True)
                                                if len(titlepaper) != 0:
                                                    titleformat = "4K Ultra HD"
                                                else:
                                                    searched_word_format7 = '4K Ultra Hd'
                                                    titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format7)),recursive=True)
                                                    if len(titlepaper) != 0:
                                                        titleformat = "4K Ultra HD"
                                                    else:
                                                        searched_word_format9 = '4K Uhd'
                                                        titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format9)),recursive=True)
                                                        if len(titlepaper) != 0:
                                                            titleformat = "4K Ultra HD"
                                                        else:
                                                            searched_word_format10 = '4K UHD'
                                                            titlepaper = titlepapercls.find_all(string=re.compile('.*{0}.*'.format(searched_word_format10)),recursive=True)
                                                            if len(titlepaper) != 0:
                                                                titleformat = "4K Ultra HD"
        except:
            pass

        try:
                # Product details episodes,seasons,volumes
                prodet = soup.find_all('div', class_='dangerous-html mb3')
                for i in prodet:
                    prodet_text = i.text.lower()
                    findepi = 'episodes'
                    findsea = 'season'
                    findvol = 'volume'
                    numwords = 1

                    for i in prodet_text.split('\n'):
                        z = i.split(' ')
                        for x in [x for (x, y) in enumerate(z) if findepi in y]:
                            episodeslist = z[max(x-numwords,0):x+numwords+1]
                            for j in episodeslist:
                                j = t2d.convert(j)
                                if  j.isnumeric():
                                    prodetepisodes = j
                        for x in [x for (x, y) in enumerate(z) if findsea in y]:
                            seasonlist = z[max(x-numwords,0):x+numwords+1]
                           
                            for j in seasonlist:
                                    j = t2d.convert(j)
                                    if  j.isnumeric():
                                        prodetseasons = j
                        for x in [x for (x, y) in enumerate(z) if findvol in y]:
                            volumelist = z[max(x-numwords,0):x+numwords+1]
                            for j in volumelist:
                                    j = t2d.convert(j)
                                    if  j.isnumeric():
                                        prodetvolumes = j     
        except:
            pass

        return prodetlist,prodetduration,titleformat,prodetepisodes,prodetseasons,prodetvolumes

def autotires(soup,wmtiresize,wmfeatures):
        prodettiresize = ""
        prodetloadrange = ""
        titletiresize = ""
        titleloadrange = ""
        titlespeedrating = ""
        
        #Title tiresize,load range
        try:
            title_ex = soup.find("title").text.split(" ")
            count = 0
            for i in title_ex:
                count += 1
                
                if '/' in i or 'x' in i or '.' in i or ('-' in i and '/' in i):
                    j = re.sub('\D', '', i)
                    if j == wmtiresize :
                        titletiresize = j
                    elif len(j) == len(wmtiresize):
                        titletiresize = j
                    else:
                        titletiresize = j

                if 'PLY' in i:
                    titleloadrange = i 
                else:
                    if titletiresize != '':
                        j = re.sub('\D', '', title_ex[count])
                        if j == '':
                            lval = count+1
                            j = re.sub('\D', '', title_ex[lval])
                        if j != '':
                            lspeed = title_ex[count+1]        
                        else:
                            lspeed = title_ex[count]
                        
                        if lspeed.isalpha() and len(lspeed) == 1:
                            titlespeedrating = lspeed
                        else:
                            if title_ex[count].isalnum():
                                for i in title_ex[count]:
                                    if i.isalpha():
                                        if len(i) == 1:
                                            titlespeedrating = i

                        titleloadrange = j
                        break
                
        except:
            pass


        #Product details Pagecount
        try:
            prodet = soup.find_all('div', class_='dangerous-html mb3')
            for i in prodet:
                    count = 0
                    li_tag = i.find_all('li')
                    for j in li_tag:
                        prodet_text = j.text
                        if "Size:" in prodet_text.strip():
                            if prodettiresize == '':
                                val = prodet_text.strip()
                                val = val.replace("Size:","")
                                val = re.sub('\D', '', val)
                                prodettiresize = val
                                
                        if "Load Range:" in prodet_text.strip():
                            if prodetloadrange == '':
                                val = prodet_text.strip()
                                val = val.replace("Load Range:","").replace(" ","").replace("G(","").replace(")","")
                                prodetloadrange = val
                       
                                
            if prodettiresize == '' or prodetloadrange == '':
                for i in prodet:
                    count = 0
                    prodet_text = i.text.replace(" x","x").replace("x ","x").replace("* ","*").replace(" *","*").split(" ")
                    for k in prodet_text:
                        count += 1
                        if '/' in k or 'x' in k:
                            if (wmtiresize != '' and '0' not in wmtiresize):
                                j = re.sub('\D', '', k).replace('0',"")
                            else: 
                                j = re.sub('\D', '', k)

                            if (wmtiresize != '' and j == wmtiresize) or (titletiresize != '' and j == titletiresize):
                                prodettiresize = j
                            elif wmtiresize != '' and len(j) == len(wmtiresize):
                                    prodettiresize = j
                            else:
                                if j.isnumeric():
                                    prodettiresize = j
                            if prodettiresize != '':
                                    l = re.sub('\D', '', prodet_text[count])
                                    prodetloadrange = l
                                    
                        if prodetloadrange != '':
                            if "-ply" in k:
                                prodetloadrange = k.replace("-","")
                                               
                                               
        except:
            pass
        if titleloadrange == '' and prodetloadrange == '':
                wmfeatures = wmfeatures.split(",")
                for i in wmfeatures:
                    if 'Load Range:' in i:
                        lr = i.replace("Load Range: ","").strip().split(" ")
                        prodetloadrange = lr[0].strip()
        
        
        return prodettiresize,prodetloadrange,titletiresize,titleloadrange,titlespeedrating


def videogames(soup):
    titleplatform = ""
    prodetplatformlist = []
    try:
        # Product details ISBN
        prodetpaperclss = soup.find_all('div', class_='dangerous-html mb3')
        for prodetpapercls in prodetpaperclss:
            prodetpapercls = prodetpapercls.text.lower()
            for i in platformlist:
                if i in prodetpapercls:
                    prodetplatformlist.append(i)   
    except:
        pass

    #Title Platform
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

    return prodetplatformlist,titleplatform


def electronics(soup):
    prodetcolor = ""
    swatchcolor = ""
    prodetsize = ""
    swatchsize = ""
    titlepackcount = ""
    prodetpackcount = ""
    prodetos = ""
    prodetvolts = ""
    prodetnetwork = ""
    titlecolor = ""
    prodetresolution = ""
    prodetitemtype = ""
    #Product Details
    try:
        prodet = soup.find_all('div', class_='dangerous-html mb3')
        for i in prodet:
            i = i.text.replace(": ",':').replace("x ","x").replace(" x","x").replace(", ",",").replace("approx. ","").replace("Chart:","").replace("Package Contents:","PackageContents:").replace("Working Voltage","WorkingVoltage").replace("Supply Voltage","SupplyVoltage").replace("Input voltage","Inputvoltage").replace("Operating system","Operatingsystem").replace("Color :","Color:").replace("Resolution: ","Resolution:").replace("Type: ","Type:").split(" ")
            count = 0
            for j in i:
                count += 1
                if 'Colour:' in j or 'Color:' in j or 'color:' in j or 'colour:' in j:
                   prodetcolor = j.replace("Colour:","").replace("color:","").replace("colour:","").replace("Color:","").strip()
                if "Size:" in j or "size:" in j:
                    prodetsize = j.replace("Size:","").replace("size:","").strip()
                if "Pcs" in j:
                    packcount = j.replace("Pcs","")
                    if packcount.isnumeric():
                        prodetpackcount = packcount
                    else:
                        prodetpackcount = i[count-2]
                if prodetpackcount == '':
                    if "PackageContents:" in j:
                        prodetpackcount = j.replace("PackageContents:","").replace("heat","").replace("*","")
                if 'WorkingVoltage:' in j or 'SupplyVoltage:' in j or 'Inputvoltage' in j:
                    prodetvolts = j.replace("WorkingVoltage:","").replace("SupplyVoltage:","").replace("Inputvoltage:","").strip()
                if 'Operatingsystem:' in j:
                    prodetos = j.replace("Operatingsystem:","").strip()  
                if 'Type:' in j:
                    prodetitemtype = j.replace("Type:","").strip()
                if 'Resolution:' in j:
                    prodetresolution = j.replace("Resolution:","").strip() 
                if 'Network:' in j:
                    j = j.strip()
                    j = j.split("Network:")
                    if len(j) > 0: 
                        prodetnetwork = j[1]
                
    except:
        pass
    try:
            titlepapercls = soup.find("title")
            words = titlepapercls.text.replace("."," ").replace(","," ").split()
            for word in words:
                titlecol = word.lower()
                for i in colorslist:
                    if i == titlecol:
                        titlecolor = titlecol
    except:
        pass

    try:
        if prodetos == '':
            prodet = soup.find_all('div', class_='dangerous-html mb3')
            for i in prodet:
                    count = 0
                    li_tag = i.find_all('li')
                    for j in li_tag:
                        prodet_text = j.text
                        if "Operating System:" in prodet_text.strip():
                            if prodettiresize == '':
                                val = prodet_text.strip()
                                val = val.replace("Operating System:","").strip()
                                prodetos = val
                    if li_tag == []:
                        tr_tag = i.find_all("tr")
                        for j in tr_tag:
                            prodet_text = j.text
                            if 'Operating System' in prodet_text and 'Operating System Platform' not in prodet_text and 'Upgradable Operating System' not in prodet_text:
                                prodetos = prodet_text.replace("Operating System","").strip()

                   
    except:
        pass

    #swatch
    try:
        swatch = soup.find_all("div",class_="w-100 f6 mt2")
        for i in swatch:
           i = i.find_all("div", class_="mb2 mid-gray")
           for j in i:
            j = j.text.strip()
            if "Actual Color:" in j:
                swatchcolor = j.replace("Actual Color:","")
            if "Size:" in j:
                swatchsize = j.replace("Size:","")
    except:
        pass

    #Title
    try:
        wtitles = soup.find("title").text.lower().split(" ")
        count = 0
        for i in wtitles:
            count += 1
            if "pcs" in i:
                titlepackcount = i.replace("pcs","").strip()
                if titlepackcount == '':
                    titlepackcount = wtitles[count-2]
    except:
        pass
    
    return prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype

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

        

        wmtitbrand = wmtitle = wmprice = wmspec = wmdes = breadcrumb = wmspbrand = wmspformat = wmspmanuf = wmsppartno = wmspmodel = wmspcolor = ""
        wmsppack = wmspshape = wmspdimen = wmspgender = wmspsize = wmpagecount  = upc = swatchformat = hprice = wmspISBN13 = wmspISBN10 = titleISBN13 = ""
        titleISBN10 = titleformat = prodetformat = wmcondition = prodetailISBN13 = prodetailISBN10 = matchtype = matchtypecomments = dspagecount = ""
        wmoccasion = wmgemstonetype = wmringstyle = wmstyle = wmcarats = wmgemstonecut = wmkarats = wmfinefashion = wmtheme = wmbirthstone = wmgemstoneshape = ""
        wmbandwidth = wmfinish = wmfeature = wmmaterial = wmmetaltype = wmchainlenght =  wmagegroup = wmdiamondclarity = wmstyle = ""
        wmcountryorigin = wmclothingsize = wmfeatures = wmsleevelength = wmneckstyle = wmpattern = wmfabriccontent = ""
        wmmoviegenre =  wmtargetaudience = wmedition = wmactors = wmduration = wmstudioproductioncompany = wmcharacter = ""
        wmdirector = wmreleasedate = wmsptitle = wmlanguage = wmseriestitle = wmtreleasedate = wmpublisher = wmpublicationdate = ""
        wmperformer = wmrecordlabel = wmpmediaformat = wmtracklist =  wmmusicgenre = wmagegroup = prodetduration = ""
        titleepisodes = titleseasons = titlevolumes = prodetepisodes = prodetseasons = prodetvolumes = ""
        wmtiresize = prodettiresize = prodetloadrange = titletiresize = titleloadrange = wmtirespeedrating = titlespeedrating =""
        wmvehicletype = wmtirewidth = wmwheeldiameter = wmutqg = wmtiretractionrating = wmtiretreadwearrating = wmtireseason = wmtreaddepth = ""
        sold = ""
        wmvideogameplatform = wmgenre = wmvideogamecollection = wmharddrivecapacity = wminternalorextrenal = wmesrbrating = ""
        wmiscordless = wmcompatibledevice = wmcompatiblebrands = prodetplatform = titleplatform = ""

        wmprocessortype = wmos = wmprocessorspeed = wmwirelesstech = wmrammemory = wmscreensize = wmprocessorbrand = ""
        prodetos = prodetvolts = prodetnetwork = prodetcolor = swatchcolor = titlecolor = prodetsize = swatchsize = prodetresolution = ""
        prodetitemtype = ""

        swatchdetails  = []
        swatchdetails_highlighted  = []
        imageurl  = []
        prodetlist = ""
        prodetplatformlist = ""

        if pgproblem == '':
            try:
                #Brand
                titleload = soup.find('h1', class_='b lh-copy dark-gray mt1 mb2 f3')
                if titleload == None:
                    time.sleep(3)
                    driver.refresh()
                    time.sleep(3)

                wmtitbrandtag = soup.find('a', class_='f6 mid-gray lh-title')
                if wmtitbrandtag == None:
                    wmtitbrandtag = soup.find('a',class_='bg-transparent bn lh-solid pa0 sans-serif tc underline inline-button mid-gray pointer f6')
                wmtitbrand = wmtitbrandtag.text
            except:
                pass
            try:
                #Title
                wmtitletag = soup.find('h1', class_='b lh-copy dark-gray mt1 mb2 f3')
                if wmtitletag == None:
                    wmtitletag = soup.find("title")
                    
                wmtitle = wmtitletag.text
                if " - Walmart.com" in wmtitle:
                    wmtitle = wmtitle.replace(" - Walmart.com","")
                   
            except:
                pass
            try:
                #Price
                wmprice = soup.find('span',attrs={"itemprop":'price'}).text
            except:
                pass
            try:
                #Description
                wmdes=soup.find('div',class_='dangerous-html mb3').text
            except:
                pass

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

            #Specification
            try:
                tagcount = 0
                wmspecitemf = soup.findAll('h3',class_='flex items-center mv0 lh-copy f5 pb1 dark-gray')
                wmspecdataf = soup.findAll('p',class_='mv0 lh-copy f6 mid-gray')
                if wmspecdataf == []:
                    wmspecdataf = soup.findAll('div', class_='mv0 lh-copy f6 mid-gray')
                for headeritem in soup.findAll('h3',class_='flex items-center mv0 lh-copy f5 pb1 dark-gray'):

                    wmsecheader = wmspecitemf[tagcount]
                    wmspecdata = wmspecdataf[tagcount]
                    tagcount=tagcount+1
                    if wmsecheader.text == "Brand":
                        wmspbrand = wmspecdata.text
                    elif wmsecheader.text == "Gender":
                        wmspgender = wmspecdata.text
                    elif wmsecheader.text == "Color":
                        wmspcolor = wmspecdata.text
                    elif wmsecheader.text == "Format" or wmsecheader.text == "Book Format":
                        wmspformat = wmspecdata.text
                    elif wmsecheader.text == "Manufacturer":
                        wmspmanuf = wmspecdata.text
                    elif wmsecheader.text == "Manufacturer Part Number":
                        wmsppartno = wmspecdata.text
                    elif wmsecheader.text == "Model":
                        wmspmodel = wmspecdata.text
                    elif wmsecheader.text == "Count Per Pack":
                        wmsppack = wmspecdata.text
                    elif wmsecheader.text == "Shape":
                        wmspshape = wmspecdata.text
                    elif wmsecheader.text == "Assembled Product Dimensions (L x W x H)" or wmsecheader.text == "Assembled Product Weight":
                        wmspdimen = wmspecdata.text
                    elif wmsecheader.text == "Size":
                        wmspsize = wmspecdata.text
                    elif wmsecheader.text == "ISBN-13":
                        wmspISBN13 = wmspecdata.text
                    elif wmsecheader.text == "ISBN-10":
                        wmspISBN10 = wmspecdata.text
                    elif wmsecheader.text == "Condition":
                        wmcondition = wmspecdata.text
                    elif wmsecheader.text == "Number of Pages":
                        wmpagecount = wmspecdata.text
                    #jewel
                    elif wmsecheader.text == "Occasion":
                        wmoccasion = wmspecdata.text
                    elif wmsecheader.text == "Gemstone Type":
                        wmgemstonetype = wmspecdata.text
                    elif wmsecheader.text == "Ring Style":
                        wmringstyle = wmspecdata.text
                    elif wmsecheader.text == "Style":
                        wmstyle = wmspecdata.text
                    elif wmsecheader.text == "Carats":
                        wmcarats = wmspecdata.text
                    elif wmsecheader.text == "Gemstone Cut":
                        wmgemstonecut = wmspecdata.text
                    elif wmsecheader.text == "Karats":
                        wmkarats = wmspecdata.text
                    elif wmsecheader.text == "Fine or Fashion":
                        wmfinefashion = wmspecdata.text
                    elif wmsecheader.text == "Theme":
                        wmtheme = wmspecdata.text
                    elif wmsecheader.text == "Birthstone":
                        wmbirthstone = wmspecdata.text
                    elif wmsecheader.text == "Gemstone Shape":
                        wmgemstoneshape = wmspecdata.text
                    
                    #moview&tvshows
                    elif wmsecheader.text == "Movie Genre":
                        wmmoviegenre = wmspecdata.text
                    elif wmsecheader.text == "Target Audience":
                        wmtargetaudience = wmspecdata.text
                    elif wmsecheader.text == "Edition":
                        wmedition = wmspecdata.text
                    elif wmsecheader.text == "Actors":
                        wmactors = wmspecdata.text
                    elif wmsecheader.text == "Duration":
                        wmduration = wmspecdata.text
                    elif wmsecheader.text == "Studio & Production Company":
                        wmstudioproductioncompany = wmspecdata.text
                    elif wmsecheader.text == "Character":
                        wmcharacter = wmspecdata.text
                    elif wmsecheader.text == "Director":
                        wmdirector = wmspecdata.text
                    elif wmsecheader.text == "Release Date":
                        wmreleasedate = wmspecdata.text
                    elif wmsecheader.text == "Title":
                        wmsptitle = wmspecdata.text
                    elif wmsecheader.text == "Original Languages" or wmsecheader.text == "Language":
                        wmlanguage = wmspecdata.text
                    elif wmsecheader.text == "Series Title":
                        wmseriestitle = wmspecdata.text
                    elif wmsecheader.text == "Theatrical Release Date":
                        wmtreleasedate = wmspecdata.text
                    elif wmsecheader.text == "Publisher":
                        wmpublisher = wmspecdata.text
                    elif wmsecheader.text == "Publication Date":
                        wmpublicationdate = wmspecdata.text

                    #clothing
                    elif wmsecheader.text == "Country of Origin - Textiles":
                        wmcountryorigin = wmspecdata.text
                    elif wmsecheader.text == "Features":
                        wmfeatures = wmspecdata.text
                    elif wmsecheader.text == "Sleeve Length Style":
                        wmsleevelength = wmspecdata.text
                    elif wmsecheader.text == "Clothing Neck Style":
                        wmneckstyle = wmspecdata.text
                    elif wmsecheader.text == "Pattern":
                        wmpattern = wmspecdata.text
                    elif wmsecheader.text == "Fabric Content":
                        wmfabriccontent = wmspecdata.text
                    elif wmsecheader.text == "Clothing Size":
                        wmclothingsize = wmspecdata.text
    
                    #Music
                    elif wmsecheader.text == "Performer":
                        wmperformer = wmspecdata.text
                    elif wmsecheader.text == "Record Label":
                        wmrecordlabel = wmspecdata.text
                    elif wmsecheader.text == "Physical Media Format":
                        wmpmediaformat = wmspecdata.text
                    elif wmsecheader.text == "Track Listing":
                        wmtracklist = wmspecdata.text
                    elif wmsecheader.text == "Music Genre":
                        wmmusicgenre = wmspecdata.text
                    elif wmsecheader.text == "Age Group":
                        wmagegroup = wmspecdata.text

                    #Auto & Tires
                    elif wmsecheader.text == "Tire Size":
                        wmtiresize = wmspecdata.text
                    elif wmsecheader.text == "Vehicle Type":
                        wmvehicletype = wmspecdata.text
                    elif wmsecheader.text == "Tire Width":
                        wmtirewidth = wmspecdata.text
                    elif wmsecheader.text == "Wheel Diameter":
                        wmwheeldiameter = wmspecdata.text
                    elif wmsecheader.text == "Tire Speed Rating":
                        wmtirespeedrating = wmspecdata.text
                    elif wmsecheader.text == "Uniform Tire Quality Grade (UTQG)":
                        wmutqg = wmspecdata.text
                    elif wmsecheader.text == "Tire Traction Rating":
                        wmtiretractionrating = wmspecdata.text
                    elif wmsecheader.text == "Tire Treadwear Rating":
                        wmtiretreadwearrating = wmspecdata.text
                    elif wmsecheader.text == "Tire Season":
                        wmtireseason = wmspecdata.text
                    elif wmsecheader.text == "Tread Depth":
                        wmtreaddepth = wmspecdata.text

                    #Video Games
                    elif wmsecheader.text == "Video Game Platform":
                        wmvideogameplatform = wmspecdata.text
                    elif wmsecheader.text == "Genre":
                        wmgenre = wmspecdata.text
                    elif wmsecheader.text == "Video Game Collection":
                        wmvideogamecollection = wmspecdata.text
                    elif wmsecheader.text == "Hard Drive Capacity":
                        wmharddrivecapacity = wmspecdata.text
                    elif wmsecheader.text == "Internal/External":
                        wminternalorextrenal = wmspecdata.text
                    elif wmsecheader.text == "ESRB Rating:":
                        wmesrbrating = wmspecdata.text
                    elif wmsecheader.text == "Is Cordless":
                        wmiscordless = wmspecdata.text
                    elif wmsecheader.text == "Compatible Devices":
                        wmcompatibledevice = wmspecdataf.text
                    elif wmsecheader.text == "Compatible Brands":
                        wmcompatiblebrands = wmspecdata.text
                    
                    #Electronics
                    elif wmsecheader.text == "Processor Type":
                        wmprocessortype = wmspecdata.text
                    elif wmsecheader.text == "Operating System":
                        wmos = wmspecdata.text
                    elif wmsecheader.text == "Processor Speed":
                        wmprocessorspeed = wmspecdata.text
                    elif wmsecheader.text == "Wireless Technology":
                        wmwirelesstech = wmspecdata.text
                    elif wmsecheader.text == "RAM Memory":
                        wmrammemory = wmspecdata.text
                    elif wmsecheader.text == "Screen Size":
                        wmscreensize = wmspecdata.text
                    elif wmsecheader.text == "Processor Brand":
                        wmprocessorbrand = wmspecdata.text
                    
            except:
                pass

            #UPC
            try:
                bb = soup.find("script", attrs={"type":"application/ld+json"}).text
                li = list(bb.split(","))
                p = li[5].replace('"', '')
                p = p.replace(':', '')
                upc = p.replace("gtin13", '')

            except:
                pass

            #Swatch Details
            try:
                d = soup.find_all("div",class_="w-100 f6 mt2")
                for item in d:
                    swatch = item.find_all("div", class_="flex flex-wrap nl2")
                    for item1 in swatch:
                        swatchde = item1.text.strip()
                        #print("SwatchDetails =", swatchde)
                        swatchdetails.append(swatchde)
                        for it in swatch:
                            dd = it.find_all("label", class_="bg-white flex dark-gray pointer relative flex-column items-center b")
                            for it1 in dd:
                                swatchformat = it1.find("span", class_="").text.strip()
                                hprice = it1.find("span", class_="mt1 f6 h1").text.strip()

            except :
                pass
            
            try:           
                d = soup.find_all("div", class_="w-100 f6 mt2")
                for dd in d:
                    dd = dd.find_all("div",class_="mb2 mid-gray")
                    for ddd in dd:
                        color = ddd.find_all("span",class_="b")
                        dataex = ddd.find_all("span",class_="ml1")
                        for dcolor in color:
                            for ddata in dataex:
                                    if wmmetaltype == '':
                                        if dcolor.text == "Metal Type:":
                                            wmmetaltype = ddata.text
                                    if wmkarats == '':
                                        if dcolor.text == "Karats:":
                                            wmkarats = ddata.text
                                    if wmspsize == '':
                                        if dcolor.text == "Ring Size:" or dcolor.text == "Size:":
                                            wmspsize = ddata.text
                                    if wmspcolor == '':
                                        if dcolor.text == "Actual Color:":
                                            wmspcolor = ddata.text
                                    if dcolor.text == "Style:":
                                            wmstyle = ddata.text
                                    if wmclothingsize == '':
                                        if dcolor.text == "Clothing Size":
                                            wmclothingsize = ddata.text             
            except:
                pass

            try:
                # Product details ISBN
                prodet = soup.find_all('div', class_='dangerous-html mb3')
                for i in prodet:
                    prodet_text = i.text.split(" ")
                    for j in prodet_text:
                        j = j.replace(',', "").replace('-', "").replace(".", "")
                        if len(j) == 13 and j.isnumeric():
                            prodetailISBN13 = j
            except:
                pass

            #Imageurl
            try:
                imgurl = soup.find("div", class_="container overflow-y-hidden mv3")
                for i in imgurl:
                    i = i.find_all('img', attrs={'src': re.compile("^https:/")})
                    for li in i:
                        lin = li.get('src')
                        imageurl.append(lin)
            except:
                pass

            try:
                if '+' in wmspformat:
                    splitformat = wmspformat.replace(" ","").split('+')
                    for splitformat in splitformat:
                        if splitformat.lower() in 'dvd':
                            wmspformat = 'DVD'
                        elif splitformat.lower() in 'blu-ray':
                            wmspformat = 'Blu-Ray'
                        elif splitformat.lower() in 'cd':
                            wmspformat = 'CD'
                        elif splitformat.lower() in '4K ultra hd':
                            wmspformat = '4K Ultra HD'
            except:
                pass

            try:
                # Title episodes,seasons,volumes
               
                wmtitle = wmtitle.lower()
                findepi = 'episodes'
                findsea = 'season'
                findvol = 'volume'
                numwords = 1

                for i in wmtitle.split('\n'):
                        z = i.split(' ')
                        for x in [x for (x, y) in enumerate(z) if findepi in y]:
                            episodeslist = z[max(x-numwords,0):x+numwords+1]
                            for j in episodeslist:
                                j = t2d.convert(j)
                                if  j.isnumeric():
                                    titleepisodes = j

                        for x in [x for (x, y) in enumerate(z) if findsea in y]:
                            seasonlist = z[max(x-numwords,0):x+numwords+1]
                            for j in seasonlist:
                                    j = t2d.convert(j)
                                    if  j.isnumeric():
                                        titleseasons = j

                        for x in [x for (x, y) in enumerate(z) if findvol in y]:
                            volumelist = z[max(x-numwords,0):x+numwords+1]
                            for j in volumelist:
                                    j = t2d.convert(j)
                                    if  j.isnumeric():
                                        titlevolumes = j 
            except:
                pass
            #Sold and Shipped 
            try:
                soldtag = soup.find("div", attrs={"data-testid":"sold-and-shipped-by"})
                sold = soldtag.find("span", class_="lh-title").text.replace("Sold and shipped by ","").strip()                
               
            except:
                pass
            
            #Private brand check
            if wmtitbrand != '':
                if wmtitbrand.lower() in privatebrandlist:
                    pgproblem = 'Private Brand'
            elif wmspbrand != '':
                if wmspbrand.lower() in privatebrand:
                    pgproblem = 'Private Brand'

            
            breadcrumbsplit = list(breadcrumb.split("/"))
            if breadcrumbsplit[0] == "Books":
                titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, titleformat, prodetformat, wmcondition, dspagecount = book(soup)
            elif breadcrumbsplit[0] == "Movies & TV Shows" or breadcrumbsplit[0] == "Music":
                prodetlist,prodetduration,titleformat,prodetepisodes,prodetseasons,prodetvolumes = movies(soup)
            elif breadcrumbsplit[0] == "Auto & Tires" and breadcrumbsplit[1] == "Tires & Accessories":
                if wmtiresize != None:
                    wmtiresize = wmtiresize.split(" ")
                    wmtiresize = re.sub('\D', '', wmtiresize[0])
                prodettiresize,prodetloadrange,titletiresize,titleloadrange,titlespeedrating = autotires(soup,wmtiresize,wmfeatures)
            elif breadcrumbsplit[0] == "Video Games":
                prodetplatformlist,titleplatform = videogames(soup)
            elif (breadcrumbsplit[0] == "Electronics" and "Audio" in breadcrumbsplit or breadcrumbsplit[0] == "Audio") or (breadcrumbsplit[0] == "Electronics" and "Portable Audio" in breadcrumbsplit) or (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "Home Audio & Theater") or (breadcrumbsplit[0] == "Portable Audio"):
              prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)
            elif breadcrumbsplit[0] == "Electronics" and "Computers" in breadcrumbsplit or breadcrumbsplit[0] == "Computers":
                prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)
            elif breadcrumbsplit[0] == "Cell Phones" or (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "TV & Home Theater") or  (breadcrumbsplit[0] == "Electronics" and "iPad & Tablets" in breadcrumbsplit) or (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "TV & Video") or (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "Electronics Accessories"):
                prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)
            elif breadcrumbsplit[0] == "Electronics" and "Wearable Technology" in breadcrumbsplit:
                prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)   
            elif (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "Cameras & Camcorders") or (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "Drones") or (breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "Surveillance Equipment"):
                prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)
            elif breadcrumbsplit[0] == "Electronics" and breadcrumbsplit[1] == "GPS & Navigation":
                prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)
            elif breadcrumbsplit[0] == "Electronics":
                prodetcolor,swatchcolor,prodetsize,swatchsize,titlepackcount,prodetpackcount,prodetos,prodetvolts,prodetnetwork,titlecolor,prodetresolution,prodetitemtype = electronics(soup)
            else:
                titleISBN13, titleISBN10, prodetailISBN13, prodetailISBN10, titleformat, prodetformat, wmcondition, dspagecount = extraction(soup)

            titleformat = titleformat
            titleISBN13 = titleISBN13
            titleISBN10 = titleISBN10
            prodetailISBN13 = prodetailISBN13
            prodetailISBN10 = prodetailISBN10
            prodetlist = prodetlist
            wmcondition = wmcondition
            prodetduration = prodetduration
            prodetepisodes = prodetepisodes
            prodetseasons = prodetseasons
            prodetvolumes = prodetvolumes
            prodettiresize = prodettiresize
            prodetloadrange = prodetloadrange
            titletiresize = titletiresize
            titleloadrange = titleloadrange
            prodetplatformlist = prodetplatformlist
            titleplatform = titleplatform
            titlespeedrating = titlespeedrating

            prodetos = prodetos
            prodetvolts = prodetvolts
            prodetnetwork = prodetnetwork
            prodetcolor = prodetcolor
            swatchcolor = swatchcolor
            titlecolor = titlecolor
            prodetsize = prodetsize
            swatchsize = swatchsize
            prodetresolution = prodetresolution
            prodetitemtype = prodetitemtype

            if wmpagecount == '':
                wmpagecount = dspagecount

            if wmspformat != '' or titleformat != '' or wmpmediaformat != '':
                for i in prodetlist:
                    if wmspformat.lower() == 'lp':
                        wmspformat = 'Vinyl'
                    if i.lower() == 'lp':
                        i = 'Vinyl'
                    if titleformat.lower() == 'lp':
                        titleformat = 'Vinyl'
                    if wmpmediaformat.lower() == 'lp':
                        wmpmediaformat = 'Vinyl'
                    
                    if  i == wmspformat and i == titleformat:
                        prodetformat = i
                    elif  i == wmspformat and i == wmpmediaformat:
                        prodetformat = i
                    elif  i == titleformat and i == wmpmediaformat:
                        prodetformat = i
                    elif i == wmspformat:
                        prodetformat = i
                    elif i == titleformat:
                        prodetformat = i
                    elif i == wmpmediaformat:
                        prodetformat = i

            if ',' in wmvideogameplatform:
                wmvideogameplatform = wmvideogameplatform.split(",")
            elif '/' in wmvideogameplatform:
                wmvideogameplatform = wmvideogameplatform.split("/")

            for i in wmvideogameplatform:
                if titleplatform != '':
                    if i.lower().strip() == titleplatform:
                        wmvideogameplatform = i
                else:
                    wmvideogameplatform = wmvideogameplatform[0]
                    
            if titleplatform != '' and wmvideogameplatform != '':
                if wmvideogameplatform.lower().strip() == 'playstation 4' and titleplatform == 'ps4':
                    wmvideogameplatform = 'ps4'
                elif wmvideogameplatform.lower().strip() =='ps4' and titleplatform == 'playstation 4':
                    wmvideogameplatform = 'playstation 4'
                elif wmvideogameplatform.lower().strip() == 'playstation 5' and titleplatform == 'ps5':
                    wmvideogameplatform = 'ps5'
                elif wmvideogameplatform.lower().strip() =='ps5' and titleplatform == 'playstation 5':
                    wmvideogameplatform = 'playstation 5'
            
            if wmvideogameplatform != '' or titleplatform != '':
                for i in prodetplatformlist:
                    if i == wmvideogameplatform.lower():
                        prodetplatform = i
                    elif i == titleplatform.lower():
                        prodetplatform = i
            else:
                for i in prodetlist:
                    prodetplatform = i
             
            if wmtirespeedrating == '':
                    wmtirespeedrating = titlespeedrating
                        
            

        swatchdetails = str(swatchdetails)
        imageurl = str(imageurl)
        lines = lines[3].replace('\n', "")
        itemid = "".join(lines.split('/', -1)[-1]).replace('?selected=true', '')
        screenshot_path = outpath + '\\' + itemid + '.html'
        itemid = itemid.replace('.html', '')

        try:
            pyautogui.press('alt')
        except:
            pass
        return pgproblem,itemid, breadcrumb, wmtitbrand, wmtitle, wmprice, wmdes, titleformat, prodetformat, wmspbrand, wmspcolor, wmspformat, wmspmanuf,wmsppartno, wmspmodel, wmsppack, wmspshape, wmcondition, wmpagecount, titleISBN13, titleISBN10,prodetailISBN13, prodetailISBN10, wmspISBN13, wmspISBN10, wmspdimen, wmspgender, wmspsize, upc, swatchdetails,swatchformat, hprice, imageurl, screenshot_path, wmoccasion, wmringstyle, wmgemstonetype, wmstyle, wmcarats, wmgemstonecut, wmkarats, wmfinefashion, wmtheme, wmbirthstone, wmgemstoneshape,wmcountryorigin, wmfeatures, wmsleevelength, wmneckstyle, wmpattern, wmfabriccontent, wmclothingsize ,wmmoviegenre, wmtargetaudience, wmedition, wmactors, wmduration, wmstudioproductioncompany, wmcharacter, wmdirector, wmreleasedate, wmsptitle, wmlanguage, wmseriestitle, wmtreleasedate, wmpublisher, wmpublicationdate, wmperformer, wmrecordlabel, wmpmediaformat, wmtracklist, wmmusicgenre, wmagegroup, prodetduration, titleepisodes, titleseasons, titlevolumes, prodetepisodes, prodetseasons, prodetvolumes, wmtiresize, wmvehicletype, wmtirewidth, wmwheeldiameter, wmtirespeedrating,wmutqg, wmtiretractionrating,wmtiretreadwearrating,wmtireseason,wmtreaddepth,prodettiresize, prodetloadrange, titletiresize, titleloadrange,sold,wmvideogameplatform,wmgenre,wmvideogamecollection,wmharddrivecapacity,wminternalorextrenal,wmesrbrating,wmiscordless,wmcompatibledevice,wmcompatiblebrands,prodetplatform,titleplatform,wmprocessortype,wmos,wmprocessorspeed,wmwirelesstech,wmrammemory,wmscreensize,wmprocessorbrand,prodetos,prodetvolts,prodetnetwork,prodetcolor,swatchcolor,titlecolor,prodetsize,swatchsize,prodetresolution,prodetitemtype
        


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
        pgproblem, itemid, breadcrumb, wmtitbrand, wmtitle, wmprice, wmdes, titleformat, prodetformat, wmspbrand, wmspcolor, wmspformat, wmspmanuf,wmsppartno, wmspmodel, wmsppack, wmspshape, wmcondition, wmpagecount, titleISBN13, titleISBN10,prodetailISBN13, prodetailISBN10, wmspISBN13, wmspISBN10, wmspdimen, wmspgender, wmspsize, upc, swatchdetails,swatchformat, hprice, imageurl, screenshot_path, wmoccasion, wmringstyle, wmgemstonetype, wmstyle, wmcarats, wmgemstonecut, wmkarats, wmfinefashion, wmtheme, wmbirthstone, wmgemstoneshape ,wmcountryorigin, wmfeatures, wmsleevelength, wmneckstyle, wmpattern, wmfabriccontent, wmclothingsize, wmmoviegenre, wmtargetaudience, wmedition, wmactors, wmduration, wmstudioproductioncompany, wmcharacter, wmdirector, wmreleasedate, wmsptitle, wmlanguage, wmseriestitle, wmtreleasedate, wmpublisher, wmpublicationdate, wmperformer, wmrecordlabel, wmpmediaformat, wmtracklist, wmmusicgenre, wmagegroup, prodetduration, titleepisodes, titleseasons, titlevolumes, prodetepisodes, prodetseasons, prodetvolumes, wmtiresize, wmvehicletype, wmtirewidth, wmwheeldiameter, wmtirespeedrating,wmutqg, wmtiretractionrating,wmtiretreadwearrating,wmtireseason,wmtreaddepth,prodettiresize, prodetloadrange, titletiresize, titleloadrange, sold , wmvideogameplatform,wmgenre,wmvideogamecollection,wmharddrivecapacity,wminternalorextrenal,wmesrbrating,wmiscordless,wmcompatibledevice,wmcompatiblebrands, prodetplatform ,titleplatform, wmprocessortype,wmos,wmprocessorspeed,wmwirelesstech,wmrammemory,wmscreensize,wmprocessorbrand,prodetos,prodetvolts,prodetnetwork,prodetcolor,swatchcolor,titlecolor,prodetsize,swatchsize,prodetresolution,prodetitemtype = AttributeExtraction(url_lines)

        wmid = url_lines[1]
        tooldate = datetime.now().strftime("%Y-%m-%d")
        tooltime = datetime.now().strftime("%H:%M:%S")
        url = url_lines[3]
        batch_id = url_lines[2]
        pgproblem = pgproblem
        itemid = itemid
        breadcrumb = breadcrumb
        wmtitbrand = wmtitbrand
        wmtitle = wmtitle
        wmprice = wmprice
        wmdes = wmdes
        wmspbrand = wmspbrand
        wmspcolor = wmspcolor
        wmspformat = wmspformat
        wmspmanuf = wmspmanuf
        wmsppartno = wmsppartno
        wmspmodel = wmspmodel
        wmsppack = wmsppack
        wmspshape = wmspshape
        wmpagecount = wmpagecount
        wmspISBN13 = wmspISBN13
        wmspISBN10 = wmspISBN10
        wmspdimen = wmspdimen
        wmspgender = wmspgender
        wmspsize = wmspsize
        upc = upc
        swatchdetails = swatchdetails
        swatchformat = swatchformat
        hprice = hprice
        imageurl = imageurl
        titleISBN13 = titleISBN13
        titleISBN10 = titleISBN10
        prodetailISBN13 = prodetailISBN13
        prodetailISBN10 = prodetailISBN10
        titleformat = titleformat
        prodetformat = prodetformat
        wmcondition = wmcondition
        wmoccasion = wmoccasion
        wmgemstonetype = wmgemstonetype
        wmringstyle = wmringstyle
        wmstyle = wmstyle
        wmcarats = wmcarats
        wmgemstonecut = wmgemstonecut
        wmkarats = wmkarats
        wmfinefashion = wmfinefashion
        wmtheme = wmtheme
        wmbirthstone = wmbirthstone
        wmgemstoneshape = wmgemstoneshape
        wmcountryorigin = wmcountryorigin
        wmclothingsize = wmclothingsize
        wmfeatures = wmfeatures
        wmsleevelength = wmsleevelength
        wmneckstyle = wmneckstyle
        wmpattern = wmpattern
        wmfabriccontent = wmfabriccontent
        wmmoviegenre = wmmoviegenre
        wmtargetaudience = wmtargetaudience
        wmedition = wmedition
        wmactors = wmactors
        wmduration = wmduration
        wmstudioproductioncompany = wmstudioproductioncompany
        wmcharacter = wmcharacter
        wmdirector = wmdirector
        wmreleasedate = wmreleasedate
        wmsptitle = wmsptitle
        wmlanguage = wmlanguage
        wmseriestitle =wmseriestitle
        wmtreleasedate = wmtreleasedate
        wmpublisher = wmpublisher
        wmpublicationdate = wmpublicationdate
        wmperformer = wmperformer
        wmrecordlabel = wmrecordlabel
        wmpmediaformat = wmpmediaformat
        wmtracklist = wmtracklist
        wmmusicgenre = wmmoviegenre
        wmagegroup = wmagegroup
        prodetduration = prodetduration
        titleepisodes = titleepisodes
        titleseasons = titleseasons
        titlevolumes = titlevolumes
        prodetepisodes = prodetepisodes
        prodetseasons = prodetseasons
        prodetvolumes = prodetvolumes
        wmtiresize = wmtiresize
        prodettiresize = prodettiresize
        prodetloadrange = prodetloadrange
        titletiresize = titletiresize
        titleloadrange = titleloadrange
        wmtirespeedrating = wmtirespeedrating
        wmvehicletype = wmvehicletype
        wmtirewidth = wmtirewidth
        wmwheeldiameter = wmwheeldiameter
        wmtirespeedrating = wmtirespeedrating
        wmutqg = wmutqg
        wmtiretractionrating = wmtiretractionrating
        wmtiretreadwearrating = wmtiretreadwearrating
        wmtireseason = wmtireseason
        wmtreaddepth = wmtreaddepth
        sold = sold
        wmvideogameplatform = wmvideogameplatform
        wmgenre = wmgenre
        wmvideogamecollection = wmvideogamecollection
        wmharddrivecapacity = wmharddrivecapacity
        wminternalorextrenal = wminternalorextrenal
        wmesrbrating = wmesrbrating
        wmiscordless = wmiscordless
        wmcompatibledevice = wmcompatibledevice
        wmcompatiblebrands = wmcompatiblebrands
        prodetplatform = prodetplatform
        titleplatform = titleplatform
        wmprocessortype = wmprocessortype
        wmos = wmos
        wmprocessorspeed = wmprocessorspeed
        wmwirelesstech = wmwirelesstech
        wmrammemory = wmrammemory
        wmscreensize = wmscreensize
        wmprocessorbrand = wmprocessorbrand
        prodetos = prodetos
        prodetvolts = prodetvolts
        prodetnetwork = prodetnetwork
        prodetcolor = prodetcolor
        swatchcolor = swatchcolor
        titlecolor = titlecolor
        prodetsize = prodetsize
        swatchsize = swatchsize
        prodetresolution = prodetresolution
        prodetitemtype = prodetitemtype
        
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
        
        cursor.execute('INSERT INTO "MIA_AE_WM_Out" (WM_Record_ID,Tool_Date,Tool_Time,Batch_ID,WM_URL,URL_Status,Item_ID,Breadcrumb,Brand_Title,Title,Price,Description,Title_Format,Prodetails_Format,Brand,Color,Format_Type,Manufacturer,Part_No,Model,Count_Per_Pack,Shape,Condition,Page_Count,Title_ISBN_13,Title_ISBN_10,Prodetails_ISBN_13,Prodetails_ISBN_10,ISBN_13,ISBN_10,Assembled_Product_Dimensions_LxWxH,Gender,Size,UPC,Swatch_Detail,Swatch_Format,Swatch_Price,Image_URL,Screenshot_Path,Occasion,Ring_Style,Gemstone_Type,Style,Carats,Gemstone_Cut,Karats,Fine_or_Fashion,Theme,Birthstone,Gemstone_Shape,Country_of_Origin_Textiles,Features,Sleeve_Length_Style,Clothing_Neck_Style,Pattern,Fabric_Content,Clothing_Size,Movie_Genre,Target_Audience,Edition,Actors,Duration,Studio_Production_Company,Character,Director,Release_Date,Sp_Title,Language,Series_Title,Theatrical_Release_Date,Publisher,Publication_Date,Performer,Record_Label,Physical_Media_Format,Track_Listing,Music_Genre,Age_Group,Productdetail_Duration,Title_Episodes ,Title_Seasons ,Title_Volumes,Prodet_Episodes ,Prodet_Seasons,Prodet_Volumes,Tire_Size,Vehicle_Type,Tire_Width,Wheel_Diameter,Tire_Speed_Rating,Uniform_Tire_Quality_Grade,Tire_Traction_Rating,Tire_Treadwear_Rating,Tire_Season,Tread_Depth,Prodet_Tire_Size,Prodet_Load_Range,Title_Tire_Size,Title_Load_Range,Sold_And_Shipped_By,Video_Game_Platform,Genre,Video_Game_Collection,Hard_Drive_Capacity,Internal_External,ESRB_Rating,Is_Cordless,Compatible_Devices,Compatible_Brands,Prodet_Compatible_Platform,Title_Platform,Processor_Type,Operating_System,Processor_Speed,Wireless_Technology,RAM_Memory,Screen_Size,Processor_Brand,Prodet_OS,Prodet_Volts,Prodet_Network,ProductDetail_Color,Swatch_Color,Title_Color,ProductDetail_ClothingSize,Swatch_Size,Prodet_Resolution,Prodet_Itemtype)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                        (wmid, tooldate, tooltime, batch_id, url, pgproblem,itemid, breadcrumb,
                         wmtitbrand, wmtitle, wmprice, wmdes, titleformat, prodetformat, wmspbrand, wmspcolor, wmspformat, wmspmanuf,
                         wmsppartno, wmspmodel, wmsppack, wmspshape, wmcondition, wmpagecount, titleISBN13, titleISBN10,
                         prodetailISBN13, prodetailISBN10, wmspISBN13, wmspISBN10, wmspdimen, wmspgender, wmspsize, upc, swatchdetails,
                         swatchformat, hprice, imageurl,screenshot_path, wmoccasion, wmringstyle, wmgemstonetype, wmstyle, wmcarats, 
                         wmgemstonecut, wmkarats, wmfinefashion, wmtheme, wmbirthstone, wmgemstoneshape, wmcountryorigin, wmfeatures, 
                         wmsleevelength, wmneckstyle, wmpattern, wmfabriccontent, wmclothingsize,wmmoviegenre, wmtargetaudience, wmedition, 
                         wmactors, wmduration, wmstudioproductioncompany, wmcharacter, wmdirector, wmreleasedate, wmsptitle, wmlanguage, 
                         wmseriestitle, wmtreleasedate, wmpublisher, wmpublicationdate, wmperformer, wmrecordlabel, wmpmediaformat, 
                         wmtracklist, wmmusicgenre, wmagegroup, prodetduration, titleepisodes, titleseasons, titlevolumes, prodetepisodes, 
                         prodetseasons, prodetvolumes,wmtiresize, wmvehicletype, wmtirewidth, wmwheeldiameter, wmtirespeedrating,
                         wmutqg, wmtiretractionrating,wmtiretreadwearrating,wmtireseason,wmtreaddepth,prodettiresize, prodetloadrange,
                         titletiresize, titleloadrange, sold,wmvideogameplatform,wmgenre,wmvideogamecollection,wmharddrivecapacity,wminternalorextrenal,wmesrbrating,wmiscordless,
                         wmcompatibledevice,wmcompatiblebrands,prodetplatform, titleplatform,wmprocessortype,wmos,
                         wmprocessorspeed,wmwirelesstech,wmrammemory,wmscreensize,wmprocessorbrand,prodetos,prodetvolts,
                         prodetnetwork,prodetcolor,swatchcolor,titlecolor,prodetsize,swatchsize,prodetresolution,prodetitemtype))
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
