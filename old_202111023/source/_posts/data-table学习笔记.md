---
title: data.table学习笔记
tags: R语言
categories: R语言
abbrlink: 9ba8b5f7
date: 2020-12-23 22:04:26
---

后面要处理大量数据，明显感觉到`data.frame`这种格式满足不了大数据要求了，索性把`data.table`学一下。

<!-- more -->

```R
#install.packages('data.table')


# load package
library(data.table)

# read data
dt = fread('flights_2014.csv')
# fread("https://github.com/arunsrinivasan/satrdays-workshop/raw/master/flights_2014.csv")

# check numbers of row and column
nrow(dt)
ncol(dt)

# view names of headers
names(dt)

# head data
head(dt)

# selecting clunms
dt1 = dt[,origin] # return a vector
dt1 = dt[,.(origin)] # retuen a datat.table
dt1 = dt[,c('origin'),with = FALSE]

# keeping a column based on column position
dt2 = dt[,2,with = FALSE]

#selecting multiple columns
dt3 = dt[,.(origin,year,month,hour)]
dt4 = dt[,c(2:4),with = FALSE]

# dropping a columns
dt5 = dt[,!c('origin'),with = FALSE]

# dropping multiple columns
dt6 = dt[,!c('origin','year'),with = FALSE]

# keeping a column that contain 'dep'
dt7 = dt[,names(dt) %like% 'dep',with = FALSE]

# rename
setnames(dt,c('dest'),c('Destination'))

# rename multiple variables
setnames(dt, c('Destination','origin'),c('dest','origin.of.flighr'))

# subsetting rows
dt8 = dt[origin.of.flighr == 'JFK']
dt9 = dt[origin.of.flighr %in% c('JFK','LGA')]

# not subsetting rows
dt10 = dt[!origin.of.flighr %in% c('JFK','LGA')]

# filter based on multiple variables
dt11 = dt[origin.of.flighr == 'JFK' & carrier == 'AA']

# sorting data
dt12 = setorder(dt,origin.of.flighr)
dt13 = setorder(dt,-origin.of.flighr)
dt14 = setorder(dt,origin.of.flighr,-carrier) # ascending then descending

# adding a colume
dt[,dep_sch:=dep_time-dep_delay]

# adding multiple columns
dt[,c('dep_sch','arr_sch'):=list(dep_time-dep_delay,arr_time - arr_delay)]

# if else
dt[,flag:=ifelse(min<50,1,0)]

# subset then subset again
dt[,dep_sch:=dep_time-dep_delay][,.(dep_time,dep_delay,dep_sch)]

# summarize
dt[,.(mean = mean(dep_delay,na.rm = TRUE),
      median = median(arr_delay, na.rm = TRUE),
      min = min(arr_delay, na.rm = TRUE),
      max = max(arr_delay, na.rm = TRUE))]

# summarize multiple columns
dt[,.(mean(arr_delay), mean(dep_delay))]
```

---

>交流请联系：
>
>💌lixiang117423@gmail.com
>
>💌lixiang117423@foxmail.com

