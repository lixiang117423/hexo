---
title: R包stat4xiang
date: 2021-01-04 11:12:47
tags: R 语言
categories: R语言
---

# Summary

The R package [**stat4xiang**](https://github.com/lixiang117423/stat4xiang) is for statistical analysis including *Student t-test*, *Anova*, *Wilcox test* and *Kruskal test*.

<!-- more -->

# Download and Install

To download the development version of the package, type the following at the R command line:

```r
install.packages("devtools")
devtools::install_github("lixiang117423/stat4xiang", build_vignettes = TRUE)
```

# Parameter

>`df`: input data.frame 输入数据框
>
>`value`: Colnames of value 值所在的列名
>
>`group`: Colnames of group 分组信息所在列名
>
>`method`: Method of statistics 统计方法：`t检验`、`方差分析`、`Wilcox检验`及`Kruskal检验`
>
>`level`: Statistical inspection level 显著水平，如`0.99`

# Basic example

```R
library(stat4xiang)

res <- stat4xiang(iris,'Sepal.Length','Species','anova',0.99)
```

# Reporting bugs and other issues

If you encounter a clear bug, please file a minimal reproducible example on github.

# Contact us

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

