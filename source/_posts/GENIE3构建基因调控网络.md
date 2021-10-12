---
title: GENIE3构建基因调控网络
tags: R语言
categories: R语言
abbrlink: '10120676'
date: 2021-07-06 10:20:00
---

最近一直寻思着构建基因共表达网络，之前了解到的方法是根据相关性构建互作网络。想着看看有没有新的方法，找到了这样一篇文献：

<!-- more -->

{% asset_img 1.png %}

谷歌学术显示该文章已经被引用940余次，引用的期刊不乏***Nature***等。

具体的算法实现过程看不懂，那就应用吧。

检索发现官方教程：https://bioconductor.org/packages/release/bioc/vignettes/GENIE3/inst/doc/GENIE3.html

# 输入数据

需要输入的数据是个表达矩阵，矩阵的行是基因，列是样本：

```R
##       Sample1 Sample2 Sample3 Sample4 Sample5
## Gene1       9       9       6       4       6
## Gene2       7       1       1       9       2
## Gene3      10       6       6       7       9
## Gene4       6       2      10       5       7
## Gene5       6       3      10       2      10
## Gene6       7       1       4      10       8
```

需要注意的是，作者在教程中提到输入的基因表达矩阵不能进行任何的处理，包括标准化、筛选及log转换等。

# 函数参数

```R
GENIE3(
  exprMatrix, # 表达矩阵
  regulators = NULL, # 指定潜在的调控因子，比如转录因子等
  targets = NULL, # 潜在的被调控的靶标基因
  treeMethod = "RF", # 选择方法，默认的是“RF"（随机森林），还可以选择“ET”（Extra-Trees）
  K = "sqrt", 
  nTrees = 1000, # 树的量，默认是1000
  nCores = 1, # 用于并行计算的核数，表达矩阵较大时选择并行，运算速度更快。
  returnMatrix = TRUE, # 结果返回形式是矩阵还是list，选择"TRUE"就返回矩阵，否则就返回list
  verbose = FALSE # 是否展示计算进度，默认是FALSE，即不展示计算进度
)
```

# 输出结果

```R
> head(linkList)
  regulatoryGene targetGene    weight
1          Gene8      Gene4 0.2056790
2         Gene13      Gene3 0.1918921
3         Gene12      Gene3 0.1822270
4          Gene7      Gene1 0.1801217
5         Gene17      Gene9 0.1781883
6          Gene5      Gene6 0.1750425
```

输出的结果有三列，分别是调控基因和被调控基因及权重weight。

# 结果提取

如果选择参数`returnMatrix = TRUE`的话，返回的就是矩阵，否则返回的是list，需要进行提取。

提取方式有两种：

- 提取前多少个
- 按照阈值进行提取

```
# 提取前几位top调控连接
linkList <- getLinkList(weightMat, reportMax=5)

# 按阈值提取
linkList <- getLinkList(weightMat, threshold=0.1)
```

# 注意事项

输出结果中的`weight`是没有统计学意义的，阈值的选择需要按照自己的经验进行选择。

# 结果可视化

最后的结果可以用Gephi或者是Cytoscape等软件进行可视化。

Gephi安装参考教程：https://mp.weixin.qq.com/s/Eotixm5tCMHgw_cXj8b6GQ

Gephi使用简明教程：https://mp.weixin.qq.com/s/8DTbSEJfrImXVhQWCAbfvw

{% asset_img 2.png %}

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com

