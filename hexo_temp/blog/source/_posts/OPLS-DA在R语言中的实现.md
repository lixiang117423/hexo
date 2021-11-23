---
title: OPLS-DA在R语言中的实现
tags: R语言
categories: R语言
abbrlink: 3f4f7ea1
date: 2020-12-13 16:23:51
---

主成分分析（Principal Component Analysis，PCA）是一种无监督降维方法，能够有效对高维数据进行处理。但PCA对相关性较小的变量不敏感，而PLS-DA（Partial Least Squares-Discriminant Analysis，偏最小二乘判别分析）能够有效解决这个问题。而OPLS-DA（正交偏最小二乘判别分析）结合了正交信号和PLS-DA来筛选差异变量。

<!-- more -->

{% asset_img 0.png %} 

图片来自：https://www.r-bloggers.com/2013/07/orthogonal-partial-least-squares-opls-in-r/

# 安装和加载包

```R
# install ropls
if (F) {
  if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
  
  BiocManager::install("ropls")
}

# load  packages
library(ropls)
library(ggplot2)
library(ggsci)
library(Cairo)
library(tidyverse)
library(extrafont)
loadfonts()
```

# 示例数据

```R
# load data
data(sacurine)
names(sacurine)

# view data information
attach(sacurine)
strF(dataMatrix)
strF(sampleMetadata)
strF(variableMetadata)
```

这个数据集是不同年龄、性别和BMI的183个人的尿液中109种代谢物的浓度差异$^{[1]}$。下面的分析主要以性别为变量来研究不同性别人群尿液种代谢物的差异。下面的分析主要包含PCA、PLS-DA和OPLS-DA。

#　PCA分析

```R
# PCA analysis
pca = opls(dataMatrix)
genderFc = sampleMetadata[, "gender"]

pdf(file = 'figures/PCA.pdf', width = 5, height = 5)
plot(pca, typeVc = "x-score",
     parAsColFcVn = genderFc, parEllipsesL = TRUE)
dev.off()
```

{% asset_img 1.jpg %}

可以看到的是如果用PCA的话，不同性别的人群是混在一起的。

# PLS-DA

```R
# PLSDA analysis
plsda = opls(dataMatrix,genderFc)

# sample scores plot
sample.score = plsda@scoreMN %>% 
  as.data.frame() %>%
  mutate(gender = sacurine[["sampleMetadata"]][["gender"]])
  
p1 = ggplot(sample.score, aes(p1, p2, color = gender)) +
  geom_hline(yintercept = 0, linetype = 'dashed', size = 0.5) +
  geom_vline(xintercept = 0, linetype = 'dashed', size = 0.5) +
  geom_point() +
  geom_point(aes(-10,-10), color = 'white') +
  labs(x = 'P1(10.0%)',y = 'P2(9%)') +
  stat_ellipse(level = 0.95, linetype = 'solid', 
               size = 1, show.legend = FALSE) +
  scale_color_manual(values = c('#008000','#FFA74F')) +
  theme_bw() +
  theme(legend.position = c(0.9,0.8),
    legend.text = element_text(color = 'black',size = 12, family = 'Arial', face = 'plain'),
    panel.background = element_blank(),
    panel.grid = element_blank(),
    axis.text = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
    axis.title = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
    axis.ticks = element_line(color = 'black'))
ggsave(p1, filename = 'figures/pls.pdf', 
       width = 5, height = 5, device = cairo_pdf)
```

{% asset_img 2.jpg %}

和PCA相比，PLS-DA的效果相对较好。PLS-DA分析的目的是找到差异变量（本例中的109种代谢物的某几种）。因此，需要找到VIP值大于1的变量（代谢物）：

