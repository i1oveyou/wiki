---
title: wiki-Reverse-elfRe-ELF文件格式-2.进阶篇-elf_loader
---


我感觉以后分析项目的话

还是现分析简单的,普通的项目





Github项目

```
https://github.com/MikhailProg/elf ;这个更加离谱..假巴意思去加载elf,,但是有些语法,写得函数不错的(√)
https://github.com/niicoooo/esp32-elfloader ;基于x86的,好像有点过时了,但是好像很全面,,没有去分析(X)
https://github.com/xrw67/elfloader ;这是不是elfloader,它更像是加载指定dll的指定导出函数..所以在有些处理上不是很到位(√)
https://github.com/espmaniac/elf_loader ;基于https://github.com/niicoooo/esp32-elfloader (X)
https://github.com/gabriel-rusu/E.L.F-Executable-Loader () ;也是基于x86的,而且代码量还比较的少(X)
```



比较庞大复杂的项目

```
https://github.com/serge1/ELFIO (√) 这个项目的demo很多,比如添加一个节区什么的...项目结构不是很乱
https://github.com/akawashiro/sloader ;感觉这个项目很乱 (X)
```





其实感觉分为2大类

1), 直接加载,从ep那里运行

2), 加载后,从指定函数哪里运行,,比如main



 





