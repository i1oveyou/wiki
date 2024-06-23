



使用NASM汇编器进行汇编：

```
nasm -f win32 .\exec_calc.asm
```

生成Obj文件后，使用VS Link 链接器进行链接

```
link.exe /OUT:"exec_calc.exe" /MACHINE:X86 /SUBSYSTEM:WINDOWS /NOLOGO /TLBID:1 /ENTRY:Start .\exec_calc.obj
```

