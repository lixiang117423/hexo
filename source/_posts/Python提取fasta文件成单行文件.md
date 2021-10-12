---
title: Python提取fasta文件成单行文件
tags: Python
categories: Python
abbrlink: 7136a0b7
date: 2021-04-07 10:18:35
---

`R`语言对`fasta`这种超大的字符文件进行处理真的是太慢了，`Python`是真的香啊！<!-- more -->

```python
import os
import time

start = time.time()

os.chdir('C:/Users/Administrator/Desktop/')
print(os.getcwd())

res_dict = {}

with open('ylg.protein.pep','r') as pep:
    for line in pep:
        if line.startswith('>'):
            name = line.strip().split()[0]
            res_dict[name] = ''
        else:
            res_dict[name] += line.replace('\n','')

print(len(res_dict))

for cds_id, sequence in res_dict.items():
    #print(cds_id)
    #print(sequence)
    #time.sleep(2)
    with open('pep.seq.txt', 'a') as file:
        file.write(cds_id.replace('>','') + "\t" + sequence + "\n")

end = time.time()
print(end - start)
```

4万多个基于32万多行，耗时5.12s。和`R`相比真的是很快了。

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com