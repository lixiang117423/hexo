---
title: Python 爬取知乎问题 即将步入研究生，有什么忠告？ 所有回答后将数据写入 Excel 并生成.html 文件
date: 2020-01-07 18:53:40
tags: Python
categories: Python
---

学Python爬虫一周多，今天练练手，爬取了一个自己感兴趣的知乎话题[即将步入研究生，有什么忠告？](https://www.zhihu.com/question/64270965)。一共是272个答案，本次爬取的目的是爬取到所有回答者的昵称、个性签名、赞同数以及具体的内容。

<!-- more -->

先检查一波：
{% asset_img 1.png %}
我天真地以为全部都在“Elements”这个页面里面，DuangDuangDuang一阵代码。呵呵，太天真了。
既然在“Elements”没有，那就一定是带参数请求数据的。
那看看“Network”下的“XHR”，每次下拉出现新的内容，总是会有个“answers?...”的东西，直觉告诉我应该就是这个鬼东西了。看看吧：
{% asset_img 2.png %}

{% asset_img 3.png %}

{% asset_img 4.png %}

**完犊子了，完全没规律啊！！！！！！**
这种大网站是不可能没有规律的，再看看、、、、、、

{% asset_img 5.png %}

{% asset_img 6.png %}



果然，第3个“answers?...”开始就有规律了，“limit”始终是5，“offset”依次叠加5。
针对前两个，两次代码，之后剩下的，一个大的for循环搞定（前两个是可以不用for循环的，但是为了后面的for循环，就索性都用了）。

代码如下：
```
# 载入相应的模块
import time
import requests
import openpyxl

time1 = time.time()

lists = []
lists.append(['answer_kname','headline','voteup_count','content'])

##################
for i in range(0,1,1):
    url = 'https://www.zhihu.com/api/v4/questions/64270965/answers'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    params = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
        'offset': str(i),
        'limit': '3',
        'sort_by': 'default',
        'platform': 'desktop'
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()
    items = res_json['data']
    for item in items:
        answer_kname = item['author']['name']
        headline = item['author']['headline']
        content = item['content']
        voteup_count = item['voteup_count']

        lists.append([answer_kname,headline,voteup_count,content])

##################
for i in range(3,3,1):
    url = 'https://www.zhihu.com/api/v4/questions/64270965/answers'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    params = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
        'offset': str(i),
        'limit': '5',
        'sort_by': 'default',
        'platform': 'desktop'
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()
    items = res_json['data']
    for item in items:
        answer_kname = item['author']['name']
        headline = item['author']['headline']
        content = item['content']
        voteup_count = item['voteup_count']

        lists.append([answer_kname,headline,voteup_count,content])

##################
for i in range(8,278,5):
    url = 'https://www.zhihu.com/api/v4/questions/64270965/answers'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    params = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
        'offset': str(i),
        'limit': '5',
        'sort_by': 'default',
        'platform': 'desktop'
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()
    items = res_json['data']
    for item in items:
        answer_kname = item['author']['name']
        headline = item['author']['headline']
        content = item['content']
        voteup_count = item['voteup_count']

        lists.append([answer_kname,headline,voteup_count,content])


##################
file = openpyxl.Workbook()
sheet = file.active
sheet.title = 'answers'
for i in lists:
    sheet.append(i)

file.save('即将步入研究生，有什么忠告.xlsx')

##################
file_html = open('知乎：即将步入研究生，有什么忠告.html','w',encoding= 'utf-8')

for i in lists:
    file_html.write(i[3])
file_html.close()

##################
time2 = time.time()
print('爬虫耗时：%.3f'%(float(time2-time1)),'秒')

```

附件：
1. [代码](https://github.com/GitHub-LiXiang/Python/blob/master/%E7%88%AC%E8%99%AB/%E7%9F%A5%E4%B9%8E%E8%AF%9D%E9%A2%98%EF%BC%9A%E5%8D%B3%E5%B0%86%E6%AD%A5%E5%85%A5%E7%A0%94%E7%A9%B6%E7%94%9F%EF%BC%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%BF%A0%E5%91%8A/%E5%8D%B3%E5%B0%86%E6%AD%A5%E5%85%A5%E7%A0%94%E7%A9%B6%E7%94%9F%EF%BC%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%BF%A0%E5%91%8A.py)
2. [即将步入研究生，有什么忠告.xlsx](https://github.com/GitHub-LiXiang/Python/blob/master/%E7%88%AC%E8%99%AB/%E7%9F%A5%E4%B9%8E%E8%AF%9D%E9%A2%98%EF%BC%9A%E5%8D%B3%E5%B0%86%E6%AD%A5%E5%85%A5%E7%A0%94%E7%A9%B6%E7%94%9F%EF%BC%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%BF%A0%E5%91%8A/%E5%8D%B3%E5%B0%86%E6%AD%A5%E5%85%A5%E7%A0%94%E7%A9%B6%E7%94%9F%EF%BC%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%BF%A0%E5%91%8A.xlsx)
3. [知乎：即将步入研究生，有什么忠告.html](https://github.com/GitHub-LiXiang/Python/blob/master/%E7%88%AC%E8%99%AB/%E7%9F%A5%E4%B9%8E%E8%AF%9D%E9%A2%98%EF%BC%9A%E5%8D%B3%E5%B0%86%E6%AD%A5%E5%85%A5%E7%A0%94%E7%A9%B6%E7%94%9F%EF%BC%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%BF%A0%E5%91%8A/%E7%9F%A5%E4%B9%8E%EF%BC%9A%E5%8D%B3%E5%B0%86%E6%AD%A5%E5%85%A5%E7%A0%94%E7%A9%B6%E7%94%9F%EF%BC%8C%E6%9C%89%E4%BB%80%E4%B9%88%E5%BF%A0%E5%91%8A.html)

---

💌lixiang117423@gmail.com

💌lixiang117423@foxmail.com