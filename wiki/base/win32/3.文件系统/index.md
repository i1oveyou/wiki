---
title: win32.API.文件系统
---



# 基础概念



**文件对象**

学过C++的可能比较好理解，学过C的可以把文件对象当成是标准库中操作文件的FILE结构体。



**文件流**

当我们开始操作一个文件的时候，这个文件的打开关闭都由程序控制，而其中的内容是可以动态增减的，

这样的情况类似水流一般，我们把这样的文件状态称作文件流。



**文件句柄**

当我们打开文件的时候，系统分配的一个句柄标识。



**文件指针**

博主看来，这个通常是文件读写操作时，存储相对于文件起始位置的一个指针。





那么实际上，用户的输入、输出这一类的“缓存”也就是这样的状态，通常是叫做输入流和输出流，

除了这两个还有一个错误流。C语言中的标准库(stdio.h)中有定义这三个常用的流，

也即stdin(标准输入流)、stdout(标准输出流)和stderr(标准错误流)。

如果大家仔细深究 stdio.h 的头文件会发现，这些流的定义跟文件的定义实际上是同样的。

好了，回到终点，那么既然这些东西都已经是 “流” 的状态了，那么也就意味着我们不需要去打开什么文件，

来生成什么文件流，直接可以用文件操作的函数来操作这些输入输出流。

比如输入

```
scanf("%d", &i);
实际上就是 fscanf(stdin, "%d", &i); 的简写而已。
```

比如 fgets 

```c
#include <Windows.h>;
#include <stdio.h>;
 
void welcome();
 
int main()
{
    char Command_str[MAX_PATH];
    DWORD Command_len;
    HANDLE hConsoleInput;  
 
    // 获取输出流的句柄
    hConsoleInput = GetStdHandle(STD_INPUT_HANDLE);  
 
    // 输出欢迎信息
    welcome();
 
    while(1)
    {
        // 清空命令字符串
        memset(&Command_str, 0, MAX_PATH);
        // 输出提示符
        printf("nLscmd>;");
        // 读取输入流
        ReadFile(
            hConsoleInput,  // 文件句柄
            Command_str,    // 获取内容的缓冲字符数组
            MAX_PATH,       // 缓冲数组大小
            &Command_len,   // 实际读出的大小
            NULL);
 
        printf("接收到命令：[%s]", Command_str);
    }
}
 
void welcome()
{
    printf("Lellansin's CMD Tool [版本 0.0.1]n");
    printf("学习自制 (c) www.lellansin.com 欢迎交流n");
}
```





# 文件系统操作 常见 API

| CreateFile                 | 创建、打开文件             |
| -------------------------- | -------------------------- |
| ReadFile                   | 读取文件内容               |
| WriteFile                  | 写入文件内容               |
| SetFilePointer             | 移动文件指针               |
| SetEndOfFile               | 设置文件结尾标志           |
| CopyFile                   | 文件拷贝                   |
| DeleteFile                 | 文件删除                   |
| MoveFile                   | 文件移动                   |
| CreateDirectory            | 创建一个目录               |
| RemoveDirectory            | 删除一个目录               |
| GetCurrentDirectory        | 获取当前程序所在目录       |
| SetCurrentDirectory        | 设置当前程序所在目录       |
| FindFirstFile              | 查找指定目录下的第一个文件 |
| FindNextFile               | 查找下一个文件             |
| LockFile                   | 文件锁定                   |
| UnlockFile                 | 文件解锁                   |
| GetFileType                | 获取文件类型               |
| GetFileSize                | 获取文件的大小             |
| GetFileAttributes          | 获取文件属性               |
| SetFileAttributes          | 设置文件属性               |
| GetFileTime                | 获取文件时间               |
| GetFileInformationByHandle | 获取文件信息               |
| GetFullPathName            | 获取文件的完整路径         |
| GetModuleFileName          | 获取当前模块全路径         |

 



文档详见：[MSDN 文件操作 详细文档](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-management-functions?redirectedfrom=MSDN)

# 高级文件操作

| CreateFileMapping | 创建文件的映射对象                                           |
| ----------------- | ------------------------------------------------------------ |
| MapViewOfFile     | 创建视图，将创建的文件映射对象到当前进程的地址空间中         |
| FlushViewOfFile   | 将视图中数据都写入磁盘，对视图的操作都会反映到磁盘上的文件中 |
| OpenFileMapping   | 打开已存在的文件映射                                         |
| UnmapViewOfFile   | 取消文件映射                                                 |
| QueryDosDevice    | 查询 MS-DOS 设备的名称                                       |