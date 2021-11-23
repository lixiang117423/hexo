---
title: ggplot2画箭头
tags: R语言
categories: R语言
abbrlink: f2d7bee6
date: 2020-12-16 15:18:17
---

突然有个用`ggplot2`画箭头的需求，So，搞它！

<!-- more -->

{% asset_img 1.jpg %}

```R
library(tidyverse)

data("iris")

pca = prcomp(iris[,1:4])

score = pca[["x"]] %>% as.data.frame()
loading = pca[["rotation"]] %>% as.data.frame()

ggplot(score, aes(PC1, PC2)) +
  geom_hline(yintercept = 0, linetype = 'dashed') +
  geom_vline(xintercept = 0, linetype = 'dashed') +
  geom_point(aes(color = iris$Species)) +
  geom_segment(data = loading,
               aes(x = PC1, y = PC2, xend = 0, yend = 0),
               arrow = arrow(length=unit(0.20,"cm"), 
                             ends="first", type = "closed"), 
               size = 0.5) +
  geom_text(data = loading,
            aes(x = PC1, y = PC2, label = rownames(loading)),
            size = 3) +
  theme_bw()
```

----

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

