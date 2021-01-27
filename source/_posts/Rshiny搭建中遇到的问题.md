---
title: Rshiny搭建中遇到的问题
date: 2021-01-21 14:24:09
tags: R语言
categories: R语言
---

- 添加其他附件（数据文件读取的时候）的时候需要把这些附件的权限开放，而且要具体到具体的文件。<!-- more -->

  ```shell
  chmod 777 yourfile
  ```

- 传参的时候如果是传入`FALSE`或者`TRUE`这两个逻辑值的时候，需要以字符串的形式传入，然后再变成逻辑值。

- 安装`xlsx`包：

  ```shell
  sudo apt-get install default-jre
  sudo apt-get install default-jdk
  export JAVA_HOME=/usr/lib/jvm/default-java
  export JRE_HOME=${JAVA_HOME}/jre
  export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
  export PATH=${JAVA_HOME}/bin:$PATH
  R CMD javareconf
  install.packages('rJava')
  install.packages('xlsx')
  ```

- `server.R`中的任何函数都不能重名，否则不同的`rabIterm`会出错。

- 递归修改权限:

  ```shell
  chmod -R 777 yourfile
  ```

-  安装`htop`：

   ```shell
   sudo apt-get install htop
   ```

- `git`删除文件夹：

  ```shell
  git rm -r yourfile
  ```

- 安装`Cairo`包：

  ```shell
  apt-get install libcairo2-dev
  apt-get install libxt-dev
  ```

- `sources`代码的时候如果在页面上出现`TRUE`这个单词，那需要在`source`后面加上`$value`：

  ```R
  ui <- source("ui-test.R", local = TRUE)$value
  ```

- 服务器端`Rshiny server`绘图中文出错：先将`windows`下的`fonts`文件上传到服务器端，然后利用R包`showtext`：

  ```R
  showtext_auto()
  font.add("simsun", "/usr/share/fonts/chinese/simsun.tcc") # 你的中文字体位置
  ```

- `chown -R git:git /var/hexo/`报错：先`chattr -i /var/hexo/.user.ini`再运行就可以了。

- 下载压缩文件：

  ```R
  output$download_figure__oplsda <- downloadHandler(
    filename <- function(){
      paste(stringr::str_sub(input$data_input_oplsda$name,
                             1,
                             (nchar(input$data_input_oplsda$name) - 4)),
            'oplsda图片结果.zip',sep = '')
    },
    content <- function(file){
      zip(file,'./results/oplsda/figures/')
    }
  )
  ```

- ````R
  # 安装libgit2
  sudo apt update
  sudo apt install libgit2-dev
  ````
  
- 安装`WGCNA`包使用`CRAN`源可能会报错，使用`BiocManager`进行安装：

  ```R
   BiocManager::install("WGCNA")
  ```

- 安装某个包提示没有空间的时候先吧那个文件夹删除了再进行安装：

  ```R
  installation of package ‘RcppEigen’ had non-zero exit status
  ```

  


---

>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

