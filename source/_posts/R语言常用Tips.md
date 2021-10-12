---
title: R语言常用Tips
tags: R语言
categories: R语言
top: true
abbrlink: '15541358'
date: 2021-01-18 17:17:33
---

经常要用到`R`，有些小技巧每次都要去查，比较麻烦，干脆记录一下。

<!-- more -->

# 软件安装

1. 安装`Rtools`：

   - 安装 Rtools4.0，安装包：[https://cran.r-project.org/bin/windows/Rtools/](https://link.zhihu.com/?target=https%3A//cran.r-project.org/bin/windows/Rtools/)

   - 配置环境

     - 在 RStudio 里面运行以下脚本：

       ```R
       writeLines('PATH="${RTOOLS40_HOME}\\usr\\bin;${PATH}"', con = "~/.Renviron")
       ```

     - 重新启动 RStudio，然后运行以下代码：

       ```R
       Sys.which("make")
       ```

       会得到结果："C:\\rtools40\\usr\\bin\\make.exe"（也就是 make.exe 的路径）

     - 尝试安装一个包

       ```R
       install.packages("jsonlite", type = "source")
       ```

2. `RStudio`中文乱码：
   菜单栏中的 `file->reopen with encoding->utf-8`

3. `Rshiny`上传文件大小限制：在`server.R`文件顶部加上下面这行代码：

   ```R
   options(shiny.maxRequestSize=1000*1024^2)
   ```
   
4. 更新所有R包：

   ```R
   #安装包
   install.packages("rvcheck")
   #加载包
   library(rvcheck)
   #检查R是否有更新
   rvcheck::check_r()
   # 更新所有R包
   rvcheck::update_all(check_R = FALSE,which = c("CRAN","BioC","github")
   ```
   
5. 更新R版本：

   ```R
   library(installr)
   updateR()
   ```

   

# `ggplot2`

1. `ggplot2`限制Y轴范围：

   ```R
   coord_cartesian(ylim = c(5, 22))
   ```

2. `ggplot2`输出中文：

   ```R
    theme_bw(base_family = "STKaiti")
   ```

3. `ggplot2`坐标轴文字角度：

   ```R
   axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)
   ```

4. `ggplot2`导出成`PPT`：

   ```R
   export::graph2ppt(p2, width = 6, height = 5,
                     margins = c(top = 0.5, right = 0.5, 
                                     bottom = 0.5, left= 0.5), 
                     center = TRUE,
                     file = '../results/PPT/稻瘟病发病情况（2020）.ppt')
   ```

5. `ggplot2`渐变色填充：

   ```R
   scale_fill_gradient2(low = "#000080", mid = "white", high = "#B22222")
   ```
   
6. 图例名称：

   ```R
   labs(fill = 'Cor')
   ```
   
7. 坐标轴刻度长度：

   ```R
   theme(axis.ticks.length.y = unit(0,'mm'))
   ```

8. 颠倒X轴和Y轴：

   ```R
   coord_flip()
   ```

   

# 热图相关

1. `ComplexHeatmap`注释的颜色设置：

   ```R
   ann.right = HeatmapAnnotation(which = 'row',
                                 gap = unit(1.5,'mm'),
                                 `Class I` = res.cor.3$`Class I`,
                                 annotation_name_side = 'top',
                                 annotation_name_rot = 90,
                                 annotation_name_offset = unit(2,'mm'),
                                 col = list(`Class I` = c('Lipids' = '#DC143C',
                                                         'Phenolic acids' = '#00FF00',
                                                         'Alkaloids' = '#483D8B',
                                                         'Terpenoids' = '#808000',
                                                         'Organic acids' = '#FF8C00',
                                                         'Others' = '#B22222',
                                                         'Nucleotides' = '#000000',
                                                         'Flavonoids' = '#006400',
                                                         'Amino acids' = '#0000CD')))
   ```

   

2. 调用`pheatmap`包中的函数解决`ComplexHeatmap::Heatmap`数据标准化问题：

   ```R
   df.heatmap[,1:6] %>% as.matrix() %>%
     pheatmap:::scale_rows() %>%
     ComplexHeatmap::Heatmap(name = '相 对\n表达量',
                             col = c("navy", "white", "firebrick3"),
                             show_row_names = FALSE)
   ```
   
3. 热图标注显著性：

   ```R
   p.cor = quickcor(design, mes, cor.test = TRUE) +
     geom_colour() +
     geom_mark(r = NA,sig.thres = 0.05, 
               size = 5, color = 'black',
               nudge_x = 0, nudge_y = 0) +
     scale_fill_gradient2(low = "navy", 
                          mid = "white", 
                          high = "firebrick3")+
     labs(fill = 'Cor')
   ```

4. `ggcor`绘制两个矩阵的热图：

   ```R
   quickcor(df.dems.1, df.degs.1.down, cor.test = TRUE, height = 10) +
       geom_colour() +
       scale_fill_gradient2(low = "navy", 
                            mid = "white", 
                            high = "firebrick3")+
       labs(fill = 'Cor')+
       remove_x_axis() +
       theme(axis.ticks.length.y = unit(0,'mm'),
             axis.text.y = element_text(size = 1))
   ```

   

# 数据处理

1. `dcast()`函数用法：

   ```R
   reshape2::dcast(res.cor, gene ~ meta) # gene是行，meta是列
   # acast()函数的话直接就生成rownames
   # gene在第一列，meta在第二列，这样才能成功，我也不知道是为啥！
   ```

2. 方差分析多重比较：

   ```R
   tuk.15 = glht(fit.15, linfct = mcp(donor = 'Tukey'))
   sig.15 = cld(tuk.15, level = 0.95, decreasing = TRUE)[["mcletters"]][["Letters"]] %>%
           as.data.frame()
   ```

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

