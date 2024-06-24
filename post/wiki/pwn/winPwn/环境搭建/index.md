---
title: wiki-pwn-winPwn-环境搭建
---
# winPwn



# 环境搭建

既然是Windows的pwn,,,那我的环境就全放在Windows吧….

可能以后换电脑或者系统重装,,就完蛋了

python包下载

```nasm
pip install winpwn
pip install pefile
pip install keystone-engine
pip install capstone
pip install ROPgadget
```

然后安装winchecksec

ROPgadget: 在二进制文件中,搜指定汇编代码(字节码)的位置



# 工具的简单使用



```
┌──(kali㉿kali)-[~/Desktop]
└─$ ROPgadget --binary ./d1.exe --only "pop|ret"
Gadgets information
============================================================
0x00411464 : pop ebp ; ret
0x00412e38 : pop ebp ; ret 0x10
0x00411502 : pop ebp ; ret 4
0x004116fd : pop ebx ; pop ebp ; ret 4
0x004116fb : pop edi ; pop esi ; pop ebx ; pop ebp ; ret 4
0x004116fc : pop esi ; pop ebx ; pop ebp ; ret 4
0x00413693 : pop esi ; ret
0x00411465 : ret
0x00412e39 : ret 0x10
0x004110a6 : ret 0x2f
0x00411748 : ret 0x558b
0x004124b0 : ret 0x5d48
0x004124a7 : ret 0x88a
0x00412bff : ret 0x8901
0x00411e6f : ret 0x8b0e
0x00411503 : ret 4

Unique gadgets found: 16
```



