---
title: R语言常用Tips
date: 2021-01-18 17:17:33
tags: R语言
categories: R语言
top: true
---

经常要用到`R`，有些小技巧每次都要去查，比较麻烦，干脆记录一下。

<!-- more -->

1. `ggplot2`限制Y轴范围：

   ```R
   coord_cartesian(ylim = c(5, 22))
   ```

2. 安装`Rtools`：

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

3. `ggplot2`输出中文：

   ```R
    theme_bw(base_family = "STKaiti")
   ```

   

>>💌lixiang117423@gmail.com
>
>>💌lixiang117423@foxmail.com