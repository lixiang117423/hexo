---
title: Ubuntu更新R
tags: R语言
categories: R语言
abbrlink: 4fa06897
date: 2021-01-09 10:42:25
---

123参考链接：https://blog.csdn.net/weixin_41929524/article/details/108470515

```shell
sudo su
echo "deb http://www.stats.bris.ac.uk/R/bin/linux/ubuntu xenial-cran40/" >> /etc/apt/sources.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
apt-get update
apt-get upgrade

sudo apt-getinstall r-base
sudo apt-get install r-base-dev
```

---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

