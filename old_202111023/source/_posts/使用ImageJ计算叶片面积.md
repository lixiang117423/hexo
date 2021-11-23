---
title: 使用ImageJ计算叶片面积
tags: 技能
categories: 技能
abbrlink: da044cd8
date: 2021-01-30 17:59:40
---

后续要扫描大量的水稻叶片然后计算病斑数量，之前没有使用过ImageJ这个软件，今天下午学了一下，成功get扫描一个图片中多个叶片面积的方法。

<!-- more -->

# 软件安装

可以从官网下载安装（[点击下载](https://imagej.nih.gov/ij/download.html)），但是网速感人，我把软件放在坚果云上面了，高速下载（[点击下载](https://www.jianguoyun.com/p/DXXP9zgQkOqUCRjesN8D )）。下载后解压，然后双击就能打开软件：

{% asset_img 1.png %}

# 准备图片

准备扫描的图片需要注意的是叶片不能和接触到边界，不然不能计算面积。

{% asset_img 2.png %}

# 导入图片

File→Open...即可打开图片：

{% asset_img 3.png %}

{% asset_img 4.png %}

# 处理图片

导入的图片需要转换成`8-bit`格式：

{% asset_img 5.png %}

转换后面的图片是这样的：

{% asset_img 6.png %}

# 改变阈值

改变图片的颜色阈值，让叶片与背景分开：

{% asset_img 7.png %}

{% asset_img 8.png %}

# 计算面积

设置完上述这些参数后，依次点击Analyze→Analyze Particles，然后在弹窗中设置参数：

{% asset_img 9.png %}

设置完成后点击`OK`即可：

{% asset_img 10.png %}

左边的弹窗是总面积数，右边的弹窗是每个叶片的面积。单位mm$^2$。

保存结果即可。

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
