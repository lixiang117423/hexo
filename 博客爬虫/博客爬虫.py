import os
import random
import openpyxl
import time
import requests
from bs4 import BeautifulSoup
import re

results = []

title_link_result = openpyxl.Workbook()
sheet = title_link_result.active
sheet.title = '博客文章链接爬取'
col_name = ['博客标题','博客链接']
sheet.append(col_name)

url = 'https://www.blog4xiang.world/page/2/'

for i in range(1,11):
  if i==1:
    url = 'https://www.blog4xiang.world'
  else:
    url = 'https://www.blog4xiang.world/page/' + str(i) + '/'
  
  res = requests.get(url)

  res.encoding = "utf-8"
  
  soup = BeautifulSoup(res.text, 'html.parser')

  items = soup.find_all('a',class_='post-title-link')

  for j in items:
    link = 'https://www.blog4xiang.world' + j['href']
    sheet.append([j.text,link])
  
title_link_result.save('根系分泌物CNKI文献链接_break.xlsx')
  
  
