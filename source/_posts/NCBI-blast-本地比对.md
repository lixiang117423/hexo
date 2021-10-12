---
title: NCBI blast 本地比对
tags: 数据库
categories: 数据库
abbrlink: 8de48821
date: 2021-04-11 15:30:56
---

# 安装 Blast +

将下载的[安装包](https://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/)解压缩后安装对应的`.exe`文件即可，安装完成后将安装目录下的`bin`文件夹的路径添加到环境变量中的`Path`中。

<!-- more -->

ftp://ftp.ncbi.nlm.nih.gov/blast/db/

# 构建比对数据库

可以利用自带的函数下载数据库：

```shell
nohup perl update_blastdb.pl --decompress nt &> update.log &
```

```shell
makeblastdb -in swissprot -dbtype prot -out swissprot.blast
```

>- -in: 待格式化的序列文件     
>- -dbtype: 数据库类型，nucl 为核酸，prot 为蛋白  
>- -out: 输出数据库名，可用于后续 -db 参数设置

# 比对

```shell
blastn -query AE014075.fasta -db /e/Blast+/database/test/res_genome.blast -out 20210421test.txt -evalue 1e-5 -outfmt 6
```

>- -query: 输入文件路径及文件名
>- -out: 输出文件路径及文件名
>- -db: 格式化了的数据库路径及数据库名
>- -outfmt: 输出文件格式，共 12 种，6 是 tabular 格式对应 BLAST 的 m8 格式
>- -evalue: 设置输出结果的 e-value 值，e 值越小最后结果可信度越

#  结果解读

[1] Query id：已知的序列 ID

[2] Subject id: 比对到数据库中的序列 ID

[3] % identity : 相似度(在氨基酸水平上，相似度可以设置为 30，严格一些可以设置为 70；在核苷酸水上，可以设置 70 或 90。没有统一的标准，还是以特定研究的参考文献为准。)

[4] alignment length：比对长度

[5] mismatches ：错配数目

[6] gap openings：gap 的数目

[7] q. Start：已知的序列比对起始位置

[8] q. End：已知的序列比对终止位置

[9] s. Start：数据库中序列比对起始位置

[10] s. End；数据库中序列比对终止位置

[11] E value；比对的 E 值

[12] score；比对的得分

注意比对到的序列长度。评价一个 blast 结果的标准主要有三项，E 值（Expect)，一致性 (Identities)，缺失或插入（Gaps）。加上比对长度的话，就有四个标准了。

**E 值（Expect)**：表示随机匹配的可能性，例如，E=1，表示在目前大小的数据库中，完全由机会搜到对象数的平均值为 1.E 值越大，随机匹配的可能性也越大。E 值接近零或为零时，具本上就是完全匹配了。通常来讲，我们认为 E 值小于 10-5 就是比较可性的 S 值结果。我们可以想象，相同的数据库，E=0.001 时如果有 1000 条都有机会 S 值比现在这个要高的话，那么不 E 设置为 10-6 时可能就会只得到一条结果，就是 S 值最可靠的那个。但是 E 值也不是万能的。它在以下几个情况下有局限性：

1）当目标序列过小时，E 值会偏大，因为无法得到较高的 S 值。

2）当两序列同源性虽然高，但有较大的 gap（空隙）时，S 值会下降。这个时候 gap scores 就非常有用。

3）有些序列的非功能区有较低的随机性时，可能会造成两序列较高的同源性。

E 值总结：

E 值适合于有一定长度，而且复杂度不能太低的序列。当 E 值小于 10-5

时，表明两序列有较高的同源性，而不是因为计算错误。当 E 值小于 10-6 时，表时两序列的同源性非常高，几乎没有必要再做确认。

**一致性 (Identities)**：或相似性。匹配上的碱基数占总序列长的百分数。

**Score** 得分值越高说明同源性越好；Expect 期望值越小比对结果越好，说明因某些原因而引起的误差越小；Identities 是同源性（相似性），例中所示比对的 1299 个碱基中只有 35 个不配，其他 97％相同；

**Gaps** 是指多出或少的碱基或缺失的碱基数；缺失或插入（Gaps）：插入或缺失。用 "—" 来表示。

此外比对的 **Strand** 则通 s. Start：和 s. End 判断，如上述结果的第三行. Star 值大于 s. End，则表示负链。

#  Blast与Blast+的差异

| **参数**                       | **Blast** | **Blast+**       |
| ------------------------------ | --------- | ---------------- |
| 数据库格式化函数               | formatdb  | makeblastdb      |
| 输入 / 输出                    | -i / -o   | -query / -out    |
| 格式化了的数据库路径及数据库名 | -d        | -db              |
| 输出结果的 e-value 值          | -e        | -evalue          |
| 输出文件格式                   | -m        | -outfmt          |
| 最大目标的数目                 | -v / -b   | -max_target_seqs |

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com