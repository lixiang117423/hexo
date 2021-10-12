---
title: 部署Rshiny到服务器的常见问题
tags: R语言
categories: R语言
abbrlink: '96076236'
date: 2021-01-09 10:53:19
---

# 下载安装Rshiny-server

参考链接：

- https://mp.weixin.qq.com/s?src=11&timestamp=1610162005&ver=2817&signature=BhA59HXhKAj1PYvJS11senjcK8co0LgnZ2iS-7RlClhHqqsESkCMVrw*HFaCnmTHdlC9CiGzbKV*xlzUOr6hXj6vMEo8VADPVLekOzyGi8iB21LHEb7hfvbw85aAE*9n&new=1
- http://m.meiyingqishi.cn/view.php?aid=85

<!-- more  -->

## 安装 R

```shell
sudo echo " debhttps://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/" | sudo tee -a/etc/apt/sources.list
```



- 添加秘钥

  ```shell
  gpg --keyserver keyserver.ubuntu.com --recv-key51716619E084DAB9
  gpg -a --export 51716619E084DAB9 | sudo apt-key add –
  sudo apt-key adv --keyserver keyserver.ubuntu.com--recv-keys E084DAB9
  ```

  

- 更新

  ```shell
  sudo apt-get update
  ```

  

- 安装

  ```shell
  sudo apt-get install r-base r-base-core r-base-dev
  ```

  

## 安装 RStudio Server
```shell
sudo apt-get install gdebi-core
wget https://download2.rstudio.org/server/trusty/amd64/rstudio-server-1.2.1335-amd64.deb
sudo gdebi rstudio-server-1.2.1335-amd64.deb
```



- 启动 / 停止 / 重启

  ```shell
  rstudio-server start# 启动
  rstudio-server stop #停止
  rstudio-server restart #重启
  ```

  

- 配置

  ```shell
  # ip 和端口：
  vi/etc/rstudio/rserver.conf
  www-port=8789 #设置监听端口
  \#www-address=127.0.0.0# 允许访问的 IP 地址，默认 0.0.0.0
  ```

  

- 会话配置：

```shell
vi/etc/rstudio/rsession.conf
session-timeout-minutes=30# 会话超时时间
r-cran-repos=https://my.favorite.cran.mirror#CRAN 资源库
```



5）帐号、访问

访问地址：
http://ip:8789
帐号密码：unbuntu 的帐号密码，注意：不能用 root 帐号
新建帐号：useradd -d/home/ 用户名 -m 用户名 #创建用户的同时指定目录 passwd 用户名 #设置密码

五、安装 Shiny Server
1）安装 shiny 包
sudosu - -c

"R -e"install.packages('shiny',repos='https://cran.rstudio.com/')""

2）查看最新版本
https://www.rstudio.com/products/shiny/download-server/

3）安装 server
sudo apt-getinstall gdebi-core
wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.9.923-amd64.deb
sudo gdebishiny-server-1.5.9.923-amd64.deb

4）启动 / 停止 / 重启 / 状态
sudo systemctl start shiny-server #开启
sudo systemctl stop shiny-server #停止
sudo systemctl restart shiny-server #重启
sudo systemctl status shiny-server #查看状态

5）访问
Http://ip:3838

六、安装 shiny 包
sudo su - -c
"R -e"install.packages (' 包名 ', repos='https://cran.rstudio.com/')""





# 报错信息等

- 如果部署成功后可以正常打开，但是很快显示与服务器断开连接，通常是以为依赖的包没有安装好。

  ```shell
  Disconnected from the server.
  Reload
  ```

- 如果显示下面的图片，通常是R包和R版本冲突，需要重新安装R包。
  {% asset_img 1.png %}

# 用户传入文件

用户传入的文件结构是这样的：

{% asset_img 2.png %}

- 上传多个文件：

  ```R
  fileInput("data_input",
                         label = h4("上传数据"),
                         multiple = TRUE,
                         accept = ".csv",
                         buttonLabel = "浏览...")
  ```

  

