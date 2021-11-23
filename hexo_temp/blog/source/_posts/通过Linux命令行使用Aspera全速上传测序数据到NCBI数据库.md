---
title: 通过Linux命令行使用Aspera全速上传测序数据到NCBI数据库
tags: 生物信息学
categories: 生物信息学
abbrlink: b213e513
date: 2020-01-07 18:48:21
---

每试错一次，就离本质就更近一步。----小蓝哥

------

# 为什么要上传数据

实验室同学找我帮忙上传宏基因组数据到NCBI，大概是45G。NCBI提供了很多种可供选择的上传方式：

<!-- more -->

{% asset_img 1.png %}

没有海外节点 **+** 学校的龟速网速，网页上传的速度可想而知，ftp又很容易断，据说Aspera上传能够达到满速上传，就想试一下。

Aspera有浏览器插件，下载试了几次都不行。决定试一下命令行方式。前前后后上传了大约100G数据，终于把这种满速上传数据的方法掌握了。

命令行方式分成Windows下的方式和Linux命令行模式，Windows还需要配制环境变量，比较麻烦，索性采用Linux命令行上传。

------

# 电脑配置

Oracle VM VirtualBox 虚拟机配Ubuntu 18.0操作系统 + FinalShell。虚拟机当个小服务器，FinalShell是国产的Shell，目前接触过的Shell中比较好用的。

{% asset_img 2.png %}

------

# 软件准备

第一步是get到Aspera的Linux版本：

{% asset_img 3.png %}

下载好了之后把本地文件upload到服务器上，然后：

run一下：

> aspera-cli-x.x.x.xxx.xxxxxxx-linux-64-release.sh

添加可执行权限：

> \# chmod +x aspera-cli-x.x.x.xxx.xxxxxxx-linux-xx-release.sh

添加环境变量：

> \# export PATH=~/.aspera/cli/bin:$PATH

我也不知道这个是干啥的，反正复制粘贴run就行：

> \# export MANPATH=~/.aspera/cli/share/man:$MANPATH

Aspera安装配置完成，下面就是上传数据了。

------

# 开始吧、、、、

首先，把硬盘里的数据上传到服务器：

{% asset_img 4.png %}

记得数据上传的**绝对路径**。

然后，我们回到NCBI---------

下载这个key file 并上传到服务器，记得上传的**绝对路径**。一定要记得这个东西！！！！！！！！！！！！！！！！！！！！！！

→

{% asset_img 5.png %}

先看看NCBI给的例子：

> ascp -i <path/to/key_file> -QT -l100m -k1 -d<path/to/folder/containing files>subasp@upload.ncbi.nlm.nih.gov:uploads/13××××××_qq.com_Ofc5bvIL

这些命令都是什么意思呢：

-QT我不知道，也不想知道。

-l100m意思是最大网速，Aspera据说是满速上传，这个设置几乎没什么意义，高兴就设置到1000m吧。

-k1指的是断点续传，这个很重要哟，看中的就是Aspera的断点续传和满速上传。

subasp@upload.ncbi.nlm.nih.gov:uploads/13××××××_qq.com_Ofc5bvIL这个是NCBI分配给每个上传er的，是独一无二的。

别的参数不用知道，直接拿轮子用就行。

**我第一次上传的时候是这样的：**

> **ascp -i /home/lixiang01/aspera.openssh -QT -l100m -k1 d /home/lixiang01/data/\*.gz subasp@upload.ncbi.nlm.nih.gov:uploads/123××××××_qq.com_Ofc5bvIL**

数据倒是全部上传完成了，但是我后续找不到数据啊啊啊啊啊啊啊啊啊啊啊啊----

找了找原因，发现了：

**If you upload your files in your root directory, you will not be able to see them or to select the folder during the submission**.Make a new subdirectory for each new submission. Your submission subfolder is a temporary holding area and it will be removed once the whole submission is complete.Do not upload complex directory structures or files that do not contain sequence data.

原来是因为我上传的时候直接上传到NCBI分配给我的root目录了，导致后面无法选择选择预上传完成的文件，于是，机智的我修改了一下命令：

> ascp-i /home/lixiang01/aspera.openssh-QT -l100m -k1 d /home/lixiang01/data/*.gzsubasp@upload.ncbi.nlm.nih.gov:uploads/123××××××_qq.com_Ofc5bvIL/**sra_data**

对，我就是简单的加了个“**/sra_data**”，简单的在root目录下创建了一个子目录 **sra_data**，结果，上传成功了。（这个可以随便取名字的，高兴就好）

------

**看使用说明和帮助文档真的很重要！！！**

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
