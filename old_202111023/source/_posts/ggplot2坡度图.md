---
title: ggplot2坡度图
tags: R语言
categories: R语言
abbrlink: b7629aa1
date: 2020-12-30 18:29:36
---

之前见过坡度图，但是不知道怎么画。今天稍微看了一下就搞定了！

<!-- more -->

```R
rm(list = ls())
library(ggplot2)
library(ggsci)

df = data.frame(cat = rep(c(1,2), each = 10),
                value = c(1:10,6:15),
                c = 1:10,
                d = 6:15,
                e= letters[1:10])
ggplot(df, aes(cat, value)) +
  geom_vline(xintercept = 1:2,linetype = 'dashed') +
  geom_point(aes(color = e),size = 2) +
  geom_segment(aes(x = 1, xend = 2, 
                   y = c, yend = d, color = e),
               size = 1) +
  geom_hline(yintercept = 16, color = 'white') +
  scale_y_continuous(breaks = seq(-1,15,2)) +
  scale_x_discrete(limit = c(1,2)) +
  scale_color_aaas() +
  labs(x = '',y = '') +
  theme_bw() +
  theme(legend.position = 'none')
```

{% asset_img 1.png %}

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

