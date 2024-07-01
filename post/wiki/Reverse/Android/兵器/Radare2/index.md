---
title: wiki-Reverse-Android-兵器-Radare2
---



# shell指令





 分析一个文件

```
┌──(kali㉿G16-7620)-[/mnt/c/mm_dqx/code/file/apk]
└─$ r2 -A lib-v0.9/arm64-v8a/libnative-lib.so
WARN: Relocs has not been applied. Please use `-e bin.relocs.apply=true` or `-e bin.cache=true` next time
INFO: Analyze all flags starting with sym. and entry0 (aa)
INFO: Analyze imports (af@@@i)
INFO: Analyze entrypoint (af@ entry0)
INFO: Analyze symbols (af@@@s)
...
[0x000052b0]>
```



# 获取导入表信息

```
ii
is
iif
iil
```



# 其shell指令

`af`的意思是”analyze function“。

`afl`可以列出分析中发现的函数。

aaa : 自动分析所有

afl : 查看所有函数



查看init, fini的函数

```

[0x00000e10]> [0x00000e10]> afl | grep "entry"
ERROR: Invalid command '[0x00000e10]> afl' (0x5b)
[0x00000e10]> 0x00000e10    1     12 entry0
[0x00000e10]> 0x000031b0    3    124 entry.init1
[0x000031b0]> 0x00000e20    2      8 entry.fini0

[0x00000e20]> [0x00000e10]> afl | grep "init"
ERROR: Invalid command '[0x00000e10]> afl' (0x5b)
[0x00000e20]> 0x00003310    1    136 sym.Java_sg_vantagepoint_uncrackable3_MainActivity_init
[0x00003310]> 0x000031b0    3    124 entry.init1
```

