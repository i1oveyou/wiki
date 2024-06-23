

# shell指令

 





`af`的意思是”analyze function“。

`afl`可以列出分析中发现的函数。





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

