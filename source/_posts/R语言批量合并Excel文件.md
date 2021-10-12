---
title: R语言批量合并Excel文件
tags: R语言
categories: R语言
abbrlink: 923787f
date: 2020-01-07 18:55:17
---

离开实验室的时候一个同学在合并他们班的某个汇总表。常规操作，一个一个的复制粘贴的。我就想，这个肯定可以用编程搞定啊，Python或者R都行。回来就 R写了个代码，编了10000个文件用于代码测试。`代码如下`。

<!-- more -->

```R
# 清空当前变量
rm(list = ls())

# 计算程序开始时间
t1 = proc.time()

# 加载数据清洗包
library(tidyverse)

# 提取需要合并的10000个文件名
dirs = dir('test/')[1:10000]

# 查看需要合并的文件综述
dirnum = length(dirs)

# 读取第一个数据转换成空的例表
data_raw = suppressMessages(read_excel(paste('test/',dirs[1],sep = ''),sheet = '高校研究生学生信息录入')[c(6,8),1:23] %>%
                              as.data.frame())

colnames(data_raw) = data_raw[1,]
data_raw = data_raw[-c(1,2),]

# for循环依次读取并合并数据
for (i in dirs) {
  filename = paste('test/',i,sep = '')
  
  data = suppressMessages(read_excel(filename)[c(6,8),1:23] %>%
                            as.data.frame())
  colnames(data) = data[1,]
  data = data[-1,]
  data_raw = rbind(data_raw,data)
  
  if (nrow(data_raw) < dirnum | nrow(data_raw) == dirnum) {
    print(paste('成功合并',nrow(data_raw),'条',sep = ''))
  }
  
  if (nrow(data_raw) == dirnum) {
    write.csv(data_raw, file = 'all_csv.csv')
    print('合并完成！')
  }
}

# 计算程序运行完的时间
print(round(proc.time()-t1,6))

```
---
**康康最后的结果：**
{% asset_img 1.png %}

**155.72秒合并10000个文件！！！**

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
