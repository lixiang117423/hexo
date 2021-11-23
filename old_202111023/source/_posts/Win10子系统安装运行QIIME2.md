---
title: "\x96Win10子系统安装运行QIIME2"
tags: 生物信息学
categories: 生物信息学
abbrlink: c539b14f
date: 2021-07-03 15:36:31
---

下载最新文件：

[https://docs.qiime2.org/2021.4/](https://docs.qiime2.org/2021.4/)

[https://docs.qiime2.org/2021.4/install/native/](https://docs.qiime2.org/2021.4/install/native/)

<!-- more -->

```PowerShell
# These instructions are identical to the Linux (64-bit) instructions
wget https://data.qiime2.org/distro/core/qiime2-2021.4-py38-linux-conda.yml
conda env create -n qiime2-2021.4 --file qiime2-2021.4-py38-linux-conda.yml
# OPTIONAL CLEANUP
rm qiime2-2021.4-py38-linux-conda.yml
```


下载示例数据：

[https://data.qiime2.org/2021.4/tutorials/atacama-soils/sample_metadata.tsv](https://data.qiime2.org/2021.4/tutorials/atacama-soils/sample_metadata.tsv)

[https://data.qiime2.org/2021.4/tutorials/atacama-soils/10p/forward.fastq.gz](https://data.qiime2.org/2021.4/tutorials/atacama-soils/10p/forward.fastq.gz)

[https://data.qiime2.org/2021.4/tutorials/atacama-soils/10p/reverse.fastq.gz](https://data.qiime2.org/2021.4/tutorials/atacama-soils/10p/reverse.fastq.gz)

[https://data.qiime2.org/2021.4/tutorials/atacama-soils/10p/barcodes.fastq.gz](https://data.qiime2.org/2021.4/tutorials/atacama-soils/10p/barcodes.fastq.gz)

开始分析：

- 首先是导入数据：

```PowerShell
# 双末端测序二数据<br />qiime tools import --type EMPPairedEndSequences --input-path ./data --output-path ./data/emp-paired-end-sequences.qza
```


- 去除barcode:

```PowerShell
qiime demux emp-paired \
  --m-barcodes-file sample-metadata.tsv \
  --m-barcodes-column barcode-sequence \
  --p-rev-comp-mapping-barcodes \
  --i-seqs emp-paired-end-sequences.qza \
  --o-per-sample-sequences demux-full.qza \
  --o-error-correction-details demux-details.qza
```


- 抽样：

```PowerShell
qiime demux subsample-paired \
  --i-sequences demux-full.qza \
  --p-fraction 0.3 \
  --o-subsampled-sequences demux-subsample.qza

qiime demux summarize \
  --i-data demux-subsample.qza \
  --o-visualization demux-subsample.qzv
```


- 导出数据

```PowerShell
qiime tools export \
  --input-path demux-subsample.qzv \
  --output-path ./demux-subsample/

qiime demux filter-samples \
  --i-demux demux-subsample.qza \
  --m-metadata-file ./demux-subsample/per-sample-fastq-counts.tsv \
  --p-where 'CAST([forward sequence count] AS INT) > 100' \
  --o-filtered-demux demux.qza
```


- 注释

```PowerShell
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux.qza \
  --p-trim-left-f 13 \
  --p-trim-left-r 13 \
  --p-trunc-len-f 150 \
  --p-trunc-len-r 150 \
  --o-table table.qza \
  --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats denoising-stats.qza
```


- 获取特征表

```PowerShell
qiime feature-table summarize \
  --i-table table.qza \
  --o-visualization table.qzv \
  --m-sample-metadata-file sample-metadata.tsv

qiime feature-table tabulate-seqs \
  --i-data rep-seqs.qza \
  --o-visualization rep-seqs.qzv

qiime metadata tabulate \
  --m-input-file denoising-stats.qza \
  --o-visualization denoising-stats.qzv
```


- 导出数据

```PowerShell
qiime tools export --input-path table.qza --output-path ../results/
```

>💌lixiang117423@foxmail.com
>💌lixiang117423@gmail.com