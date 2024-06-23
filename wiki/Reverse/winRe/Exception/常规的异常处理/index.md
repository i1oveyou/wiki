# 常规的异常处理

# links

```c
[https://blog.csdn.net/hustd10/article/details/51167902](https://blog.csdn.net/hustd10/article/details/51167902)
https://www.securitysift.com/windows-exploit-development-part-6-seh-exploits/

没认真看:
https://cloud.tencent.com/developer/article/1471316
```

# 常见的的异常编写

**`__try__except`**

```c
int exception_filter(unsigned long exceptionCode, struct _EXCEPTION_POINTERS *exceptionInfo) {
    // 在这里进行异常过滤和处理逻辑
    // 返回相应的值来指示如何处理异常
    if (exceptionCode == EXCEPTION_ACCESS_VIOLATION) {
        // 处理访问冲突异常
        return EXCEPTION_EXECUTE_HANDLER;
    }
    else {
        // 其他异常，继续搜索其他的异常处理程序
        return EXCEPTION_CONTINUE_SEARCH;
    }
}

__try {
    // 受保护的代码区域
    // ...
}
__except (exception_filter(GetExceptionCode(), GetExceptionInformation())) {
    // 异常处理代码
    // ...
}

/*
__try{}、
__finally{}、
__except{}、
__leave
无论 __try 块中的指令以何种方式退出，都必然会执行 __finally 块
*/
```

**`try-catch`**

```cpp
#include <iostream>
#include <stdexcept>

class MyException : public std::exception {
public:
    const char* what() const noexcept override {
        return "My custom exception occurred!";
    }
};

int main() {
    int numerator, denominator;

    std::cout << "Enter the numerator: ";
    std::cin >> numerator;

    std::cout << "Enter the denominator: ";
    std::cin >> denominator;

    try {
        if (denominator == 0) {
           // 代码块，可能引发自定义异常
		        throw MyException();
        }
        double result = static_cast<double>(numerator) / denominator;
        std::cout << "Result: " << result << std::endl;
    }catch (const MyException& e) {
        // 捕获并处理自定义异常
        std::cerr << "Caught exception: " << e.what() << std::endl;
    }
    catch (...) {
        // 默认处理其他类型的异常
        std::cout << "Unknown exception caught." << std::endl;
    } 
    return 0;
}
```

**try_catch**和**__try__except区别**

C/C++中的 **`try-catch`**和**`__try-__except`**是用于异常处理的两种不同的机制。

它们有一些关键的区别

**`__try__except`** 是 Microsoft/Windows/VC 特定的语法,不能用在Linux上

![Untitled](./img/Untitled.png)

**`try-catch`** 是 C++ 标准中引入的异常处理机制，只要是C++就都可以使用

**`try-catch`** 适用于 C++ 中的异常处理，可以捕获各种类型的异常，包括用户自定义异常。

**`__try__except`** 更为底层，可以用于处理 SEH 中定义的异常，通常用于处理系统级别的异常，

如访问冲突、硬件异常等。不太适合用于 C++ 中的高级异常处理。

# 运行机制

**当某函数触发异常时，系统首先会通过调用 KiDispatchException 来给内核调试器**

**一个机会，如果内核调试器没有处理该异常，则该机会被转给 RtlDispatchException，**

**这个函数就开始分发该异常。分发过程为：**

**从当前线程的异常链表头开始遍历，**

**对于每一个 SEH 注册信息（即 EXCEPTION_REGISTRATION(_RECORD)），**

**调用其 Handler。根据 Handler 的返回值做相应的后续处理：**

**1. 返回 ExceptionContinueExecution，表示 Handler 已经修复了异常触发点，从异常触发点继续执行。**

**2. 返回 ExceptionContinueSearch，表示该 Handler 没有处理该异常，继续遍历异常链表。**

**3. Handler 没有修复异常触发点，但是却能处理该异常（某个 __except 过滤代码返回 EXCEPTION_EXECUTE_HANDLER）。这种情况下，**

**处理完该异常后就从异常解决代码（__except 代码块）继续执行，Handler 不会返回。**

**以上是简略的 x86 SEH 流程，其中省略了很多细节，**

**比如展开、错误处理、ExceptionNestedException 和 ExceptionCollidedUnwind 等等**

