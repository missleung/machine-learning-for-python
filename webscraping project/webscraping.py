#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 20:10:10 2019

@author: lisa
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 19:31:46 2019

@author: lisa
"""

# Scraping raw data from google search an outputing landing pages

########## #trying googlesearch... this only prints out the urls

import requests
import bs4
from googlesearch import search
test_search = search('landing page', stop=4)
test = list(test_search)

import xlsxwriter
import re
import urllib
import pandas as pd
import os
# Create an new Excel file and add a worksheet.

###### HTML resource: https://developer.mozilla.org/en-US/docs/Web/HTML/Element
wd = "/Users/lisa/machine-learning-for-python/webscraping project/"
wd_raw = "/Users/lisa/machine-learning-for-python/webscraping project/raw data/"

f=open(wd+"url_testing.csv",'w')
print(test, file=f)
f.close()
    
def write_html_to_xlsx(set_of_urls, url_tag, wd):
    for url in set_of_urls:
        res_all = requests.get(url)
        soup = bs4.BeautifulSoup(res_all.text,'lxml')
    
        workbook = xlsxwriter.Workbook(wd+url.split("/")[2]+"_"+url_tag+'.xlsx')
        worksheet = workbook.add_worksheet("full_html")
        worksheet.write(0,0,str(soup))
    
        # all tag names
        all_tags = list(set([tag.name for tag in soup.find_all()]))
        for i in all_tags:
            res_tag = soup.find_all(i)
            i = re.sub(":","-",i)
            worksheet = workbook.add_worksheet(i)
            row_ind=0
            for row in res_tag:
                worksheet.write(row_ind,0,str(row))
                row_ind += 1
                
            
        # getting urls only from link tags 
        href_urls = soup.find_all("a",attrs={'href': re.compile("^http://")})
        worksheet = workbook.add_worksheet("href_urls")
        row_ind=0
        for i in href_urls:
            worksheet.write(row_ind,0,str(i.get('href')))
            row_ind += 1            
        
        workbook.close()
     
# Getting the html from direct landing page on google
write_html_to_xlsx(test, "main", wd_raw)

# Looping html from href links through direct landing page
main_excel_files = os.listdir(wd_raw)
main_excel_files = pd.Series(main_excel_files)
main_excel_files = main_excel_files[main_excel_files.str.contains('xlsx')]

for i in main_excel_files:
    sub_urls = pd.read_excel(wd_raw+i, sheet_name = "href_urls")
    
    # Looping href links and saving those as well
    for j

