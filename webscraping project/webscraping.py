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
# Create an new Excel file and add a worksheet.

###### HTML resource: https://developer.mozilla.org/en-US/docs/Web/HTML/Element

f=open("url.csv",'w')
print(test, file=f)
f.close()
    
for url in test:
    res_all = requests.get(url)
    soup = bs4.BeautifulSoup(res_all.text,'lxml')
    
    workbook = xlsxwriter.Workbook(url.split("/")[2]+'.xlsx')
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
                
    workbook.close()
        