x64 中 SEH 的流程总体思路也是如此，只是细节上做了一些修改。

但这并不表示熟悉 x86 SEH 就能很轻松的掌握 x64 SEH。

# SEH介绍

## 简单介绍

SEH（ Structured Exception Handling ， 结构化异常处理 ）

小名: SEH 和线程相关 

异常处理的回调存在于堆栈中

当一个异常发生的时候，操作系统从SEH链头部开始，检查第一个

_EXCEPTION_REGISTRATION_RECORD（即异常处理器）的异常处理函数，

看它能否处理该异常（通过ExceptionRecord 和ContextRecord参数）。

如果不能，则移动到下一个_EXCEPTION_REGISTRATION_RECORD，

继续检查，直到找到合适的异常处理器。

Windows在SEH链的末尾放置了一个默认的通用异常处理器，保证异常肯定能被处理。

如果使用默认的异常处理器处理，你通常会看到“程序遇到了一个问题，需要关闭…”之类的信息。

![Untitled](./img/Untitled%201.png)

```c
struct _EXCEPTION_REGISTRATION_RECORD
{
    struct _EXCEPTION_REGISTRATION_RECORD *Next; //下一个节点
    PEXCEPTION_ROUTINE Handler;				//异常处理函数的地址
} EXCEPTION_REGISTRATION_RECORD;
//Next 为指向下一个链表的指针,直到遇到 0xFFFFFFFF 结束
```

![Untitled](./img/Untitled%202.png)

## 处理函数

SEH默认使用的是

```c
//异常处理函数类型
EXCEPTION_DISPOSITION
NTAPI
EXCEPTION_ROUTINE (
    _Inout_ struct _EXCEPTION_RECORD *ExceptionRecord,
    _In_ PVOID EstablisherFrame,
    _Inout_ struct _CONTEXT *ContextRecord, //上下文结构体
    _In_ PVOID DispatcherContext
    );

typedef EXCEPTION_ROUTINE *PEXCEPTION_ROUTINE;

//返回值类型 包括异常码，异常发生的地址，参数的个数
// Exception disposition return values
typedef enum _EXCEPTION_DISPOSITION
{
    ExceptionContinueExecution,//0 表示 Handler 已经修复了异常触发点，从异常触发点继续执行
		ExceptionContinueSearch,//1 表示该 Handler 没有处理该异常，继续遍历异常链表。
    ExceptionNestedException,//2
    ExceptionCollidedUnwind//3
} EXCEPTION_DISPOSITION;

//异常记录结构体
typedef struct _EXCEPTION_RECORD {
    DWORD    ExceptionCode;
    DWORD ExceptionFlags;
    struct _EXCEPTION_RECORD *ExceptionRecord;
    PVOID ExceptionAddress;
    DWORD NumberParameters;
    ULONG_PTR ExceptionInformation[EXCEPTION_MAXIMUM_PARAMETERS];
    } EXCEPTION_RECORD;

typedef EXCEPTION_RECORD *PEXCEPTION_RECORD;
```

SEH处理函数返回的数值 和try_except返回的数值是不一样的

SEH返回如下

```cpp
// Exception disposition return values
typedef enum _EXCEPTION_DISPOSITION
{
    ExceptionContinueExecution,//0 表示 Handler 已经修复了异常触发点，从异常触发点继续执行
		ExceptionContinueSearch,//1 表示该 Handler 没有处理该异常，继续遍历异常链表。
    ExceptionNestedException,//2
    ExceptionCollidedUnwind//3
} EXCEPTION_DISPOSITION;

```

 

try_except返回如下

```cpp
// Defined values for the exception filter expression
// 注意和_EXCEPTION_DISPOSITION不同的
#define EXCEPTION_EXECUTE_HANDLER      1  //执行**Handler且不会返回**
#define EXCEPTION_CONTINUE_SEARCH      0  //丢个下一个
#define EXCEPTION_CONTINUE_EXECUTION (-1) 
```

# _except_handler3

# _except_handler4_common

## except_handler4

其实我们的try catch 就是通过except_handler4注册的

而汇编手动注册的东西 是基于FS(x86),GS(x64)的SEH链注册的,而且采用的是头插法

