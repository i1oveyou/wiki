

# 指令



```

gdb ./exmp # 表示我们要调试exmp

start #开始调试

s #f7
n # f8
c #运行到断点
info b #查看断点情况
```

# GDB常用命令



| 命令                      | 简写                | 含义                                        | eg            |
| ------------------------- | ------------------- | ------------------------------------------- | ------------- |
| file <file>               | -                   | 装入待调试的可执行文件                      |               |
| **run**                   | r                   | 执行程序(至结束)                            |               |
| **start**                 |                     | 开始调试(至main开始处暂停)                  |               |
| **step**                  | s                   | 执行一条程序，若为函数则进入内部执行        |               |
| **next**                  | n                   | 执行一条程序，不进入函数内部                |               |
| continue                  | c                   | 连续运行                                    |               |
| finish                    |                     | 运行到当前函数返回                          |               |
| kill                      | k                   | 终止正在调试的程序                          |               |
| **list**                  | l                   | 列出源代码的一部分(10行)                    |               |
| **print** <tmp>           | p <tmp>             | 打印变量的值                                |               |
| **info locals**           | i locals            | 查看当前栈帧的局部变量                      |               |
| **backtrace**             | bt                  | 查看函数调用栈帧编号                        |               |
| **frame** <id>            | f <id>              | 选择栈帧(再看局部变量)                      |               |
| **display** <tmp>         |                     | 每次自动显示跟踪的变量的值                  |               |
| undisplay <tmp>           |                     | 取消跟踪                                    |               |
| **break** <num>           | b                   | 设置(调试)断点                              | b *0x00401678 |
| delete breakpoints <num>  | d breakpoints <num> | 删除断点，不加行号则删除所有                |               |
| disable breakpoints <num> | -                   | 屏蔽断点                                    |               |
| enable breakpoints <num>  | -                   | 启用断点                                    |               |
| **info breakpoints**      | i breakpoints       | 显示所有断点                                |               |
| break 9 if sum != 0       |                     | 根据条件设置断点(sum不等于0时，第9行设断点) |               |
| **set var** sum=0         |                     | 修改变量的值(使sum变量的值为0)              |               |
| watch <tmp>               |                     | 监视一个变量的值                            |               |
| examine <...>             |                     | 查看内存中的地址                            |               |
| jump <num>                | j                   | 跳转执行                                    |               |
| signal <...>              |                     | 产生信号量                                  |               |
| return                    |                     | 强制函数返回                                |               |
| call <fun>                |                     | 强制调用函数                                |               |
| make <...>                |                     | 不退出gdb下重新产生可执行文件               |               |
| shell <...>               |                     | 不退出gdb下执行shell命令                    |               |
| **quit**                  | q                   | 退出gdb环境                                 |               |

# 调试示例1



# 插件



