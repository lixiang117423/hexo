---
title: 分类-回归树(CART)在R语言中的实现
tags: R语言
categories: R语言
abbrlink: dca5ae94
date: 2020-12-22 15:36:07
---

**CART 模型** ，即 Classification And Regression Trees。它和一般回归分析类似，是用来对变量进行解释和预测的工具，也是数据挖掘中的一种常用算法。如果因变量是连续数据，相对应的分析称为回归树，如果因变量是分类数据，则相应的分析称为分类树。

<!-- more -->

```R
rm(list = ls())

library(rpart) 
library(maptree)
library(TH.data)
library(tidyverse)

# load data
df = data.table::fread('df.csv', header = T, encoding = 'UTF-8')

colnames(df)

# for Taxa_S
df_1 = df[,-c(2,3)]
formula_1 = Taxa_S ~.
fit_1 = rpart(formula_1, method='anova', data = df_1)
pfit_1=prune(fit_1,cp= fit_1$cptable[which.min(fit_1$cptable [,"xerror"]),"CP"]) 
pdf(file = 'Taxa_S.回归树.pdf', width = 8, height = 5,family="GB1")
draw.tree(fit_1,digits = 2) 
dev.off()

printcp(fit_1) %>% as.data.frame() %>%
  write.csv(file = 'Taxa_S结果.csv', row.names = FALSE)


# for Individuals
df_2 = df[,-c(1,3)]
formula_2 = Individuals ~.
fit_2 = rpart(formula_2, method='anova', data = df_2)
pfit_2=prune(fit_2,cp= fit_2$cptable[which.min (fit_2$cptable [,"xerror"]),"CP"]) 

pdf(file = 'Individuals.回归树.pdf', width = 8, height = 5,family="GB1")
draw.tree(fit_2,digits = 2) 
dev.off()

printcp(fit_2) %>% as.data.frame() %>%
  write.csv(file = 'Individuals结果.csv', row.names = FALSE)


# for Chao_1
df_3 = df[,-c(1,2)]
formula_3 = Chao_1 ~.
fit_3 = rpart(formula_3, method='anova', data = df_3)
pfit_3=prune(fit_3,cp= fit_3$cptable[which.min(fit_3$cptable [,"xerror"]),"CP"]) 

pdf(file = 'Chao_1.回归树.pdf', width = 8, height = 5,family="GB1")
draw.tree(fit_3,digits = 2) 
dev.off()

printcp(fit_3) %>% as.data.frame() %>%
  write.csv(file = 'Chao_1结果.csv', row.names = FALSE)
```

{% asset_img 1.png %}

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

