---
title: 清理WinSXS文件夹
date: 2020-12-25 16:19:58
tags: 技能
categories: 技能
---

以管理员身份运行`cmd`命令行，输入下方代码即可:

```c
Dism /online /Cleanup-Image /StartComponentCleanup
```

