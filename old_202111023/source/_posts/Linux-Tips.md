---
title: Linux Tips
tags: Linux
categories: Linux
abbrlink: 2f176420
date: 2021-04-05 16:56:33
---

1. 统计某个特定字符串出现的次数：

   ```shell
   grep -c '>' filename
   ```

   <!-- more -->

2. 查看某个特定字符出现的行数：

   ```R
   grep -n '>' filename
   ```

3. 根据`gff`文件提取基因序列：

   ```shell
   awk '{if ($3=="gene") print}' ylg.gff3 > ylg.gene.gff3
   bedtools getfasta -fi your_fasta.file -bed your_gff3.file > your_output.name
   ```

4. 统计文件行数：

   ```shell
   wc -l your_file
   ```

5. 修改`atp`源：

   ```shell
   # 备份源
   sudo cp /etc/apt/sources.list  /etc/apt/sources.list_backup
   # 编辑源
   sudo vi /etc/apt/sources.list
   
   deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
   ```

6. `conda`安装：

   ```shell
   wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
   
   bash Miniconda2-latest-Linux-x86_64.sh
   
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda
   conda config --set show_channel_urls yes
   
   conda create -n rna
   # 创建一个小环境名为rna
   
   conda install python=2
   # 安装python 2版本
   # 以上两句话可以等同于一句命令：conda create -n rna python=2
   
   conda info -e
   conda info --envs
   conda env list
   # 都是来查看已经存在小环境名的
   
   # 运行后如下：rna即为刚刚建立成功的小环境名
   
   $ conda info -e
   # conda environments:
   #
   base                  *  /home/you/miniconda2
   rna                      /home/you/miniconda2/envs/rna
   
   source activate rna
   ```

7. 安装`htop`：

   ```shell
   sudo apt install htop
   ```

8. `wget`后台运行+断点续传：

   ```shell
   wget -b -c your_link
   ```

9. 查看某个文件夹的大小：

   ```shell
   du -h youdir
   ```

10. `wegt`批量下载：

    ```shell
    wget -c -b -t 0 -T 6000 -i yourlinkesfiles
    ```
    
11. 服务器之间传输文件：

    ```shell
    scp -r ./thisfolder username@192.168.212.212:/home/user $ 目标服务器
    ```

12. md5值检验：

    ```shell
    md5sum yourfile
    ```

    

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com

