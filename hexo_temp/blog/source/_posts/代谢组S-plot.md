---
title: 代谢组S-plot
tags: R语言
categories: R语言
abbrlink: a1ccb979
date: 2020-12-16 17:24:49
---

经过一翻探索，终于把OPLS-DA里面的S-plot给搞清楚了！

<!-- more -->

在代谢组学中，`S-plot`常用来展示差异代谢物。横坐标表示的是每个样品的在OPLS-DA模型上的得分与每个代谢物的协方差，纵坐标表示的是每个样品的在OPLS-DA模型上的得分与每个代谢物的相关性。通常筛选相关性≥0.8的代谢物为差异代谢物。也可以将代谢物的`VIP`值用不同的颜色进行展示。

```R
# load  packages
library(ropls)
library(ggplot2)
library(ggsci)
library(Cairo)
library(tidyverse)
library(extrafont)
loadfonts()

# load data
data(sacurine)
names(sacurine)

# OPLS-DA
oplsda = opls(dataMatrix, genderFc, predI = 1, orthoI = NA)

loading = oplsda@scoreMN %>% as.data.frame()
df = sacurine[["dataMatrix"]] %>% as.data.frame()

cor.value = WGCNA::cor(df, loading)
colnames(cor.value) = 'cor'

cov.value = cov(df, loading)
colnames(cov.value) = 'cov'

res = cbind(cor.value, cov.value) %>% as.data.frame()
res$col = ifelse(res$cor > 0.2,'Positive',
                 ifelse(res$cor < -0.2, 'Negative','NS'))
res$col = factor(res$col, levels = unique(res$col))

p = ggplot(res, aes(cov, cor, col = col)) +
  geom_vline(xintercept = 0, linetype = 'dashed') +
  geom_hline(yintercept = 0, linetype = 'dashed') +
  geom_point(size = 2) +
  scale_color_manual(values = c('black', 'blue', 'red')) +
  labs(x = 'Cov',y = 'Corr') +
  theme_bw() +
  theme(legend.title = element_blank(),
        legend.position = c(0.8,0.3))

p

ggsave(p, filename = 'S-plot.pdf', 
       width = 5, height = 5, device = cairo_pdf)
```

{% asset_img 1.png %}

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