那么手动汇编注册的异常处理会先于except_handler4

如果你的代码中长得像这样

```nasm
push    ebp
mov     ebp, esp
push    0FFFFFFFEh
push    offset stru_419230;这里是特征
push    offset __except_handler4;这里是特征
mov     eax, large fs:0 ;这里是特征
push    eax
add     esp, 0FFFFFF38h
push    ebx
push    esi
push    edi
lea     edi, [ebp+ms_exc]
xor     ecx, ecx
mov     eax, 0CCCCCCCCh
rep stosd
mov     eax, ___security_cookie
xor     [ebp+ms_exc.registration.ScopeTable], eax;这里是特征
xor     eax, ebp
push    eax             ; char
lea     eax, [ebp+ms_exc.registration];这里是特征

mov     large fs:0, eax;这里是特征

```

说明,差不多就用了try except了

SEH 函数返回值

```c
__except 后的括号中会存在一个异常过滤表达式表达式的返回值必定是一下说明的几个之一
EXCEPTION_EXECUTE_HANDLER(1): 	//自己处理,EIP不会返回,直接去父级的__except{}
EXCEPTION_CONTINUE_SEARCH(0): 	//把异常丢给下一位嘉宾
EXCEPTION_CONTINUE_EXECUTION(-1): //自己处理,EIP会根据CONTEXT做一个返回 ,EIP原理是异常发生的地方

```

### try, except

在 VS 的同一个函数中无论编写了多少个 SEH， 编译器实际上只会安装一个叫做 except_handler4 的函数

然后的话,一个try只能匹配一个except(我这里不是指的嵌套)

```c
#include <windows.h>
#include <stdio.h>
// 带有异常处理函数的函数
void test1()
{
    int x = 10;
    __try
    {
        printf("__try - { ... }\\n");
        __try
        {
            printf("__try -- { ... }\\n");
            x = x / 0;
        }
        __except (0)
        {
            printf("__except (1) --{ ... }\\n");
        }
    }
    __except (1)//如果返回-1.会陷入exit的结果,返回1就是不再去往异常处
    {
        printf("__except (1) - { ... }\\n");
    }
}

// 没有异常处理函数的函数
void test2()
{

}

// 遍历当前程序中已经存在的异常处理函数
void ShowSEH()
{
    // 定义一个结构体指针，用于保存 SEH 链表的头节点
    PEXCEPTION_REGISTRATION_RECORD header = 0;

    // 通过 FS:[0] 找到 ExceptionList 的头节点
    __asm push fs : [0]
    __asm pop header

        // 遍历异常处理链表，链表以 -1 结尾
        while (header != (EXCEPTION_REGISTRATION_RECORD*)-1)
    {
        printf("function: %08X\\n", header->Handler);
        header = header->Next;
    }
    printf("\\n");
}

int main()
{
    test1();
    test2();
    ShowSEH();
    ShowSEH();
    return 0;
}

```

一单try后面出现异常,他不是往回运行,而是去except处理函数

### finally , leave

另外就是这个finally块为什么except块不是共存的呀

无论 __try 以何种方式退出，都会执行finally这里

```c
#include <windows.h>
#include <stdio.h>

int main(void)
{
    __try
    {
        printf("异常代码可能发生部分\\n");
        __leave; // 使用 __leave 跳出当前的 __try ,这是正常退出的方式之一
        //goto flag; //异常退出方式
    }
    __finally
    {

        // 无论 __try 以何种方式退出，都会执行这里的指令
        printf("退出\\n");
        if (AbnormalTermination())
            printf("异常退出\\n");
        else
            printf("正常退出\\n");
    }
    flag:
    return 0;
}

```

## Handler 手动注册

是的注册的东西,它是位于SEH大链的

关于汇编手动注册的返回值,

```c
// Exception disposition return values
enum _EXCEPTION_DISPOSITION
{
    ExceptionContinueExecution,         // 0 继续执行异常代码 (可以视为已经处理)
    ExceptionContinueSearch,            // 1 丢给下一个异常处理器
    ExceptionNestedException,           //在OS内部使用
    ExceptionCollidedUnwind             //在OS内部使用
} EXCEPTION_DISPOSITION;

```

