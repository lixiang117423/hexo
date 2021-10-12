---
title: PCA和PERMANOVA分析
categories: R语言
tags: R语言
abbrlink: 76358c9
date: 2020-01-07 12:32:15
---

PCA这种图，图片上看起来不同的组别之间是有差异的，比如说这个：

<!-- more -->

{% asset_img 1.png %}

可是各组别之间到底有没有显著的差异呢？普通的ANOVA行不行？就16s的数据来说，一般是有几千个OTU，普通的ANOVA根本就是无能为力啊。
这个时候就需要进行PERMANOVA检验了。PERMANOVA分析(也叫 NPMANOVA、Adonis 分析) 是一种以距离矩阵为对象的多元方差分析。
下面的代码包括了PCA和PERMANOVA的整个分析流程。

```R
rm(list = ls())

library(dplyr)
library(ggplot2)
library(vegan)

data = read.table('data/otu.txt',header = T, row.names = 1) %>%
  t() %>%
  as.data.frame() %>%
  mutate(group = rep(c('AAS','ANS','NAS','NNS'),each = 3))

pca = prcomp(data[,1:ncol(data)-1],scale. = TRUE)

# 计算原始数据中的每个数据在每个 PC 上的比重
pca.var = pca$sdev^2 

#计算每个 PC 占所有 PC 的和的比列
pca.var.per = round(pca.var/sum(pca.var)*100,2)

# 柱状图显示每个PC所占的比列
data.frame(PC = as.character(paste('PC',1:nrow(data),sep = '')),
           value = pca.var.per) %>%
  ggplot(aes(PC,value))+
  geom_bar(stat = 'identity', fill = 'white', color = 'black')+
  geom_hline(yintercept = pca.var.per[1]*1.1, color = 'white')+
  scale_x_discrete(limits = c(paste('PC',1:nrow(data),sep = '')))+
  theme_classic()+
  scale_y_continuous(expand = c(0,0))+
  geom_text(aes(y = value + 1,label = paste(value,'%',sep = '')),size = 2.5)+
  labs(x = '',y = '',title = 'ScreePlot')+
  theme(axis.text = element_text(size = 11,color = 'black'),
        axis.ticks = element_line(color = 'black'),
        plot.title = element_text(hjust = 0.5))

# ggplot2绘图
as.data.frame(pca$x) %>%
  mutate(group = data$group) %>%
  ggplot(aes(PC1,PC2,color = group))+
  geom_point(size = 2)+
  theme_classic()+
  labs(x = paste('PC1(',pca.var.per[1],'%)',sep = ''),
       y = paste('PC2(',pca.var.per[2],'%)',sep = ''))+
  stat_ellipse(level = 0.68)+
  theme(axis.text = element_text(size = 11,color = 'black'),
        axis.ticks = element_line(color = 'black'),
        plot.title = element_text(hjust = 0.5))

###############################################################
###############################PERMANOVA分析###################
###############################################################
otu = data[,1:ncol(data)-1]

dist = vegdist(otu, method = 'bray') # 计算距离

# 分组信息
site = data.frame(sample = rownames(data),
                  group = data$group)

# PERMANOVA分析
# 整体水平比较
adonis_result_dis = adonis(dist~group, site, permutations = 999)
adonis_result_dis

# 两两比较
group_name = unique(site$group)

result = data.frame()

for (i in 1:(length(group_name) - 1)) {
  for (j in (i + 1):length(group_name)) {
    group_ij = subset(site, group %in% c(as.character(group_name[i]), as.character(group_name[j])))
    otu_ij = otu[group_ij$sample, ]
    adonis_result_otu_ij = adonis(otu_ij~group, group_ij, permutations = 999, distance = 'bray')
    res.temp = as.data.frame(adonis_result_otu_ij$aov.tab)[1,]
    rownames(res.temp) = paste(as.character(group_name[i]),'/',as.character(group_name[j]))
    
    result = rbind(result,res.temp)
  }
}

head(result,nrow(result))
```
最终得到的结果有PCA分析的碎石图、PCA图、PERMANOVA整体分析的结果以及两两比较的结果。

----

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
