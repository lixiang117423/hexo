---
title: '我的统计函数:stat_xiang'
tags: R语言
categories: R语言
abbrlink: 4b6eae4d
date: 2021-01-04 08:46:58
---

常用的基础统计函数每次都要对统计分析的结果进行提取，稍微有些麻烦，索性写个函数，后期封装成R包，方便自己直接调用。

<!-- more -->

```R
library(multcomp)
library(pgirmess)

stat_xiang <- function(df, value, group, method, level){
  df_sub <- df[,c(value, group)]
  colnames(df_sub) <- c('value','group')
  
  # mean, sd, se and number
  number <- as.data.frame(table(df_sub$group))
  colnames(number) <- c('group','number')
  df_sub <- merge(df_sub, number, by = 'group')
  mean_value <- aggregate(df_sub$value, by = list(df_sub$group), FUN = mean)
  colnames(mean_value) <- c('group','mean')
  sd_value <- aggregate(df_sub$value, by = list(df_sub$group), FUN = sd)
  colnames(sd_value) <- c('group','standard_deviation')
  temp_df <- merge(mean_value, sd_value, by = 'group')
  df_sub <- merge(df_sub, temp_df, by = 'group')
  df_sub$standard_error <- df_sub$standard_deviation / sqrt(df_sub$number)
  
  # statistical analysis
  if (length(unique(df_sub$group)) == 2) {
    if (method == 't.test') {
      fit <- t.test(value ~ group, data = df_sub)
      pvalue <- fit[["p.value"]]
      signif <- ifelse(pvalue < 0.001,'***',
                       ifelse(pvalue > 0.001 & pvalue < 0.01, '**',
                              ifelse(pvalue > 0.05, 'NS','*')))
    }
    if (method == 'wilcox') {
      fit <- wilcox.test(value ~ group, data = df_sub)
      pvalue <- fit[["p.value"]]
      signif <- ifelse(pvalue < 0.001,'***',
                       ifelse(pvalue > 0.001 & pvalue < 0.01, '**',
                              ifelse(pvalue > 0.05, 'NS','*')))
    }
    # dataframe for statistical 
    sig <- data.frame(group = unique(df_sub$group),
                      method = method,
                      level = level,
                      pvalue = pvalue,
                      signif = c(signif,''))
    
  }
  if (length(unique(df_sub$group)) > 2) {
    if (method == 'anova') {
      fit <- aov(value ~ group, data = df_sub)
      pvalue <- summary(fit)[[1]][["Pr(>F)"]][1]
      tuk <- glht(fit, linfct = mcp(group = 'Tukey'))
      signif <- cld(tuk, level = level, ddecreasing = TRUE)[["mcletters"]][["Letters"]]
      signif <- as.data.frame(signif)
      colnames(signif) = 'signif'
      signif$group <- rownames(signif)
      signif$method <- method
      signif$pvalue <- pvalue
      signif$level <- level
      
      sig <- signif[,c('group','method','level','pvalue','signif')]
      
    }
    if (method == 'kruskal') {
      fit <- kruskal.test(value ~ group, data = df_sub)
      pvalue <- fit[["p.value"]]
      if (pvalue < 0.05) {
        fit_2 <- as.data.frame(kruskalmc(df_sub$value, df_sub$group, probs = 1-level))
        signif <- as.data.frame(fit_2)
        signif$statistic <- rownames(signif)
        colnames(signif)[2] <- 'group_comp'
        signif$group <- unique(df_sub$group)
        
        sig <- data.frame(group = unique(df_sub$group),
                          method = method,
                          level = level,
                          pvalue = pvalue)
        sig <- merge(signif, sig, by = 'group')
      }else{
        sig <- data.frame(group = unique(df_sub$group),
                          method = method,
                          level = level,
                          pvalue = pvalue,
                          signif = 'NS')
      }
    }
  }
  results <- merge(df_sub,sig, by = 'group', all.x = TRUE)
  
  return(results)
}
```

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com
