---
title: ComplexHeatmap学习笔记
tags: R语言
categories: R语言
abbrlink: 550b1dc8
date: 2021-03-06 14:11:08
---

之前绘制热图都是使用`pheatmap`这个R包，后面<!-- more -->了解到一个包叫[`tidyHeatmap`](https://github.com/stemangiola/tidyHeatmap)，开始使用的时候觉得比较惊艳，数据格式是`tidy`的，比较熟悉些。后面自己要绘制比较复杂的热图，感觉`tidyHeatmap`不够用，索性直接学`ComplexHeatmap`。

# 我对`ComplexHeatmap`的理解

`ComplexHeatmap`是基于`grid`绘图系统的，对`grid`绘图系统了解不多，但是学习完`ComplexHeatmap`给我的感受是就像`ggplot2`那样，丝滑无比。我把`ComplexHeatmap`里面的各种注释、图列理解成了`ggplot2`里面的图层，不同的图层之间通过唯一的`key`来实现的。

# 示例代码

下面的示例代码我会选择性注释，未注释的代码行多为`R`基础。

```R
# 15_15VS87_87
if (F) {
  # 选择画图的数据
  col = c('Index',
          paste(str_split('15_15VS87_87','VS')[[1]][1],1:3, sep = '_'),
          paste(str_split('15_15VS87_87','VS')[[1]][2],1:3, sep = '_'))
    
  # 筛选数据
  df.sub = dplyr::select(metadata, col) %>%
    dplyr::filter(Index %in% df[df$group_by == '15_15VS87_87',]$Index) %>%
    as.data.frame()
  
  # 合并数据
  df.sub = merge(df.sub, metainfo[,c('Index','物质')])
  
  col.names = colnames(df.sub)[2:7]
  
  rownames(df.sub) = df.sub$物质
  
  
  df.sub = df.sub[,2:7] %>% # 选择数据
    apply(1, scale) %>% # 按行对数据进行标准化
    t() %>% # 行列转换
    as.data.frame()
  
  colnames(df.sub) = col.names
  
  ann = df[df$group_by == '15_15VS87_87',] # 筛选代谢物的信息，分组筛选
  ann = merge(ann, metainfo, by = 'Index') %>% as.data.frame() # 从原始数据中筛选代谢物信息
  rownames(ann) = ann$物质 # 将注释信息数据框的行名称设置成代谢物名称
  ann = ann[rownames(df.sub),] # 将代谢物注释信息和热图数据框进行匹配，这个就是上面提到的key
  ann$signif = ifelse(ann$pvalue < 0.001, '***',
                      ifelse(ann$pvalue > 0.01, '*','**')) # 根据p值标注显著性
  
  # 热图左边的注释
  ann.left = HeatmapAnnotation(which = 'row', # 表明这是行的注释
                               # 柱状图注释
                               `OPLS-DA VIP Value` = anno_barplot(ann$VIP,# 选择数据来源
                                                                  baseline = 1, # 柱状图基线
                                                                  # 设置颜色及填充色等
                                                                  gp = gpar(fill = 1:nrow(ann),
                                                                            col = 'white')),
                               # 同上
                               FoldChange = anno_barplot(ann$FC,
                                                         # bar_width = 1,
                                                         gp = gpar(fill = 1:nrow(ann),
                                                                   col = 'white')),
                               gap = unit(3,'mm'), # 两个注释信息之间的间隔
                               annotation_name_side = 'top', # 注释信息的名称
                               annotation_name_rot = 90, # 注释信息名称的旋转角度
                               annotation_name_offset = unit(2,'mm')) # 注释信息名称的偏移量
  
  # 热图顶部注释：此处只是简单地添加分组信息
  ann.top = HeatmapAnnotation(which = 'column',
                              #Group = rep(c('15_15','15_69'), each = 3),
                              Group = anno_block(gp = gpar(fill = 'black'),
                                                 labels = c('87_87','15_15'), # 手动调整分组
                                                 labels_gp = gpar(col = 'white', fontsize = 15)))
  # 右侧注释
  ann.right = HeatmapAnnotation(which = 'row',
                                gap = unit(1.5,'mm'), 
                                pvalue = anno_simple(ann$pvalue, 
                                                     col = pvalue_col_fun,
                                                     pch = ann$signif), # 只能显示1个*，多余的要手动加
                                一级分类 = ann$物质一级分类,
                                二级分类 = ann$物质二级分类,
                                annotation_name_side = 'top',
                                annotation_name_rot = 90,
                                annotation_name_offset = unit(2,'mm'))
  
  # 定义P值的颜色等
  pvalue_col_fun = colorRamp2(c(min(ann$pvalue), 
                                mean(ann$pvalue), 
                                max(ann$pvalue)), 
                              c("green", "white", "red")) 
  
  # 设置P值的图例等
  lgd_pvalue = Legend(title = 'P-value',
                      col_fun = pvalue_col_fun,
                      at = c(min(ann$pvalue), 
                             mean(ann$pvalue), 
                             max(ann$pvalue)),
                      
                      labels = c(round(min(ann$pvalue), 5), 
                                 round(mean(ann$pvalue), 5), 
                                 round(max(ann$pvalue), 5)))
  
  # 绘制热图
  p = ComplexHeatmap::Heatmap(as.matrix(df.sub), # 输入数据为矩阵
                              name = '相对含量', # 热图图例名称
                              col = c("navy", "white", "firebrick3"), # 定义颜色
                              column_km = 2, # 划分列聚类
                              row_km = 2, # 划分行聚类
                              border = TRUE, # 显示边框
                              column_names_rot = 90, # 列名称旋转角度
                              row_names_rot = 45, # 行名称旋转角度
                              left_annotation = ann.left, # 添加左侧注释信息
                              top_annotation = ann.top, # 添加顶部注释信息
                              right_annotation = ann.right, # 添加右侧注释信息
                              row_title = 'Metabolites', # 行名称
                              column_title = 'Group', # 列名称
                              width = ncol(df.sub)*unit(10, "mm"), # 格子的宽度
                              height = nrow(df.sub)*unit(10, "mm")) # 格子的高度
  
  # 保存图片
  pdf(file = 'results/heatmap/complexheatmap/15_15VS87_87_1.pdf', width = 15, height = 20, family = 'GB1')
  
  # 绘图
  draw(p, 
       merge_legend = TRUE, # 图例在一列上
       annotation_legend_list = list(lgd_pvalue))
  
  dev.off() # 关闭绘图设备
```

{% asset_img 1.jpg %}

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com