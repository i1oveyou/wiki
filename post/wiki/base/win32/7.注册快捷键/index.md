---
title: wiki-base-win32-7.注册快捷键
---
---
title: win32.API.热键
---



# 控制台注册快捷键



比如我们注册一个`CTRL+A`

```c
HWND hConsole = GetActiveWindow(); // 获取当前显示窗口的句柄（即控制台这个窗口的句柄）

RegisterHotKey(
    hConsole,   // 注册快捷键的窗口句柄
    1,          // 热键标识符
    MOD_CONTROL | MOD_NOREPEAT, // Ctrl 键  No Repeat 不重复发送
    'A'         // A
);  // Ctrl + A
```



神奇的是,,这个快捷键注册后,,

我无论在哪里按,,,`HWND hConsole = GetActiveWindow(); `

所在的窗口都可以接受到消息的



