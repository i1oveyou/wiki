# shellcode数据引用



# 字符串比较

比如我们想实现一个`strcmp(xxx,"GetProaddress")`

汇编如何实现

```assembly
cmp dword ptr[eax], 0x50746547; //Getp
jnz Get_Function;
cmp dword ptr[eax + 0x4], 0x41636f72; //rocA
jnz Get_Function;
cmp dword ptr[eax + 0x8], 0x65726464; //ddre
jnz Get_Function;
```

可以看到他把`GetProaddress`拆分为一些4字节来比较,思路比较奇特

当然这里也看尽了了一种特殊的方式去引用字符串,也就是拆分字符串



# 字符串引用



## way1 在字节码中插入字符串



这是使用汇编的编译器引用字符串的例子

```assembly
.386
.model flat,stdcall
.stack 4096


.data


.code
main PROC
    call end_of_string
    db 'evil.exe',0
    end_of_string:
    ret
main ENDP
END main
```



这个是x86内嵌汇编例子,比较傻b鸡肋

```assembly
    _asm
    {   call $ + 5;
        pop esi;
        add esi, 8
        jmp tag
        _emit 0x4C;
        _emit 0x6F;
        _emit 0x61;
        _emit 0x64;
        _emit 0x4C;
        _emit 0x69;
        _emit 0x62;
        _emit 0x72;
        _emit 0x61;
        _emit 0x72;
        _emit 0x79;
        _emit 0x41;
        _emit 0x00;
    tag:
    }  
```

这种方式的话,,,还可以起到一定的干扰静态分析的效果



## way2 push入栈



其实和之前的一样,,,,

也是把字符串拆分为4字节一组或者其它什么什么的

然后我们push 入栈

最后我们再获取esp,于是esp就指向了



```assembly
push 0                ; WinExec uCmdShow
push 0x6578652e       ; exe. : 6578652e
push 0x636c6163       ; clac : 636c6163
; 然偶就是引用esp的操作了
```





## way3  依然是在字节码中插入字符串,但...

这是c语言生成汇编那种,,,,

```
char szBuff[]={'1','2','3','4','5'};
```

类似于这种

为什么不用,我就不多说了

```
char szBuff[]="12345";
```







