

# 异常处理

在没有配置的情况下&&在调试的情况下

如果程序遇到异常,,,就会一直卡住,不会交付给用户写的异常处理程序

如果出现异常,并且把异常交付给用户的处理程序,需要做一些过程的配置

 

![image-20230728171404213](./img/image-20230728171404213.png)

然后逐个浏览

于是取消勾选对应的异常

vs的调试器在遇到异常的时候,就把异常交付给用户自定义的处理程序
而不是报错

# 搭配x64的内联汇编环境

有时候,TMD就是配置失败

有时候又成功

## way1

比如写了写了下面的汇编

```nasm
.CODE
 
Int_3 PROC
		MOV EAX, 1234  ;返回1234
		RET
Int_3 ENDP
 
 
MY_TEST PROC
		MOV EAX, 23 ;返回23
		RET
MY_TEST ENDP
 
END
```

写入头文件

```c
#pragma once

#ifndef __ASMCODE_H
#define __ASMCODE_H

int _stdcall Int_3();
int _stdcall MY_TEST();

#endif
```

main函数文件(是main.c)

```c
#define  _CRT_SECURE_NO_WARNINGS
#include <Windows.h>
#include <stdio.h>
#include "head.h"
int main()
{   
	int x = Int_3();
	int y= MY_TEST();
	printf("%d", x + y);
	return 0;
}
```

然后做一些配置

右键asm文件

![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled1.png)

然后

![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled2.png)

然后

![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled3.png)

```c
ml64 /c %(fileName).asm
%(fileName).obj;%(Outpus)
```

然后就愉快的生成文件

```c
已启动重新生成...
1>------ 已启动全部重新生成: 项目: C1, 配置: Debug x64 ------
1>Microsoft (R) Macro Assembler (x64) Version 14.36.32535.0
1>Copyright (C) Microsoft Corporation.  All rights reserved.
1>
1> Assembling: asm1.asm
1>C1.c
1>C1.vcxproj -> E:\Code\normal\C\VisualStdio\Often\x64\Debug\C1.exe
========== “全部重新生成”: 1 成功，0 失败，0已跳过 ==========
========= 重新生成 开始于 12:42 PM，并花费了 01.394 秒 ==========

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++                 Please consider donating to VSColorOutput                    +++
+++                       https://mike-ward.net/donate/                          +++
+++            (this message can be turned off in the settings panel)            +++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```



## way2

https://zhuanlan.zhihu.com/p/270397861

![image-20230721163350068](./img/image-20230721163350068.png)

然后选择并确定

![image-20230721163414169](./img/image-20230721163414169.png)

右键asm文件属性

![image-20230721163446906](./img/image-20230721163446906.png)

选择

![image-20230721163512503](./img/image-20230721163512503.png)



然后就差不多了



asm文件

```assembly
.CODE
 
Int_3 PROC
		MOV EAX, 1234  ;返回1234
		RET
Int_3 ENDP
 
 
MY_TEST PROC
		MOV EAX, 23 ;返回23
		RET
MY_TEST ENDP
 
END
```



c文件

```c
#define  _CRT_SECURE_NO_WARNINGS
#include <Windows.h>
#include <stdio.h>
//#include "head.h" 不用加

extern "C"   int _stdcall Int_3();
extern "C"   int _stdcall MY_TEST();
int main()
{
	int x = Int_3();
	int y = MY_TEST();
	printf("%d", x + y);
	return 0;
}
```







## way3

https://www.cnblogs.com/jszyx/p/12808085.html

https://www.cnblogs.com/VxerLee/p/15185403.html

# 编译设置



## 一些基于源代码的编译指令



### 设置节区的属性

```
#pragma comment(linker, "/SECTION:.text,ERW")
```



### 自定义一个节



```
#pragma data_seg("mydata")
HHOOK g_hHook = NULL;
#pragma data_seg()
#pragma comment(linker, "/SECTION:mydata,RWS")
```





### 设置入口点



```
#pragma comment(linker,"/entry:MyMain")
```



其实通过上面这2个例子,,,

我们就知道,,这些东西都是linker的特性....

所以以后我们在想到某一个功能的时候

应该搜

```
链接器选项,设置节区属性为rwx之类的
```







## 关闭 CheckForDebuggerJustMyCode 

![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled4.png)



![image-20230926215703196](./img/image-20230926215703196.png)



## 关闭 RTC_CheckEsp 



![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled6.png)



## 关闭 数据段不可执行



![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled7.png)

“ **pch”预编译头文件来自编译器的其他版本，或者预编译头为 C++ 而在 C 中使用它(或相反) and vs找不到路径**

![Untitled](./img/27d33af6ca5244a095cb96384bc21234Untitled8.png)





