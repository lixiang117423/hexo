---
title: tidyHeatmap学习笔记
tags: R语言
categories: R语言
abbrlink: 4de9add
date: 2021-02-04 19:49:12
---

相当惊艳的一个包，简单学习了下。<!-- more -->

```R
#devtools::install_github("stemangiola/tidyHeatmap")

library(tidyHeatmap)
library(tidyverse)

mtcars_tidy <- 
  mtcars %>% 
  as_tibble(rownames="Car name") %>% 
  
  # Scale 除开那些行，剩下的行进行标准化
  mutate_at(vars(-`Car name`, -hp, -vs), scale) %>%
  
  # tidyfy 转换成长数据，保证3个变量不变，剩下的转换成长数据
  pivot_longer(cols = -c(`Car name`, hp, vs), names_to = "Property", values_to = "Value")

mtcars_tidy

# plot
mtcars_heatmap <- 
  mtcars_tidy %>% 
  heatmap(`Car name`, # 行
          Property, # 列
          Value ) %>%
  add_tile(hp) # 行注释

mtcars_heatmap

# save
mtcars_heatmap %>% save_pdf("mtcars_heatmap.pdf")

# grouping
mtcars_tidy %>% 
  group_by(vs) %>% # 按照vs这个变量进行分组
  heatmap(`Car name`, Property, Value ) %>%
  add_tile(hp)

# 自定义颜色
mtcars_tidy %>% 
  heatmap(
    `Car name`, 
    Property, 
    Value,
    palette_value = c("red", "white", "blue")
  )

mtcars_tidy %>% 
  heatmap(
    `Car name`, 
    Property, 
    Value,
    palette_value = circlize::colorRamp2(c(-2, -1, 0, 1, 2), viridis::magma(5))
  )

# Multiple groupings and annotations
tidyHeatmap::pasilla %>%
  group_by(location, type) %>%
  heatmap(
    .column = sample,
    .row = symbol,
    .value = `count normalised adjusted`
  ) %>%
  add_tile(condition) %>%
  add_tile(activation)

# Annotation types

# Create some more data points
pasilla_plus <- 
  tidyHeatmap::pasilla %>%
  dplyr::mutate(act = activation) %>% 
  tidyr::nest(data = -sample) %>% #创建list
  dplyr::mutate(size = rnorm(n(), 4,0.5)) %>%
  dplyr::mutate(age = runif(n(), 50, 200)) %>%
  tidyr::unnest(data) 

# Plot
pasilla_plus %>%
  heatmap(
    .column = sample,
    .row = symbol,
    .value = `count normalised adjusted`
  ) %>%
  add_tile(condition) %>%
  add_point(activation) %>%
  add_tile(act) %>%
  add_bar(size) %>%
  add_line(age)
```

{% asset_img 1.png %}

---

>>💌lixiang117423@foxmail.com
>
>>💌lixiang117423@gmail.com

