---
title: iTOL修饰进化树
tags: 生物信息学
categories: 生物信息学
abbrlink: 651c50ad
date: 2020-01-09 20:22:33
---

绘制进化树的软件很多，窗口界面的MEGA$^{[1]}$、Y叔R包ggtree$^{[2]}$等。MEGA属于神仙级别的软件，一篇文章拉高期刊的影响因子。而Y的`ggtree`更受R爱好者的青睐，可以各种尽情修饰进化树。相对来说，MEGA建的树就不是那么好看，需要后期修饰一下。修饰的软件推荐[iTOL](https://itol.embl.de/)$^{[3]}$。大多数的参数直接在右边界面就能修改，但是如果需要批量修改颜色等信息的话，就需要写配置文件。

<!-- more -->

# 开局一张图

`iTOL`并不能建树，只能修饰进化树，需要导入`.nwk`结尾的文件，是长这样的：

{% asset_img 1.png %}

在网站界面直接选择文件upload就行，就能得到下面这样的图：

{% asset_img 2.png %}

简单修饰直接点击右边就能进行修改。

# 标签背景色

批量添加标签的背景色，需要写一个配置文件`label.txt`，这个文件的格式是这样的：

{% asset_img 3.png %}

最上面的三行是默认的，下面的分别表示样品名称、range(表示背景色)、颜色编码、样品的分组。最后上色的时候是用样品分组信息进行着色的，效果如下：

{% asset_img 4.png %}

# 线条着色

同样的编辑配置文件，格式如下：

{% asset_img 6.png %}

前三行是固定的，下面每一列分别表示的是样品名称、线条、颜色属性、样式、大小。

编辑完之后直接将文件拖到网页的进化树上就行了。效果如下：

{% asset_img 5.png %}

# 标签颜色

标签颜色和标签的背景色的设置是大同小异的，直接将`range`换成`label`就可以 了。

# 最终效果

{% asset_img 7.png %}

<font color=red>更多修饰细节可以观看网页视频教程噢。</font>

# 参考文献

>[1] Kumar, Sudhir, Koichiro Tamura, and Masatoshi Nei. "MEGA: molecular evolutionary genetics analysis software for microcomputers." **Bioinformatics**** 10.2 (1994): 189-191.
>
>[2] Yu, Guangchuang, et al. "ggtree: an R package for visualization and annotation of phylogenetic trees with their covariates and other associated data." ***Methods in Ecology and Evolution*** 8.1 (2017): 28-36.
>
>[3] Letunic, Ivica, and Peer Bork. "Interactive tree of life (iTOL) v3: an online tool for the display and annotation of phylogenetic and other trees." ***Nucleic acids research*** 44.W1 (2016): W242-W245.

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
