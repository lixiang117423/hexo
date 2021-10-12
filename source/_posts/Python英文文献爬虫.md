---
title: Python英文文献爬虫
tags: Python
categories: Python
abbrlink: 926c2b5a
date: 2020-01-12 15:27:11
---

之前写过用Python爬取中文文献，但是更多时候需要的是英文文献，就写了个英文的爬虫代码。

<!-- more -->

```python
import os
import random
import openpyxl
import time
import requests
from bs4 import BeautifulSoup
import re

time_start = time.time()
header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

user_key_words = input('请输入你的关键词(空格分隔)：')
user_key_words = user_key_words.replace(' ','%20')
url_1 = 'http://xueshu.baidu.com/s?wd='
url_2 = '&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1'

url_0 = url_1 + user_key_words +  '&pn=' + str(0) + url_2
res = requests.get(url_0, headers=header)
soup = BeautifulSoup(res.text, 'html.parser')
num = re.findall('\d{1,20}', soup.find('span',class_='nums').text.replace(',',''))[0]

print('找到约%s条相关结果'%(num))

for i in range(0,int(num),10):
    print(i)
    url = url_1 + user_key_words +  '&pn=' + str(i) + url_2
    res = requests.get(url, headers=header)

    title_link_result = openpyxl.Workbook()
    sheet = title_link_result.active
    sheet.title = '百度学术文献爬取'
    col_name = ['title','key_words','year','ref_wr','author','abstract','doi','doi_url','journal']
    sheet.append(col_name)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.find_all('div', class_='sc_content')
        for item in items:
            url_temp = item.find('h3').find('a')['href']
            res_final = requests.get(url_temp, headers=header)
            soup_final = BeautifulSoup(res_final.text, 'html.parser')
            main_info = soup_final.find('div', class_='main-info')
            try:
                title = main_info.find('h3').text.replace('\n','')
                title = re.sub(' ','', title, 8)
            except AttributeError:
                title = 'None'
            try:
                author = main_info.find('div', class_='author_wr').find('p',class_='author_text').find('a').text
            except AttributeError:
                author = 'None'
            
            try:
                abstract = main_info.find('div',class_='abstract_wr').find('p',class_='abstract').text
            except AttributeError:
                abstract = 'None'

            try:
                key_temp = main_info.find('div',class_='kw_wr').find('p',class_='kw_main').find_all('a')
                key_words = ''
                for key in key_temp:
                    key_words = key_words + ',' + key.text
            except AttributeError:
                key_words = 'None'

            try:
                doi = main_info.find('div',class_='doi_wr').find('p', class_='kw_main').text.replace(' ','')
            except AttributeError:
                doi = 'None'

            doi_url = ("https://doi.org/" + doi).replace('\n','')

            try:
                ref_wr = main_info.find('div', class_='ref_wr').find('a',class_='sc_cite_cont').text.replace(' ','')
            except AttributeError:
                ref_wr = 'None'

            try:
                year = main_info.find('div', class_='year_wr').find('p',class_='kw_main').text.replace(' ','')
            except AttributeError:
                yeay = 'None'

            try:
                journal = soup_final.find('div',class_='dtl_r_item').find('div', class_='container_right').find('a', class_='journal_title').text.replace('《','').replace('》','')
            except AttributeError:
                journal = "None"
        
            sheet.append([title,key_words,year,ref_wr,author,abstract,doi,doi_url,journal])
        file_name = 'D:\!01\git\Python\Python爬取英文文献\\results\第'+str((i+10)/10).replace('.0','') + '页.xlsx'
        title_link_result.save(file_name)

    else:
        print('Something is wrong! Please check!')

    time_end = time.time()
    
    print('已经完成第'+str((i+10)/10).replace('.0','') + '页爬取，耗时：%s'%(time_end-time_start) + '，休息10s继续爬取！')
    time.sleep(10)
```

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