返回EXCEPTION_EXECUTE_HANDLER时则表示异常被处理，

会先把内部的__finally块执行完，

再跳到自身的__except块中执行。

反正不会在以前绊脚摔跟头的地方那里继续执行

返回EXCEPTION_CONTINUE_EXECUTION时表示该异常被忽略，继续在异常发生的地方开始执行

ps: 说的好像有点问题,以后实践在解决吧

下面的处理函数

```c
// SEH handler
EXCEPTION_DISPOSITION __cdecl _except_handler(
    _In_ struct _EXCEPTION_RECORD* _ExceptionRecord,
    _In_ void*                     _EstablisherFrame,
    _Inout_ struct _CONTEXT*       _ContextRecord,
    _Inout_ void*                  _DispatcherContext
);

```

注册

手动直接注册

```nasm
push @_except_handler    ;异常处理器
push dword ptr fs:[0]     ;取出 SEH链表头
mov dword ptr fs:[0],esp  ;添加链表

```

卸载

```nasm
pop dword ptr fs:[0]    ;还原链表头
add esp,4    ;删除 异常处理器

```

参数1(lp)

一个指向EXCEPTION_RECORD结构的指针

```c
typedef struct _EXCEPTION_RECORD {
    DWORD ExceptionCode; //异常的类型
    DWORD ExceptionFlags;
    struct _EXCEPTION_RECORD *ExceptionRecord; //这个类型和自己是一样的 ?
    PVOID ExceptionAddress; //异常发生的地址 !!!!!!
    DWORD NumberParameters;//含有的元素个数
    DWORD ExceptionInformation[EXCEPTION_MAXIMUM_PARAMETERS];
} EXCEPTION_RECORD;

```

参数2(lp)

是一个指向establisher帧结构的指针。它是SEH中一个至关重要的参数，但是现在你可以忽略它。

参数3(lp)

一个指向CONTEXT结 构的指针

这个CONTEXT结构就是GetThreadContext和SetThreadContext这两个API中使用 的那个CONTEXT结构

```c
typedef struct _CONTEXT
{
    DWORD ContextFlags;
    DWORD Dr0;
    DWORD Dr1;
    DWORD Dr2;
    DWORD Dr3;
    DWORD Dr6;
    DWORD Dr7;
    FLOATING_SAVE_AREA FloatSave;
    DWORD SegGs;
    DWORD SegFs;
    DWORD SegEs;
    DWORD SegDs;
    DWORD Edi;
    DWORD Esi;
    DWORD Ebx;
    DWORD Edx;
    DWORD Ecx;
    DWORD Eax;
    DWORD Ebp;
    DWORD Eip;
    DWORD SegCs;
    DWORD EFlags;
    DWORD Esp;
    DWORD SegSs;
} CONTEXT;

```

参数4

被称为DispatcherContext。它暂时也可以被忽略。

```c
#include <stdio.h>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>

DWORD scratch;
EXCEPTION_DISPOSITION _cdecl _except_handler(struct _EXCEPTION_RECORD* ExceptionRecord,
    void* EstablisherFrame,
    struct _CONTEXT* ContextRecord,
    void* DispatcherContext)
{
    unsigned i;
    // 指明是我们让流程转到我们的异常处理程序的
    printf("Hello from an exception handler\\n");
    // 改变CONTEXT结构中EAX的值，以便它指向可以成功进写操作的位置
    ContextRecord->Eax = (DWORD)&scratch;
    // 告诉操作系统重新执行出错的指令
    return ExceptionContinueExecution; //ExceptionContinueSearch;// ExceptionContinueExecution; //基于异常表达式的返回值, 基于SEH函数的返回值?
}

int main()
{
    DWORD handler = (DWORD)_except_handler;
    __asm
    {
        // 创建EXCEPTION_REGISTRATION结构：
        push handler; // handler函数的地址
        push FS : [0] ; // 前一个handler函数的地址
        mov FS : [0] , ESP; // 安装新的EXECEPTION_REGISTRATION结构
    }
    __asm
    {
        mov eax, 0;     // 将EAX清零
        mov[eax], 1; // 写EAX指向的内存从而故意引发一个错误
    }
    printf("After writing!\\n");
    __asm
    {
        // 移去我们的EXECEPTION_REGISTRATION结构
        mov eax, [ESP];    // 获取前一个结构
        mov FS : [0] , EAX; // 安装前一个结构
        add esp, 8;      // 将我们的EXECEPTION_REGISTRATION弹出堆栈
    }
    return 0;
}

```

