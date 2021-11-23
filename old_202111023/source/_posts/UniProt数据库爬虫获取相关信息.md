---
title: UniProt数据库爬虫获取相关信息
tags: Python
categories: Python
abbrlink: 41af5d00
date: 2021-04-18 22:02:11
---

最近在分析转录组，基因组是自己组装的，好多基因注释不到KEGG和GO这两个数据库，就索性先把基因蛋白blast到SwissProt数据库，然后得到比对的蛋白的ID，再经过筛选后再去看蛋白相关的GO term。但是，这么多基因我也不可能一个一个查啊，那就Python爬虫吧。

<!-- more -->

```python
import os
import random
import openpyxl
import csv
import time
import requests
from bs4 import BeautifulSoup
import re

os.chdir('C:/Users/Administrator/Desktop')

with open('temp.txt','r') as f:
    for line in f:
        acuce_gene_id = line.split('\t')[1].split('.')[0]
        acuce_prot_id = line.split('\t')[1]
        match_uniprot_id = line.split('\t')[2]
        uniprot_link = 'https://www.uniprot.org/uniprot/' + match_uniprot_id.split('.')[0]

        #print(acuce_gene_id)
        #print(acuce_prot_id)
        #print(match_uniprot_id)
        #print(uniprot_link)
        #print('----------------------------------------------------')

        res = requests.get(uniprot_link)

        soup = BeautifulSoup(res.text,'html.parser')

        organism = soup.find('div',id = 'content-organism', class_ = 'entry-overview-content').get_text()
        gene = soup.find('div',id = 'content-gene', class_ = 'entry-overview-content').get_text()
        protein = soup.find('div',id = 'content-protein', class_ = 'entry-overview-content').get_text()
        res_temp = {'Q9UUH7':[organism,gene,protein]}

        function = soup.find('div', class_ = 'annotation').find('span').get_text().replace('By similarity','')

        go_mol = soup.find('ul', class_ = 'noNumbering molecular_function') 
        if str(type(go_mol)) != "<class 'NoneType'>":
            for i in go_mol.find_all('a'):
                link = i['href']
                link_split = link.split('/')
                go_item_id = link_split[len(link_split)-1]
                if go_item_id.split(':')[0] != 'GO':
                    continue
                else:
                    go_item = i.get_text()

                    res_excel = openpyxl.Workbook()
                    sheet = res_excel.active
                    sheet.title = '爬虫结果'
                    col_name = ['月亮谷基因编号','月亮谷转录本编号','匹配的UniProt编号','蛋白名称','物种','基因','功能','GO ID','GO Description','Link']
                    sheet.append(col_name)
                    res_new = [acuce_gene_id,acuce_prot_id,match_uniprot_id,protein,organism,gene,function,go_item_id,go_item_id,link]
                    #print(res_new)
                    sheet.append(res_new)
                    file_name = os.getcwd() + '/results/' + 'GO_Biological_process_' + acuce_prot_id + '_' + match_uniprot_id + '_' +go_item_id.replace(':','_') + '.xlsx'
                    res_excel.save(file_name)

        go_bio = soup.find('ul', class_ = 'noNumbering biological_process') 
        if str(type(go_bio)) != "<class 'NoneType'>":
            for i in go_bio.find_all('li'):
                link = i.find('a')['href']
                link_split = link.split('/')
                go_item_id = link_split[len(link_split)-1]
                
                if go_item_id.split(':')[0] != 'GO':
                    continue
                else:
                    go_item = i.find('a').get_text()

                    res_excel = openpyxl.Workbook()
                    sheet = res_excel.active
                    sheet.title = '爬虫结果'
                    col_name = ['月亮谷基因编号','月亮谷转录本编号','匹配的UniProt编号','蛋白名称','物种','基因','功能','GO ID','GO Description','Link']
                    sheet.append(col_name)
                    res_new = [acuce_gene_id,acuce_prot_id,match_uniprot_id,protein,organism,gene,function,go_item_id,go_item,link]
                    #print(res_new)
                    sheet.append(res_new)
                    file_name = os.getcwd() + '/results/' + 'GO_Biological_process_' + acuce_prot_id + '_' + match_uniprot_id + '_' +go_item_id.replace(':','_') + '.xlsx'
                    res_excel.save(file_name)
```

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com