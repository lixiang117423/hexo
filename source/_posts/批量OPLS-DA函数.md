---
title: 批量OPLS-DA函数
date: 2020-12-31 12:08:27
tags: R语言
categories: R语言
---

每次分组过多都要写`for`循环，还容易出错，直接写个函数搞定！

<!-- more -->

```R
multi_opls <- function(df, group, method){
  # load  packages
  library(ropls)
  colnames(group) <- c('sample','group_name')
  group[,2] = as.character(group[,2])
  group_num <- as.numeric(length(unique(group[,2])))
  group_unique <- as.character(unique(group[,2]))
  
  for (i in 1:(group_num - 1)) {
    for (j in (i+1):group_num) {
      
      dir.create(paste(group_unique[i],' VS ',group_unique[j], sep = ''))
      selected_group <- c(group_unique[i],group_unique[j])
      group_sub <- dplyr::filter(group, group_name %in% selected_group)
      df_sub <- df[group_sub$sample,]
      
      if (method == 'opls') {
        opls_res <- opls(df_sub,group_sub$group_name)
        
        sample_scores <- as.data.frame(opls_res@scoreMN)
        loading_scores <- as.data.frame(opls_res@loadingMN)
        modelDF <- as.data.frame(opls_res@modelDF)
        vip_value <- as.data.frame(opls_res@vipVn)
      }
      else {
        oplsda_res <- opls(df_sub,
                           group_sub$group_name,
                           predI = 1,
                           orthoI = NA)
        
        sample_scores <- as.data.frame(oplsda_res@scoreMN)
        loading_scores <- as.data.frame(oplsda_res@loadingMN)
        modelDF <- as.data.frame(oplsda_res@modelDF)
        vip_value <- as.data.frame(oplsda_res@vipVn)
      }
      write.csv(sample_scores, 
                file = paste(group_unique[i],' VS ',group_unique[j],
                             '/',
                             'sample_scores.csv',sep = ''))
      write.csv(loading_scores, 
                file = paste(group_unique[i],' VS ',group_unique[j],
                             '/',
                             'loading_scores.csv',sep = ''))
      write.csv(modelDF, 
                file = paste(group_unique[i],' VS ',group_unique[j],
                             '/',
                             'modelDF.csv',sep = ''))
      write.csv(vip_value, 
                file = paste(group_unique[i],' VS ',group_unique[j],
                             '/',
                             'vip_value.csv',sep = ''))
  }
}
}
```

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com