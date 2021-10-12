---
title: "配色包\x96paletteer使用"
tags: R语言
categories: R语言
abbrlink: d4b49eb0
date: 2021-04-13 09:29:27
---

```R
library(paletteer)
```

<!-- more -->

```R

paletteer_c("scico::berlin", n = 10)

## <colors>
## #9EB0FFFF #5AA3DAFF #2D7597FF #194155FF #11181DFF #270C01FF #501802FF #8A3F2AFF #C37469FF #FFACACFF

paletteer_d("RColorBrewer::Paired")

## <colors>
## #A6CEE3FF #1F78B4FF #B2DF8AFF #33A02CFF #FB9A99FF #E31A1CFF #FDBF6FFF #FF7F00FF #CAB2D6FF #6A3D9AFF #FFFF99FF #B15928FF

paletteer_dynamic("cartography::green.pal", 5)

## <colors>
## #B8D9A9FF #8DBC80FF #5D9D52FF #287A22FF #17692CFF

library(ggplot2)
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +
  geom_point() +
  scale_color_paletteer_d("basetheme::minimal")
  
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Sepal.Width)) +
  geom_point() +
  scale_color_paletteer_c("grDevices::PinkYl")
  
library(ggpubr)
data("ToothGrowth")
df <- ToothGrowth
ggboxplot(df, x = "dose", y = "len", width = 0.8,color = "dose")+
  scale_color_paletteer_d("basetheme::minimal")  
  
pheatmap::pheatmap(volcano,color = paletteer_c("scico::berlin", n = 100))

library(ComplexHeatmap)
Heatmap(t(iris[,1:4]),col = paletteer_c("scico::berlin", n = 100),name = "iris")
```

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com