## 如何让程序变得更小？ 像汇编那样

比如，导入表就只有一个导入函数

```c
#include<windows.h>
int my_main()
{
	MessageBoxA(0, "small", "(:", 0);
	return 0;
}
```

通过一些配置后，我们可以让程序只有2-3个函数

而且导入表只有2个API

![image-20230730143359558](./img/image-20230730143359558.png)

然后

![image-20230730143502395](./img/image-20230730143502395.png)

于是就可以正常编译了（我并不知道原理）

如果程序加入一些stdio.h标准库的调用，就会g

但是MessageBox不会



同时还要关闭GS检查

关闭支持仅我的代码调试







## 关闭 __security_checks_cookie 



![image-20231213221422471](./img/image-20231213221422471.png)



## 关于 (/MT),(/MTd),(/MD),(/MDd）

配置属性->C/C++->代码生成->运行库->MT或者MTD

其实就是一个分为2模式

和多线程啥的没关系

分为dbg和release

在每个分支之后,有分为静态和动态的

动态的就是API加载呗

静态的就是把多数代码写入到exe中

# 如何脱离VS运行环境

这个就是基于vs运行库下静态编译和动态编译的一些东西了

也就输说如果你用的是静态编译,那么就可以脱离vs的运行环境

但是对于这些kernel32,user32我暂时还不知道如脱离

如何脱离?

那就多线程MD/MTD啦

配置属性->C/C++->代码生成->运行库->MT或者MTD

如果说连启动函数都不要的话,,那就直接修改入口点





# 忽略特定的警告

假如某个警告是C4133

于是就下面这么操作,就可以忽略这个警告



![image-20231001002040835](./img/image-20231001002040835.png)



或者在代码中实现?

```
#pragma warning(disable:4996)
```



# ml.exe / ml64exe

用于汇编语言的编译链接的

使用VS自带的ml.exe和link.exe进行编译和链接



```assembly
.386
.model flat

extern _MessageBoxA@16:near
extern _ExitProcess@4:near

.data
msg_title db "Demo!", 0
msg_content db "Hello World!", 0

.code
main proc
    push 0
    push 0
    push offset msg_title
    push offset msg_content
    push 0
    call _MessageBoxA@16
    push 0
    call _ExitProcess@4
main endp
end
```



使用VS自带的ml.exe和link.exe进行编译和链接，首先要使用 vcvars32.bat 初始化环境变量

编译：

```
ml.exe /c demo.asm
```

链接：

```
link.exe demo.obj /subsystem:console /defaultlib:kernel32.lib /defaultlib:user32.lib /entry:main /out:demo32_masm.exe
```



# cl.exe



用于c语言的编译链接的

```c
#include <Windows.h>

int main()
{
    const char msg_title[] = "Demo!";
    const char msg_content[] = "Hello World!";

    MessageBoxA(0, msg_title, msg_content, MB_OK);
    ExitProcess(0);
}
```

下面我们通过命令行的方式来生成exe，进行之前需要先运行`vcvars32.bat`，

如果你想要生成64位的exe文件，那么就要先运行`vcvars64.bat`



```
cl /c demo.cpp                                         

link demo.obj /defaultlib:user32.lib /out:demo_cpp.exe
```

如果在编译的时候加上一个`/FA`选项，那么编译器会在当前目录生成一个同名的asm文件（MASM语法），

然后你可以再使用该asm文件编译出obj文件

这样我们就拥有了修改汇编代码的机会，而不是从0开始全部用汇编语言编写代码



使用C编译器生成汇编代码：`cl /c /FA /GS- <file_name>.cpp`

将汇编代码进行编译：`cl /c file.asm`











一般我们都是调试虚拟机,除非你有真机,,,,



 





 



# vs2019 Linux 远程开发

这个不同于vscode

vscode只是远程连接,然后编辑文件和调试文件方便点

但是,,,,还是基于cmake和gdb,,,,调试和编写无法像vs2019 windwos开发那样,,



我本以为vs2019的远程开发也会像vscode那样

但是,,,,他并没有把编译过程交给用户,,,而是自己编译完,,

然后把东西给用户



比如

![image-20231225010513369](./img/image-20231225010513369.png)



ps:

项目创建和windows是一样的

但是head和src文件是我自己单独创建的

但是并不影响真个编译过程



关于c文件,,不能正确引用头文件

https://blog.csdn.net/qq_62147567/article/details/131393829

也就是把头文件文件夹放到Windows中,,然后让Windows引用

```
zip -r usr_include.zip /usr/include
zip -r usr_local_include.zip /usr/local/include
```



![image-20231225011743252](./img/image-20231225011743252.png)