# 回调问题?

我暂时没看懂

但是发现

如果返回异常处理是下面这句话,就不会再次回调那个异常处理函数,并且不会进入except

```c
ContextRecord->Eip+=0xA;//指向下一个汇编语句,0xA是我看汇编找到的
    return ExceptionContinueExecution;
}

```

```c
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
EXCEPTION_DISPOSITION
__cdecl _except_handler(
    struct _EXCEPTION_RECORD* ExceptionRecord,
    void* EstablisherFrame,
    struct _CONTEXT* ContextRecord,
    void* DispatcherContext)
{
    printf("Home Grown handler: Exception Code: %08X Exception Flags %X",
           ExceptionRecord->ExceptionCode, ExceptionRecord->ExceptionFlags);

    if (ExceptionRecord->ExceptionFlags & 1)
        printf(" EH_NONCONTINUABLE");
    if (ExceptionRecord->ExceptionFlags & 2)
        printf(" EH_UNWINDING");
    if (ExceptionRecord->ExceptionFlags & 4)
        printf(" EH_EXIT_UNWIND");
    if (ExceptionRecord->ExceptionFlags & 8) 		// 注意这个标志
        printf(" EH_STACK_INVALID");
    if (ExceptionRecord->ExceptionFlags & 0x10)   	// 注意这个标志
        printf(" EH_NESTED_CALL");
    printf("\\n");

    // 我们不想处理这个异常，让其它函数处理吧
    return ExceptionContinueSearch;
}

void HomeGrownFrame(void)
{
    DWORD handler = (DWORD)_except_handler;
    __asm
    {
        // 创建EXCEPTION_REGISTRATION结构：
        push handler       // handler函数的地址
            push FS : [0]        // 前一个handler函数的地址
        mov FS : [0] , ESP     // 安装新的EXECEPTION_REGISTRATION结构
        }

    *(PDWORD)0 = 0; // 写入地址0，从而引发一个错误
    printf("I should never get here!\\n");

    __asm
    {
        // 移去我们的EXECEPTION_REGISTRATION结构
        mov eax, [ESP]     // 获取前一个结构
            mov FS : [0] , EAX // 安装前一个结构
            add esp, 8        // 把我们EXECEPTION_REGISTRATION结构弹出堆栈
        }
}

int main()
{
    __try
    {
        HomeGrownFrame();
    }
    __except (EXCEPTION_EXECUTE_HANDLER)
    {
        printf("Caught the exception in main()\\n");
    }

    return 0;
}

```

# eg

## 1