```R
# VIP scores plot
vip.score = as.data.frame(plsda@vipVn)
colnames(vip.score) = 'vip'
vip.score$metabolites = rownames(vip.score)
vip.score = vip.score[order(-vip.score$vip),]
vip.score$metabolites = factor(vip.score$metabolites,
                               levels = vip.score$metabolites)

loading.score = plsda@loadingMN %>% as.data.frame()
loading.score$metabolites = rownames(loading.score)

all.score = merge(vip.score, loading.score, by = 'metabolites')

all.score$cat = paste('A',1:nrow(all.score), sep = '')

p2 = ggplot(all.score[all.score$vip >= 1,], aes(cat, vip)) +
  geom_segment(aes(x = cat, xend = cat,
                   y = 0, yend = vip)) +
  geom_point(shape = 21, size = 5, color = '#008000' ,fill = '#008000') +
  geom_point(aes(1,2.5), color = 'white') +
  geom_hline(yintercept = 1, linetype = 'dashed') +
  scale_y_continuous(expand = c(0,0)) +
  labs(x = '', y = 'VIP value') +
  theme_bw() +
  theme(legend.position = 'none',
        legend.text = element_text(color = 'black',size = 12, family = 'Arial', face = 'plain'),
        panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.text.x = element_text(angle = 90),
        axis.title = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.ticks = element_line(color = 'black'),
        axis.ticks.x = element_blank())
ggsave(p2, filename = 'figures/pls_VIP.pdf', 
       width = 8, height = 5, device = cairo_pdf)
```

下面这些物质就是差异代谢物（VIP值大于等于1）：

```R
 [1] (gamma)Glu-Leu/Ile                                                                  
 [2] 2-acetamido-4-methylphenyl acetate                                                  
 [3] 2-Methylhippuric acid                                                               
 [4] 3-Methylcrotonylglycine                                                             
 [5] 3,4-Dihydroxybenzeneacetic acid                                                     
 [6] 3,5-dihydroxybenzoic acid/3,4-dihydroxybenzoic acid                                 
 [7] 4-Acetamidobutanoic acid isomer 3                                                   
 [8] 6-(carboxymethoxy)-hexanoic acid                                                    
 [9] Acetaminophen glucuronide                                                           
[10] Acetylphenylalanine                                                                 
[11] alpha-N-Phenylacetyl-glutamine                                                      
[12] Asp-Leu/Ile isomer 1                                                                
[13] Citric acid                                                                         
[14] Dehydroepiandrosterone 3-glucuronide                                                
[15] Dehydroepiandrosterone sulfate                                                      
[16] Gluconic acid and/or isomers                                                        
[17] Glucuronic acid and/or isomers                                                      
[18] Glyceric acid                                                                       
[19] Hippuric acid                                                                       
[20] Hydroxybenzyl alcohol isomer                                                        
[21] Malic acid                                                                          
[22] Methyl (hydroxymethyl)pyrrolidine-carboxylate/Methyl (hydroxy)piperidine-carboxylate
[23] Monoethyl phthalate                                                                 
[24] N-Acetyl-aspartic acid                                                              
[25] Oxoglutaric acid                                                                    
[26] p-Anisic acid                                                                       
[27] p-Hydroxyhippuric acid                                                              
[28] Pantothenic acid                                                                    
[29] Pentose                                                                             
[30] Phe-Tyr-Asp (and isomers)                                                           
[31] Pyruvic acid                                                                        
[32] Testosterone glucuronide                                                            
[33] Threonic acid/Erythronic acid                                                       
[34] Valerylglycine isomer 1                                                             
[35] Valerylglycine isomer 2                                                              
```

将它们的VIP值得进行可视化（某些代谢物名称太长，进行转换表示）：

{% asset_img 3.jpg %}

# OPLS-DA分析

```R
# OPLS-DA analysis
oplsda = opls(dataMatrix, genderFc, predI = 1, orthoI = NA)

# sample scores plot
sample.score = oplsda@scoreMN %>% 
  as.data.frame() %>%
  mutate(gender = sacurine[["sampleMetadata"]][["gender"]],
         o1 = oplsda@orthoScoreMN[,1])

p3 = ggplot(sample.score, aes(p1, o1, color = gender)) +
  geom_hline(yintercept = 0, linetype = 'dashed', size = 0.5) +
  geom_vline(xintercept = 0, linetype = 'dashed', size = 0.5) +
  geom_point() +
  #geom_point(aes(-10,-10), color = 'white') +
  labs(x = 'P1(5.0%)',y = 'to1') +
  stat_ellipse(level = 0.95, linetype = 'solid', 
               size = 1, show.legend = FALSE) +
  scale_color_manual(values = c('#008000','#FFA74F')) +
  theme_bw() +
  theme(legend.position = c(0.1,0.85),
        legend.title = element_blank(),
        legend.text = element_text(color = 'black',size = 12, family = 'Arial', face = 'plain'),
        panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.title = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.ticks = element_line(color = 'black'))
ggsave(p3, filename = 'figures/opls.pdf', 
       width = 5, height = 5, device = cairo_pdf)
```

