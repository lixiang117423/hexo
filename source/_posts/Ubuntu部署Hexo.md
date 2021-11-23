---
title: Ubuntu部署Hexo
cover: /img/cover/hexo.png
toc: true
toc_number: 4
mathjax: true
katex: true
date: 2021-11-23 16:25:32
updated:
tags:
categories:
keywords:
description:
top_img:
comments:
copyright:
copyright_author:
copyright_author_href:
copyright_url:
copyright_info:
aplayer:
highlight_shrink:
aside:
---

```shell
# 添加用户
adduser hexo

# 切回用户目录
su hexo

# 新建目录存放blog
mkdir blog

# 初始化裸git
git init --bare hexo.git

# 可选
vim blog.git/hooks/post-receive

# 修改权限
chmod +x blog.git/hooks/post-receive

# 修改nginx默认目录
sudo vim /etc/nginx/sites-available/default
root /var/www/html; 
root /home/hexo/blog;

# 修改hexo配置
# Deployment
## Docs: https://hexo.io/docs/one-command-deployment
deploy:
  type: git
  repo: hexo@106.55.94.9:/home/hexo/blog.git
  branch: master                           
  message: '站点更新:{{now("YYYY-MM-DD HH:mm:ss")}}'
```

将本地hexo推送到服务器端即可。刷新Nginx即可访问。

如果发现部署不上，先把本地文件`known_hosts`里面对应的ssh记录先删除。然后把对应的文件拷贝上去：

```shell
scp ~/.ssh/id_rsa.pub hexo@xxxxxx:/home/hexo/.ssh/Jking.pub
```



---

💌lixiang117423@foxmail.com
💌lixiang117423@gmail.com