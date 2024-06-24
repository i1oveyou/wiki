---
title: wiki-base-Assembly-编译器语法
---
# masm32的语法



在masm32中.16进制必须用`h`结尾表示,,,不能是0x,,,并且不能是字母开头

比如

```
32h
0Ch
```

另外,还有一个很奇怪的问题

就是我直接使用fs寄存器的话,,会报错

比如`mov eax,fs:[30h]`

只能这样

```
assume fs:nothing
mov ebx, fs:[edx + 30h]
```



# vs的内敛汇编



数字形式

```
0x100 
100h
```



关于一些地址的书写方式

```
jne $+5 ;
jmp farlabel ;
.
.
.
farlabel:
```



一些立即数

```
_emit  0x4A
```





数组操作

```
int array[10];

__asm mov array[6], bx ;  Store BX at array+6 (not scaled)
array[6] = 0;         /* Store 0 at array+24 (scaled) */

__asm mov array[6 * TYPE int], 0 ; Store 0 at array + 24
array[6] = 0;                   /* Store 0 at array + 24 */
```



## MASM x64 汇编语法

MASM x64 汇编语法只是单独提出来了,但是他和MASM x86大多数是一样的

Microsoft Macro Assembler 的汇编语法

关于如何配置x64调用汇编,不在解释

x64貌似不能内联汇编,只能把汇编代码块封转为一个函数,然乎去调用

最基本的函数

```nasm
.code

_sum PROC
    mov rax, rcx ; 参数1 函数调用约定
    add rax, rdx ; 参数2 函数调用约定
    ret
_sum ENDP

END
```

调用它

```nasm
#define  _CRT_SECURE_NO_WARNINGS
#include <Windows.h>
#include <stdio.h>
#include "head.h"
int main()
{   
	printf("%d", _sum(1,2));
	return 0;
}
```



## 汇编文件引用C语言变量

```nasm
.data
extern gvar:QWORD

.code
_sum PROC
    jmp qword ptr [gvar];
_sum ENDP

END
```



大概就是这个样子

另外一个C语言文件的全局变量大概张这个样子

```nasm
#define  _CRT_SECURE_NO_WARNINGS
#include <Windows.h>
#include <stdio.h>
#include "head.h"

void msg1();
void msg2();
DWORD64 gvar;
BYTE* getReallCall(BYTE* lp)
{
	return  *(DWORD*)(lp + 1) + (BYTE*)lp + 5;
}
void msg1()
{
	MessageBoxA(0, "org", "(:", 0);
	return;
}
void msg2()
{
	MessageBoxA(0, "hook", "(:", 0);
	msg1();
	return;
}
int main()
{
	gvar = getReallCall(msg2);
	_sum();
	return 0;
}
```



# GCC





```
asm(".intel_syntax noprefix");
```





```
gcc -masm=intel ./exmaple
```



```
"__asm__" 表示后面的代码为内嵌汇编，“asm”是“__asm__”的别名。
“__volatile__” 表示编译器不要优化代码，后面的指令保留原样，“volatile”是它的别名。 括号里面是汇编指令。

```