{% asset_img 4.jpg %}

可以看到的是OPLS-DA的效果比PLS-DA更好一些。

同样进行差异代谢物筛选：

```R
# VIP scores plot
vip.score = as.data.frame(oplsda@vipVn)
colnames(vip.score) = 'vip'
vip.score$metabolites = rownames(vip.score)
vip.score = vip.score[order(-vip.score$vip),]
vip.score$metabolites = factor(vip.score$metabolites,
                               levels = vip.score$metabolites)

loading.score = oplsda@loadingMN %>% as.data.frame()
loading.score$metabolites = rownames(loading.score)

all.score = merge(vip.score, loading.score, by = 'metabolites')

all.score$cat = paste('A',1:nrow(all.score), sep = '')

p4 = ggplot(all.score[all.score$vip >= 1,], aes(cat, vip)) +
  geom_segment(aes(x = cat, xend = cat,
                   y = 0, yend = vip)) +
  geom_point(shape = 21, size = 5, color = '#008000' ,fill = '#008000') +
  geom_point(aes(1,2.5), color = 'white') +
  geom_hline(yintercept = 1, linetype = 'dashed') +
  scale_y_continuous(expand = c(0,0)) +
  labs(x = '', y = 'VIP value') +
  theme_bw() +
  theme(legend.position = 'none',
        legend.text = element_text(color = 'black',size = 12, family = 'Arial', face = 'plain'),
        panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.text.x = element_text(angle = 90),
        axis.title = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.ticks = element_line(color = 'black'),
        axis.ticks.x = element_blank())
p4
ggsave(p4, filename = 'figures/opls_VIP.pdf', 
       width = 8, height = 5, device = cairo_pdf)
```

下面的的是差异代谢物：

```R
 [1] (gamma)Glu-Leu/Ile                                                                  
 [2] 2-acetamido-4-methylphenyl acetate                                                  
 [3] 2-Methylhippuric acid                                                               
 [4] 3-Methylcrotonylglycine                                                             
 [5] 3,4-Dihydroxybenzeneacetic acid                                                     
 [6] 3,5-dihydroxybenzoic acid/3,4-dihydroxybenzoic acid                                 
 [7] 4-Acetamidobutanoic acid isomer 3                                                   
 [8] 6-(carboxymethoxy)-hexanoic acid                                                    
 [9] Acetaminophen glucuronide                                                           
[10] Acetylphenylalanine                                                                 
[11] alpha-N-Phenylacetyl-glutamine                                                      
[12] Asp-Leu/Ile isomer 1                                                                
[13] Citric acid                                                                         
[14] Dehydroepiandrosterone 3-glucuronide                                                
[15] Dehydroepiandrosterone sulfate                                                      
[16] Gluconic acid and/or isomers                                                        
[17] Glucuronic acid and/or isomers                                                      
[18] Glyceric acid                                                                       
[19] Hippuric acid                                                                       
[20] Hydroxybenzyl alcohol isomer                                                        
[21] Malic acid                                                                          
[22] Methyl (hydroxymethyl)pyrrolidine-carboxylate/Methyl (hydroxy)piperidine-carboxylate
[23] Monoethyl phthalate                                                                 
[24] N-Acetyl-aspartic acid                                                              
[25] Oxoglutaric acid                                                                    
[26] p-Anisic acid                                                                       
[27] p-Hydroxyhippuric acid                                                              
[28] Pantothenic acid                                                                    
[29] Pentose                                                                             
[30] Phe-Tyr-Asp (and isomers)                                                           
[31] Pyruvic acid                                                                        
[32] Testosterone glucuronide                                                            
[33] Threonic acid/Erythronic acid                                                       
[34] Valerylglycine isomer 1                                                             
[35] Valerylglycine isomer 2                                                             
```

