---
title: clusterProfiler做富集分析
tags: R语言
categories: R语言
abbrlink: 97c73a9e
date: 2021-03-31 14:51:12
---

最近在分析水稻的转录组数据，用的参考基因组是我们小组自己组装的，没有用常见的那几个参考基因组做比对，这就导致一个问题，<!-- more -->得到的基因ID是我们参考基因组上的，而不是常见的水稻基因ID，也就无法转换成ENTREZID，想要用`clusterProfiler`$^{[1]}做$`GO`或者`KEGG`富集分析就很困难。难道就用公司返回的数据么？肯定不行啊，想要自己探索数据都不方便。怎么办呢？

仔细观察公司返回的数据，发现他们注释的信息里面是有GO和KEGG信息的：
{% asset_img 1.png %}

那我把这些信息整合一下就可以用`clusterProfiler`包的函数`enricher`进行富集分析。

# 构建富集分析的背景文件

通过一些列的代码将公司返回的数据里面的相关信息进行整理：

{% asset_img 2.png %}

第一列是基因ID，第二列是GO term的ID，第三列是GO term的描述，第四列是GO term的分类。

这个文件就是富集分析里面用到背景文件，背景文件里面的基因数量越多，后面富集到的也就越多。

# 开始富集分析

```R
go.rich.1 = enricher(gene = df.1$id, # 输入的差异基因的ID
                     TERM2GENE = go.anno[c('ID','gene.id')], # 指定背景文件中的基因ID
                     TERM2NAME = go.anno[c('ID','Description')], # 指定背景文件中的GO term的描述
                     pvalueCutoff = 1, # p值阈值
                     pAdjustMethod = 'BH', # p值校正方法
                     maxGSSize = length(df.1$id)) # 最大基因数量
```

运行完了以后，就得到对应的富集分析结果。

# 富集分析结果可视化

可视化我没有选择`clusterProfiler`默认的绘图函数，而是先把数据稍加整理，然后用`ggplot2`进行可视化。

{% asset_img 3.png %}

```R
ggplot(df.plot, aes(GeneRatio,Description)) +
  geom_point(aes(size = Count, shape = Ontology, color = pvalue)) +
  scale_color_gradient(low = 'navy',high = 'firebrick3') +
  labs(y = 'GO term', title = '15(15||15) VS 87(87||87)') +
  theme_bw() +
  theme(axis.text = element_text(color = 'black',size = 12))
```

{% asset_img 4.png %}

# 参考文献：

>[1] Yu G, Wang L G, Han Y, et al. clusterProfiler: an R package for comparing biological themes among gene clusters[J]. Omics: a journal of integrative biology, 2012, 16(5): 284-287.

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com

