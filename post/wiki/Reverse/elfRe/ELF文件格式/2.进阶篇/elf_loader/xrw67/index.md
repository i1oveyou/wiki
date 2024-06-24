---
title: wiki-Reverse-elfRe-ELF文件格式-2.进阶篇-elf_loader-xrw67
---
一个加载so的loader

加载指定函数....这个函数必须得是一个已经导出的函数,,也就是有对应的符号的

所以的话,,,如果我们拿着这个项目去加载一个elf的话...elf是不会导出函数的名字的



有些字段没有,并不影响elf的运行

比如没有rel, rel.plt.....

如果有,,,同时还处理失败,,那才是真正的加载失败

比如有些elf没有symtab一样可以运行的





fini/init

ep

main