{% asset_img 5.jpg %}

# 模型训练与预测

这些降维的方法都属于机器学习算法，那就可以对模型进行训练，并用这个模型去预测未知的数据。

模型训练很简单：

```R
# model training
oplsda.2 = opls(dataMatrix, genderFc, predI = 1, orthoI = NA,subset = "odd") 
```

```R
OPLS-DA
92 samples x 109 variables and 1 response
standard scaling of predictors and response(s)
      R2X(cum) R2Y(cum) Q2(cum)
Total     0.26    0.825   0.608
      RMSEE RMSEP pre ort
Total 0.213 0.341   1   2
Warning message:
'permI' set to 0 because train/test partition is selected.
```

可以看到使用了92个样本进行训练。

先看看模型在训练集上的准确率：

```R
# 模型在训练集上的准确率
trainVi = getSubsetVi(oplsda.2)
tab = table(genderFc[trainVi], fitted(oplsda.2))
print(paste('模型准确率：',round(sum(diag(tab))/sum(tab)*100, 2),'%', sep = ''))
```

```R
   M  F
  M 50  0
  F  0 42
[1] "模型准确率：100%"
```

看模型在训练集上的准确率是没有什么意义的，要是在训练集的表现都不好，那模型一定不好。那看看模型在未知数据上的预测准确率吧：

```R
# model on test data
tab2 = table(genderFc[-trainVi],predict(oplsda.2, dataMatrix[-trainVi, ]))
print(paste('模型准确率：',round(sum(diag(tab2))/sum(tab2)*100, 2),'%', sep = ''))
```

```R
     M  F
  M 43  7
  F  7 34
[1] "模型准确率：84.62%"
```

这个准确率已经很棒了。

# 差异代谢物其他筛选方法

除了用(O)PLS-DA中的VIP值对代谢物进行筛选，还可以用别的方法进行筛选，如`log2FC`等。通常是绘制火山图。

```R
# volcano plot
df = dataMatrix %>% as.data.frame()
df$gender = sacurine[["sampleMetadata"]][["gender"]]
df = df[order(df$gender),]
df = df[,-110]

M.mean = apply(df[1:100,],2,FUN = mean)
F.mean = apply(df[101:183,],2,FUN = mean)

FC = M.mean / F.mean
log2FC = log(FC,2)

pvalue = apply(df, 2, function(x)
  {t.test(x[1:100],x[101:183])$p.value})

p.adj = p.adjust(pvalue, method = 'BH')
p.adj.log = -log10(p.adj)

colcano.df = data.frame(log2FC,p.adj, p.adj.log)
colcano.df$cat = ifelse(colcano.df$log2FC >= 1 & colcano.df$p.adj < 0.05,'Up',
                        ifelse(colcano.df$log2FC <= -1 & colcano.df$p.adj < 0.05,'Down','NS'))

p5 = ggplot(colcano.df, aes(log2FC, p.adj.log)) +
  geom_point() +
  labs(y = '-log10(p-value.adj)') +
  theme_bw() +
  theme(legend.position = 'none',
        legend.text = element_text(color = 'black',size = 12, family = 'Arial', face = 'plain'),
        panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.text.x = element_text(angle = 90),
        axis.title = element_text(color = 'black',size = 15, family = 'Arial', face = 'plain'),
        axis.ticks = element_line(color = 'black'),
        axis.ticks.x = element_blank())
p5
ggsave(p5, filename = '20201214PLSDA分析/figures/volcano.pdf', 
       width = 5, height = 5, device = cairo_pdf)
```

{% asset_img 6.jpg %}

可能是这个例子中的代谢物太少了，导致算完以后都没有差异代谢物了。

# 参考文献

>[1] Thévenot E A, Roux A, Xu Y, et al. Analysis of the human adult urinary metabolome variations with age, body mass index, and gender by implementing a comprehensive workflow for univariate and OPLS statistical analyses[J]. ***Journal of proteome research***, 2015, 14(8): 3322-3335.

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

