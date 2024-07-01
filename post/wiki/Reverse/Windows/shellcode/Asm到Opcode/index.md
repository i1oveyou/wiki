---
title: wiki-Reverse-winRe-shellcode-Asm到Opcode
---
# 从汇编到字节码的方式





为什么会写这篇文章....

因为vs2019的 c/c++ x86中,内嵌汇编的语法有限

比如难受的_emit语法,,,无法使用db,dw,dd指令

对于纯汇编手写的shellcode,,,不是内嵌那种

我还是建议使用纯正的汇编编译器

支持的汇编语法更多



工具有很多.常见的IDE有

```
RadAsm
YASM
```

当然自己写命令行去敲,,,也没问题



常见的assembly编译器

```
微软masm的ml.exe
nasm.exe
yasm.exe
```

连接器,,好像是通用的link.exe



网上的大佬说,,写汇编,语法越简单越好,他们推荐nasm或者yasm

当然,我认为无所谓...自己顺手就行



比如我们用SASM,然后使用masm去编译

![image-20231214152254039](./img/image-20231214152254039.png)

可以发现可以构建成功,,,

然乎字符串的引用也方便了很多



