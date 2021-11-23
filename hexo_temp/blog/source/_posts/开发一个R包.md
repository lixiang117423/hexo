---
title: 开发一个R包
tags: R语言
categories: R语言
abbrlink: 6f22d8f6
date: 2020-01-10 16:26:48
---

R最强大的莫过于统计分析和可视化，关键是完全的开源免费啊。有时候使用多了以后，会积累一些函数或者是数据库，而这些函数和数据库通常能够帮助到别人，这时候就可以把这些函数或者是数据库打包成R包，上传到CRAN、Bioconductor或者是GitHub，让 其他的使用者使用自己的包。

<!-- more -->

我开发的第一个包是[riceidconverter](https://cran.r-project.org/web/packages/riceidconverter/index.html)，主要的用途是水稻的ID转换。整个包的开发断断续续经历了两个月，包括数据的爬取(Python脚本见[GitHub]([https://github.com/GitHub-LiXiang/R/tree/master/R%E5%8C%85%E5%BC%80%E5%8F%91/riceidconverter/NCBI%E7%88%AC%E8%99%ABPython%E8%84%9A%E6%9C%AC](https://github.com/GitHub-LiXiang/R/tree/master/R包开发/riceidconverter/NCBI爬虫Python脚本)))、整理、函数的构思，以及最艰难的调试。

{% asset_img 1.png %}

# 主要流程

我的开发流程是软件安装、构思R包、准备数据、编写R包、调试代码、R包提交。下面就从这几方面一一道来我这个小白的经验。

# 软件安装

## MikTex

`MikTex`主要是用于编译后面的pdf文档，如果包只是自己用，就不用安装这个软件。软件的下载地址是[MikTex](https://miktex.org/download)。安装的话一路默认就OK。

## roxygen2

`roxygen2`是个R包，通过注释的方式，生成文档。直接`install。package('roxygen2')`即可。

## devtools

这个包主要是用来`build`和`check`R包的。直接`install。package('devtools')`即可。

# 构思R包

这个比较难说清楚，每个R包都有一定的功能的，构思的过程就是R包功能完善的过程。

# 准备数据

这个环节，也是很难说清除。如果数据要内嵌到R包，而且包里面的函数会用到数据，那表头名称和函数中的变量名称要保持一致。

# 编写R包

## 创建项目

直接用RStudio创建`R Package即可`：`File→New Project→New Directory→R Package`。<font color=red>需要注意的是选择的路径不可以有中文字符！</font>会生成下面的文件：

{% asset_img 2.png %}

比较重要的是`man`、`R`和`DESCRIPTION`这三个文件(夹)。其他的几个可以删除。

## 编写DESCRIPTION

这个文件是用来描述一些基本信息的，这些信息也是必填的一些信息。

{% asset_img 3.png %}

下面这是我的包的一些描述：

{% asset_img 4.png %}

<font color=red>需要注意的是在`Title`部分，大小写要求很严格。</font>

另外需要注意的是在`Description`部分，每个缩写都需要有详细的解释，如果有链接，还需要将链接放在`<>`里面，而不是`()`。

## 编写函数

在`R`这个文件夹下面创建对应的`.R`文件。比如想实现的功能是`t`检验，那就创建一个`t.test.R`。打开以后还是有几行`#'`开头的描述，这些是必须的：

{% asset_img 6.png %}

`@name`是指这个函数的名称，其他的就是和`DESCRIPTION`类似的；`@param`表示的是参数；`@example`表示的是函数使用的例子；`@return`表示的是返回的结果；接着下一行编写函数就行：

{% asset_img 7.png %}

<font color=red>需要注意的是在`R`文件夹下面还应该创建一个和R包名称相同的`.R`文件。</font>只需要填写这些东西就可以了：

{% asset_img 8.png %}

## 调试代码

这个部分，就需要不断的调试，就是使用不同的数据去测试这个函数是否可靠。

## 添加数据

如果需要将数据内嵌在R包怎么办呢？一行代码搞定：`use_data(test.data, internal = TRUE)`。`test.data`就是先前准备好的数据，需要先加载到R环境中。会在`R`文件夹下生成一个`sysdata.rda`文件。

# R包提交

在完成编写和调试后，就只剩下`build`、`check`和`upload`了。

先要生成注释文件：

````R
library(roxygen2)
roxygenize('packagename')
````

## build

一行代码：

```R
system('R CMD build packagename --binary')
```

会生成一个`tar.gz`文件。这个文件用于后面的提交。

## check 

一行代码：

```R
system('R CMD check packagename --as-cran')
```

完后会生成一个`riceidconverter.Rcheck`文件夹，里面有各种报告。在RStudio输出界面没有`ERROR`、`Warning`还有`NOTE`，那就基本没问题了。

## 安装

先尝试一下能不能安装上：

```R
system('R CMD INSTALL packagename')
```

## <font color=red>提交</font>

这个就比较简单了，直接在[https://cran.r-project.org/submit.html](https://cran.r-project.org/submit.html)按照要求提交`tar.gz`文件就行。

---

最后，等着邮件吧。

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

