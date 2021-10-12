---
title: NMDS分析
tags: R语言
categories: R语言
abbrlink: 4e41844f
date: 2021-01-04 12:21:13
---

NMDS（nonmetric multidimensional scaling，非度量多维尺度分析）是排序（ordination）分析一种。排序分析的目的在于寻找数据的连续性（也就是通过连续的排序轴来展示数据的主要趋势）。

<!-- more -->

为什么在微生物（微生态）研究中常用排序分析呢？因为自然生态群落往往是沿着环境梯度呈连续性分布的。

# 为什么要用排序分析

假设现在有这样一组数据：100个样本，100个变量（如基因），那得到的数据就是一个100行×100列的表，也就是100×100=10000维的数据，我（们）能理解（想象）的维度只能到3维，超过3维的数据就很难理解（想象）了。那怎么办呢？既然维度太高我们无法理解，那就把维度降低，降到一维、二维或者三维就能理解了。所以，我理解的排序分析的本质就是降维（个人理解）。

# 排序分析分类

那都有哪些排序分析方法呢？

按照是否”约束“可以分成两类：

- 约束（典范）排序：RDA（冗余分析）、CCA（典范对应分析）、LDA（线性判别分析）等；
- 非约束排序：PCA（主成分分析）、CA对应分析、PCoA（主坐标分析）、NMDS（非度量多维尺度分析）等。

需要注意的是：非约束排序只是一种描述性的方法，不存在统计检验评估排序结果显著性的问题；而约束排序则需要对排序的结果进行显著性检验。

# NMDS的原理

数学原理和算法很复杂，我们作为应用中，只需要要知道怎么用就可以了（下面的例子都是我自己的理解，不妥指出还请批评指正）。

举个很简单的例子，假设现在路上有4个人在跑步，分别是①②③④。现在我们并不关心他们之间的具体的距离是多少，我们在乎的只是对某个人来说，其他三个人和他的相对距离。现在假设我是图中的①，那么②就是我的”第一远“，思就是我的”第二远“，③就是我的”第三远“。

{% asset_img 1.png %}

在NMDS中，排序轴就是一条条的跑道，根据排序轴来比较样本的差异。

# NMDS在R中的实现

好像是有好多软件能完成NMDS分析，但是我还是觉得R语言是最好的。PS：就在我些这个文章的时候，同学告诉我说经典的进化树可视化软件（软件）`iTOL`开始收费了，所以是，开源不收费还是好啊。

```R
rm(list = ls())

library(ade4)
library(vegan)
library(plyr)
library(tidyverse)
library(ggsci)

# download data
load('Doubs.RData')
spe = spe[-8,] # 提出无物种数据的样本

# run NMDS
spe.nmds = vegan::metaMDS(spe, distance = 'bray')
spe.nmds

# 经验法则：应力 < 0.05 可很好地表示尺寸减小，
# <0.1 非常好，<0.2 还不错，而应力 < 0.3 有待提高。
spe.nmds$stress

plot(spe.nmds,type = 't')

# 评估拟合度
png(filename = '20201109NMDS(非度量多维尺度分析)/figures/2.png',
    width = 500, heigh = 400)
stressplot(spe.nmds)
dev.off()
```

{% asset_img 2.png %}



这个图看$R^2$即可，$R^2$越大越好。

# NMDS可视化

NMDS的可视化本质是散点图，通常有三种可视化方法：

1. 置信椭圆
2. 多边形
3. 放射线

```R
# 利用ggplot2进行可视化
nmds.res = spe.nmds[["points"]] %>%
  as.data.frame() %>%
  mutate(group = rep(c('a','b','c'),c(10,10,9)))

# 椭圆
p1 = ggplot(nmds.res, aes(MDS1, MDS2, color = group)) +
  geom_point() +
  stat_ellipse(level = 0.68, show.legend = F) +
  scale_x_continuous(breaks = seq(-2,2,0.5)) +
  scale_color_aaas() +
  annotate('text', x = -1.4, y = -1.2, label = 'Rseq = 0.995 \n Stress = 0.0738') +
  labs(x = 'NMDS1',y = 'NMDS2') +
  theme_bw() +
  theme(legend.position = c(0.1,0.3))
p1
ggsave(p1, filename = '20201109NMDS(非度量多维尺度分析)/figures/3.png',
       width = 5, height = 5)
```

{% asset_img 3.png %}

```R
# 多边形
group_border = ddply(nmds.res, 'group', 
                     function(df) df[chull(df[[1]], df[[2]]), ])

p2 = ggplot(nmds.res, aes(MDS1, MDS2, color = group, fill = group)) +
  geom_point() +
  geom_polygon(data = group_border, alpha = 0.4, show.legend = F) +
  scale_x_continuous(breaks = seq(-2,2,0.5)) +
  scale_color_aaas() +
  scale_fill_aaas() +
  annotate('text', x = -1.4, y = -1.2, label = 'Rseq = 0.995 \n Stress = 0.0738') +
  labs(x = 'NMDS1',y = 'NMDS2') +
  theme_bw() +
  theme(legend.position = c(0.1,0.3))
p2
ggsave(p1, filename = '20201109NMDS(非度量多维尺度分析)/figures/4.png',
       width = 5, height = 5)
```

{% asset_img 4.png %}

```R
# 放射线

# mean
cent = aggregate(cbind(MDS1,MDS2) ~ group, data = nmds.res, FUN = mean)
colnames(cent)[2:3] = c('cent1','cent2')

# merge data
nmds.res = merge(nmds.res, cent, by = 'group', all.x = TRUE)

p3 = ggplot(nmds.res, aes(MDS1, MDS2, color = group)) +
  geom_point() +
  geom_point(data = cent, aes(cent1, cent2), size = 5, show.legend = FALSE) +
  geom_segment(mapping = aes(xend = cent1, yend = cent2), show.legend = FALSE) +
  scale_x_continuous(breaks = seq(-2,2,0.5)) +
  scale_color_aaas() +
  scale_fill_aaas() +
  annotate('text', x = -1.4, y = -1.2, label = 'Rseq = 0.995 \n Stress = 0.0738') +
  labs(x = 'NMDS1',y = 'NMDS2') +
  theme_bw() +
  theme(legend.position = c(0.1,0.3))
p3
ggsave(p3, filename = '20201109NMDS(非度量多维尺度分析)/figures/5.png',
       width = 5, height = 5)
```

{% asset_img 5.png %}

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com















