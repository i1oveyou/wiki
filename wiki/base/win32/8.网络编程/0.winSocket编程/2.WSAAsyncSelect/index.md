---
title: win32.API.网络编程.WSAAsyncSelect
---





原理是基于窗口的消息机制

然后网络消息是某种自定义的消息

```c
int WSAAsyncSelect(
    SOCKET s,      //需要事件通知的套接字
    HWND   hWnd,   //当网络事件发生时接收消息的窗口句柄
    u_int  wMsg,   //当网络事件发生时窗口收到的消息
    long   lEvent  //应用程序感兴趣的网络事件集合
)
```



对于参数四可选的值有：（来自MSDN）

```
Value                          Meaning 
FD_READ                        想要接收可读的通知
FD_WRITE                       想要接收可写的通知
FD_OOB                         想要接收带外数据到来的通知
FD_ACCEPT                      想要接收有到来连接的通知
FD_CONNECT                     想要接收一次连接完成或多点jion操作完成的通知
FD_CLOSE                       想要接收套接字关闭的通知
FD_QOS                         想要接收套接字服务质量发生变化的通知
FD_GROUP_QOS                   想要接收套接字组服务质量发生变化的通知
FD_ROUTING_INTERFACE_CHANGE    想要在指定方向上，与路由接口发生变化的通知
FD_ADDRESS_LIST_CHANGE         想要接收针对套接字的协议家族，本地地址列表发生变化的通知 
```

根据需要选择需要的事件，当需要关注多个事件时，对多个事件按位或（OR）操作，

```
WSAAsyncSelect(s,hwnd,WM_SOCKET,FD_CONNECT | FD_READ | FD_CLOSE);
```

