---
title: Python爬取水稻基因的Entrez ID
tags: Python
categories: Python
abbrlink: 61374b33
date: 2021-03-28 16:44:04
---

海外服务器爬NCBI是真的香！！！<!-- more -->

大概有25000个基因，用R包做KEGG和GO的时候需要把基因ID转换成ENTREZID，显然一个一个查找是不现实的，那就爬虫吧。

国内网络的话单次爬取500个左右就会断，索性部署到阿里云新加坡的服务器上去，爬取12000+了依旧没有断线，继续分析数据等它爬完。

```R
import os
import random
import openpyxl
import csv
import time
import requests
from bs4 import BeautifulSoup
import re

# os.chdir('C:/Users/Administrator/Desktop')
os.chdir(os.getcwd())

symbol_id = open('rice.SYMBOL.csv','r')
read_id = csv.reader(symbol_id)

url_list = []

for i in read_id:
    order = i[0]
    symbol = i[1]
    url = 'https://www.ncbi.nlm.nih.gov/gene/?term=' + i[1]

    url_temp = [order, symbol, url]

    url_list.append(url_temp)


for i in url_list[10388:len(url_list)]:
    #print(i[0] + '---' + i[1])
    #print(i[1])
    
    res = requests.get(i[2])
    #print(res.status_code)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text,'html.parser')
        entrezid = soup.find_all('span',class_ = 'geneid')

        if len(entrezid) != 0:
            entrezid = soup.find_all('span',class_ = 'geneid')[0].get_text().split(',')[0].split(': ')[1]
            res_excel = openpyxl.Workbook()
            sheet = res_excel.active
            sheet.title = 'rice gene ENTREZID'
            col_name = ['SYMBOL','ENTREZID']
            sheet.append(col_name)
            res_now = [i[1],entrezid]
            sheet.append(res_now)

            file_name = os.getcwd() + '/results/' + i[1] + '-entrezid.xlsx'
            res_excel.save(file_name)

            print(i[0] + '---' + i[1] + '---' + entrezid)

        else:
            print(i[0] + '---' + i[1] + '---' + 'NO entrezid')
            continue
    else:
        print(i[0] + '---' + i[1] + '---' + 'Failed')
        continue

    time.sleep(0)
```

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com