```c
#include <stdio.h>
//==================================================
// MYSEH - Matt Pietrek 1997
// Microsoft Systems Journal, January 1997
// FILE: MYSEH.CPP
// 用命令行CL MYSEH.CPP编译
//==================================================
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
DWORD scratch;

LONG WINAPI VectoredExceptionHandler(PEXCEPTION_POINTERS ExceptionInfo)
{
    printf("ExceptionCode: %X\\n", ExceptionInfo->ExceptionRecord->ExceptionCode);
    if (ExceptionInfo->ExceptionRecord->ExceptionCode == 0xc0000005)
    {
        ExceptionInfo->ContextRecord->Eax = 1;
        ExceptionInfo->ContextRecord->Ecx = 1;

        return EXCEPTION_CONTINUE_SEARCH;
    }
    return EXCEPTION_EXECUTE_HANDLER;
}
EXCEPTION_DISPOSITION _cdecl _except_handler(struct _EXCEPTION_RECORD* ExceptionRecord,
    void* EstablisherFrame,
    struct _CONTEXT* ContextRecord,
    void* DispatcherContext)
{
    unsigned i;

    printf("%08x\\n", ExceptionRecord->ExceptionCode);
    ContextRecord->Eax = (DWORD)&scratch;
    return ExceptionContinueSearch;
    //ExceptionContinueSearch;
    // ExceptionContinueExecution;
    //基于异常表达式的返回值, 基于SEH函数的返回值?

    /*

    typedef enum _EXCEPTION_DISPOSITION
{
    ExceptionContinueExecution,0 <- 1
    ExceptionContinueSearch,1 <- 0
    ExceptionNestedException,2
    ExceptionCollidedUnwind3

} EXCEPTION_DISPOSITION;*/
}
LONG FirstSEHer(PEXCEPTION_POINTERS pExcepInfo)
{

    printf("%08x\\n", pExcepInfo->ExceptionRecord->ExceptionCode);
    return EXCEPTION_CONTINUE_SEARCH;
}
LONG SecondSEHer(PEXCEPTION_POINTERS pExcepInfo)
{
    printf("%08x\\n", pExcepInfo->ExceptionRecord->ExceptionCode);
    return EXCEPTION_CONTINUE_EXECUTION;

    //return EXCEPTION_EXECUTE_HANDLER;
}
void ExceptTest()
{
    DWORD handler = (DWORD)_except_handler;
    DWORD* lp = 0;
    __asm
    {
        // 创建EXCEPTION_REGISTRATION结构：
        push handler // handler函数的地址
        push FS : [0] // 前一个handler函数的地址
        mov  FS : [0] , ESP // 安装新的EXECEPTION_REGISTRATION结构
    }
    printf("After writing!\\n");
    __try
    {
        __try
        {
            __try
            {
                *lp = 0;
                printf("Find Me?\\n");
            }
            __finally
            {
                printf("[[SEH][0] finally \\n");
            }
        }
        __except (FirstSEHer(GetExceptionInformation()))
        {
            printf("[EH.Exe] [SEH][1] 被俺处理了 SEH1 返回 EXCEPTION_EXECUTE_HANDLER\\n");
        }
    }
    __except (SecondSEHer(GetExceptionInformation()))
    {
        printf("[EH.Exe] [SEH][2] 被俺处理了 SEH2 返回 EXCEPTION_EXECUTE_HANDLER\\n");
    }
    __asm
    {
        // 移去我们的EXECEPTION_REGISTRATION结构
        mov eax, [ESP]    // 获取前一个结构
        mov FS : [0] , EAX // 安装前一个结构
        add esp, 8       // 将我们的EXECEPTION_REGISTRATION弹出堆栈
    }
}

int main()
{

    AddVectoredExceptionHandler(TRUE, VectoredExceptionHandler);
    ExceptTest();
    return 0;
}

```

## 2

```c
#include <stdio.h>
//==================================================
//#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
DWORD scratch;

LONG WINAPI VectoredExceptionHandler(PEXCEPTION_POINTERS ExceptionInfo)
{
    printf("VEH:%08X\\n", ExceptionInfo->ExceptionRecord->ExceptionCode);
    if (ExceptionInfo->ExceptionRecord->ExceptionCode == 0xc0000005)
    {
        return EXCEPTION_CONTINUE_SEARCH;
    }
    return EXCEPTION_EXECUTE_HANDLER;
}
EXCEPTION_DISPOSITION  SEH1(struct _EXCEPTION_RECORD* ExceptionRecord,
    void* EstablisherFrame,
    struct _CONTEXT* ContextRecord,
    void* DispatcherContext)
{
    unsigned i;
    printf("SEH:%08X\\n", ExceptionRecord->ExceptionCode);
    ContextRecord->Eax = (DWORD)&scratch;
    return ExceptionContinueExecution;
}
void ExceptTest()
{
    DWORD* lp = 0;
    __asm
    {
        // 创建EXCEPTION_REGISTRATION结构：
        push SEH1 // handler函数的地址
        push FS : [0] // 前一个handler函数的地址
        mov  FS : [0] , ESP // 安装新的EXECEPTION_REGISTRATION结构
    }
    *lp = 0;
    __asm
    {
        // 移去我们的EXECEPTION_REGISTRATION结构
        mov eax, [ESP]    // 获取前一个结构
        mov FS : [0] , EAX // 安装前一个结构
        add esp, 8       // 将我们的EXECEPTION_REGISTRATION弹出堆栈
    }
}

int main()
{
    AddVectoredExceptionHandler(TRUE, VectoredExceptionHandler);
    ExceptTest();
    return 0;
}

```