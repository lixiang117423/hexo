---
title: ggplot2柱状图相关
tags: R语言
categories: R语言
abbrlink: c005101c
date: 2021-03-01 15:26:37 
---

之前在公众号上的文章，查看不方便，搬到个人博客好了。<!-- more -->

```R
rm(list = ls())

library(tidyverse)
library(ggplot2)

library(ggsci)
library(reshape2)

data = melt(iris, id.vars = ncol(iris))

# 普通柱状图
p0 = ggplot(data, aes(Species, value)) +
        geom_bar(aes(fill = variable),
                 stat = 'identity',
                 position = 'dodge') +
        scale_y_continuous(expand = c(0,0)) +
        scale_fill_aaas() +
        theme_bw()
ggsave(p0, filename = '普通柱状图.pdf',width = 5, height = 5)

# 堆叠柱状图
p1 = ggplot(data, aes(Species, value)) +
        geom_bar(aes(fill = variable),
                 stat = 'identity') +
        scale_y_continuous(expand = c(0,0)) +
        scale_fill_aaas() +
        theme_bw()

ggsave(p1, filename = '堆叠柱状图.pdf',width = 5, height = 5)

# 百分比柱状图
p2 = ggplot(data, aes(Species, value)) +
        geom_bar(aes(fill = variable),
                 stat = 'identity',
                 position = 'fill') +
        scale_y_continuous(labels = scales::percent) +
        scale_fill_aaas() +
        theme_bw()
ggsave(p2, filename = '百分比柱状图.pdf',width = 5, height = 5)

# 带百分比标签的堆积柱状图
data.2 = data %>%
        mutate(cat = paste(data$variable, data$Species, sep = '_'))
data.2 = aggregate(data.2$value, by = list(as.character(data.2$Species), 
                                          as.character(data.2$variable)), FUN = sum)
colnames(data.2) = c('Species', 'variable','value')

sum.temp = aggregate(data.2$value, by = list(data.2$Species), FUN = sum)

data.2$per = ifelse(data.2$Species == 'setosa', 
                    data.2$value / sum.temp[1,2],
                    ifelse(data.2$Species == 'versicolor', 
                           data.2$value / sum.temp[2,2],
                           data.2$value / sum.temp[3,2]))
data.2$per2 = paste(round(data.2$per *100, 2), '%', sep = '')
data.2$variable = factor(data.2$variable, levels = unique(data.2$variable))


p3 = ggplot(data.2, aes(Species, per, 
                     fill = variable,
                     label = per2)) +
        geom_col(position = position_stack()) +
        geom_text(position = position_stack(vjust = .5), 
                  size = 2.5, color = 'white') +
        scale_y_continuous(labels = scales::percent) +
        theme_bw() +
        scale_fill_aaas() +
        theme(axis.text = element_text(color = 'black'))

ggsave(p3, filename = '带百分比标签的堆积柱状图.pdf',width = 5, height = 5)
```

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com