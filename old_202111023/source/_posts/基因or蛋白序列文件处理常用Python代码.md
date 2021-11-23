---
title: 基因or蛋白序列文件处理常用Python代码
tags: Python
categories: Python
abbrlink: c13c3eb8
date: 2021-04-21 10:22:41
---

序列转换成fasta文件及后续的SwissProt数据库爬虫代码。<!-- more -->

Excel格式序列转换成fasta格式文件：

```python
import os

os.chdir('C:/Users/Administrator/Desktop/')

res = open('植物病原互作通路基因fasta文件.fasta','w+')

original_file = open('植物病原互作通路_查询结果.txt','r')

for line in original_file.readlines()[1:]:
    gene = '>' + line.split(' ')[0]
    pro = line.split(' ')[5].split('\n')[0]
    res.writelines([gene,'\n',pro,'\n'])

res.close()
```

将比对到SwissProt数据库的结果进行爬虫：

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

res = open('植物病原互作通路基因蛋白爬取swiss数据库结果.txt','w+',encoding = "utf-8")

original_file = open('植物病原互作通路基因蛋白swiss数据库blast结果.txt','r')

for line in original_file.readlines()[0:]:
    gene = line.split('\t')[0]
    pro = line.split('\t')[1]
    pro_id = pro.split('.')[0]
    similarity = line.split('\t')[2]
    
    if float(similarity) >= 70:
        evalue = line.split('\t')[10]
        score = line.split('\t')[11].replace('\n','')

        spider_link = 'https://www.uniprot.org/uniprot/' + pro_id

        res_spider = requests.get(spider_link)

        soup = BeautifulSoup(res_spider.text,'html.parser')

        organism = soup.find('div',id = 'content-organism', class_ = 'entry-overview-content').get_text()
        gene_1 = soup.find('div',id = 'content-gene', class_ = 'entry-overview-content').get_text()
        protein = soup.find('div',id = 'content-protein', class_ = 'entry-overview-content').get_text()
        
        status = soup.find('div', id = 'content-status',class_ = 'entry-overview-content').find('span', class_ = 'context-help tooltipped-click').get_text()
        res_str = re.findall('<p>(.*?)</p>',status)
        status = status.replace(res_str[0],'').replace('\n','.').replace('                                    <p></p>','').replace('-','').replace('leveli','level')

        if False:
            try:
                function = soup.find('div', class_ = 'annotation').find('span').get_text().replace('By similarity','')
            except AttributeError:
                function = 'None'

        res.writelines([gene,'\t',pro,'\t',similarity,'\t',evalue,'\t',score,'\t',organism,'\t',gene_1,'\t',protein,'\t',status,'\n'])
    else:
        next

res.close()
```

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com

