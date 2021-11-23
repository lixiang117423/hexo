---
title: WGS学习笔记
tags: 生物信息学
categories: 生物信息学
abbrlink: 258e55c8
date: 2021-03-01 09:01:06
---

# FASTA和FASTQ文件格式

## FASTA

`FASTA`是已知序列的存储文件，以`>`开头，<!-- more -->紧接着`>`的是该序列的名称，如果是基因名称，那通常是统一的。后面是其他附加信息。第二行才是真真正正的序列，可以是一行，也可以是多行，软件识别`FASTA`文件的时候默认将两个`>`之间的内容识别为一条序列。`FASTA`文件的缩写可以是`.fa`或者`.fa.gz`，前一种是没有压缩的格式，后面一种是压缩格式。

>\>ENSMUSG00000020122|ENSMUST00000138518
>CCCTCCTATCATGCTGTCAGTGTATCTCTAAATAGCACTCTCAACCCCCGTGAACTTGGT
>TATTAAAAACATGCCCAAAGTCTGGGAGCCAGGGCTGCAGGGAAATACCACAGCCTCAGT
>TCATCAAAACAGTTCATTGCCCAAAATGTTCTCAGCTGCAGCTTTCATGAGGTAACTCCA
>GGGCCCACCTGTTCTCTGGT
>\>ENSMUSG00000020122|ENSMUST00000125984
>GAGTCAGGTTGAAGCTGCCCTGAACACTACAGAGAAGAGAGGCCTTGGTGTCCTGTTGTC
>TCCAGAACCCCAATATGTCTTGTGAAGGGCACACAACCCCTCAAAGGGGTGTCACTTCTT
>CTGATCACTTTTGTTACTGTTTACTAACTGATCCTATGAATCACTGTGTCTTCTCAGAGG
>CCGTGAACCACGTCTGCAAT
>
>\>gene_00284728 length=231;type=dna
>GAGAACTGATTCTGTTACCGCAGGGCATTCGGATGTGCTAAGGTAGTAATCCATTATAAGTAACATG
>CGCGGAATATCCGGGAGGTCATAGTCGTAATGCATAATTATTCCCTCCCTCAGAAGGACTCCCTTGC
>GAGACGCCAATACCAAAGACTTTCGTAAGCTGGAACGATTGGACGGCCCAACCGGGGGGAGTCGGCT
>ATACGTCTGATTGCTACGCCTGGACTTCTCTT

## FASTQ

`FASTQ`则是我们常说的下机数据，长得像这样：

>@DJB775P1:248:D0MDGACXX:7:1202:12362:49613
>TGCTTACTCTGCGTTGATACCACTGCTTAGATCGGAAGAGCACACGTCTGAA
>+
>JJJJJIIJJJJJJHIHHHGHFFFFFFCEEEEEDBD?DDDDDDBDDDABDDCA
>@DJB775P1:248:D0MDGACXX:7:1202:12782:49716
>CTCTGCGTTGATACCACTGCTTACTCTGCGTTGATACCACTGCTTAGATCGG
>+
>IIIIIIIIIIIIIIIHHHHHHFFFFFFEECCCCBCECCCCCCCCCCCCCCCC

以`@`开头的每4行就是我们常说的`read`。

第一行是每条`read`的标识符，在一个`FASTQ`文件中是不可能重复的，甚至在多个`FASTQ`文件中也是不可能出现重复的。

第二行就是序列了，包含了A、T、C、G及N这5种情况，N表示的是测序仪器无法识别的序列号。

第三行在很老的版本里面是有信息的，通常是重复第一行的信息，现在基本都是只有一个`+`。

第四行是每个剑戟对应的质量值，用`ASCII`进行编码，计算公式为：

$Q = -10log(p_error)$

现在常用的衡量指标是Q20和Q30，分别表示的是100个碱基中出现一个碱基测错的概率和1000个碱基中出现一个碱基测错的概率，对应的正确率分别是99%和99.9%，以此类推，Q40下的正确率应该是99.99%。

## 查看测序所用的质量体系

### `shell`脚本

```shell
less $1 | head -n 1000 | awk '{if(NR%4==0) printf("%s",$0);}' \
| od -A n -t u1 -v \
| awk 'BEGIN{min=100;max=0;} \
{for(i=1;i<=NF;i++) {if($i>max) max=$i; if($i<min) min=$i;}}END \
{if(max<=126 && min<59) print "Phred33"; \
else if(max>73 && min>=64) print "Phred64"; \
else if(min>=59 && min<64 && max>73) print "Solexa64"; \
else print "Unknown score encoding"; \
print "( " min ", " max, ")";}'
```



### `python`

`ord () `函数会将字符转换为 `ASCII` 对应的数字，减掉 33 后就得到了该碱基最后的质量值（即，`Phred quality score`）

```python
In [1]: qual='JJJJJIIJJJJJJHIHHHGHFFFFFFCEEEEEDBD'
In [2]: [ord(q)-33 for q in qual]
Out[2]:
[35, 20, 17, 18, 24, 34, 35, 35, 35, 34, 35, 34, 29, 29, 32, 32, 34, 34, 33, 
29, 33, 33, 32, 35, 35, 35, 34, 34, 34, 34, 35, 35, 34, 35, 34, 35, 34, 35, 
34, 34, 34, 35, 35, 35, 35, 34, 33, 33, 30, 33, 24, 27]
```

# WGS分析流程

可以将WGS分成一下及部分：

1. 原始测序数据的质控
2. read 比对，排序和去除重复序列
3. Indel 区域重（“重新” 的 “重”）比对
4. 碱基质量值重校正
5. 变异检测
6. 变异结果质控和过滤

# 数据质控

为什么要进行数据质控呢？illumina测序的策略是“边合成边测序”，在合成的过程中随着链的增长，DNA聚合酶的效率会降低，于是越到后面的碱基的错误率就会越高。下机数据的质量严重影响着后续的下游分析的结果。

软件是`fastqc`，利用`conda`安装简单：

````shell
conda install fastqc
````

软件的使用也很简单：

```shell
fastqc untreated.fq -o fastqc_out_dir/
```

`-o`表示的是结果输出目录，如果没有指定目录，就会输出到和输入文件一个文件夹。

输入多个文件：

```shell
fastqc /path_to_fq/*.fq -o fastqc_out_dir/
```

质控后数据不好的话需要对数据进行处理，如切除低质量的`reads`及接头序列等。









>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com

