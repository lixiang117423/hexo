---
title: 清理WinSXS文件夹
tags: 技能
categories: 技能
abbrlink: b4fcbbe6
date: 2020-12-25 16:19:58
---

以管理员身份运行`cmd`命令行，输入下方代码即可:

```c
Dism /online /Cleanup-Image /StartComponentCleanup
```

