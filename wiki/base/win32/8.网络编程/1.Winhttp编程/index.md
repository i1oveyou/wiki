---
title: win32.API.网络编程.winhttp编程
---

参考链接

```
https://learn.microsoft.com/zh-cn/windows/win32/winhttp/winhttp-start-page
https://learn.microsoft.com/zh-cn/windows/win32/winhttp/error-messages
```



目前是学不动一点

```

https://www.cnblogs.com/super119/archive/2011/04/10/2011350.html
https://bbs.kanxue.com/thread-258291-1.htm
https://www.cnblogs.com/Toya/p/14927913.html
https://uknowsec.cn/posts/notes/ShellCode%E8%BF%9C%E7%A8%8B%E5%8A%A0%E8%BD%BD%E5%99%A8%E6%94%B9%E9%80%A0%E8%AE%A1%E5%88%92.html

winhttp的视频讲义: https://www.bilibili.com/video/BV1nP4y1G7rJ?p=2&vd_source=43e0e1ba96c9433bed474fdc8305c719
视频讲义: https://search.bilibili.com/all?keyword=winhttp&from_source=webtop_search&spm_id_from=333.788&search_source=5&duration=4
```







WinHTTP比WinINet更加安全和健壮，可以这么认为WinHTTP是WinINet的升级版本。

下面是WinHTTP常规接口调用步骤：



WintpOpen

WinHttpConnect

WinHttpOpenRequest

WinHttpAddRequestHeaders

WinHttpSendRequest

WinHttpReceiveResponse

WinHttpQueryHeaders

WinHttpReadData

WinHttpCloseHandle




可查询的文档

```
http://www.yfvb.com/help/winhttp/index.htm
```



**winhttp 支持https 支持http代理 (可带用户密码) 。**





# 使用 WinHTTP API 访问 Web



![用于创建句柄的函数](./img/art-winhttp3.png)





一个wenhttp 例子, 访问目标url,并获取返回信息

```c
#include <windows.h>
#include <winhttp.h>
#include <stdio.h>

#pragma comment(lib, "winhttp.lib")

int main() {
 
    DWORD dwSize = 0;
    DWORD dwDownloaded = 0;
    LPSTR pszOutBuffer;
    BOOL  bResults = FALSE;
    HINTERNET  hSession = NULL,hConnect = NULL,hRequest = NULL;

    // Use WinHttpOpen to obtain a session handle.
    // 初始化一个环境
    hSession = WinHttpOpen(L"WinHTTP Example/1.0",//会话句柄
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS, 0);

    // Specify an HTTP server.
    // 打开特定资源的 HTTP 请求,在调用时不会将请求发送到服务器。
    if (hSession)
        hConnect = WinHttpConnect(hSession, L"www.microsoft.com",//连接句柄
            INTERNET_DEFAULT_HTTPS_PORT, 0);

    // Create an HTTP request handle.
    if (hConnect)
        hRequest = WinHttpOpenRequest(hConnect, L"GET", NULL,//请求句柄
            NULL, WINHTTP_NO_REFERER,
            WINHTTP_DEFAULT_ACCEPT_TYPES,
            WINHTTP_FLAG_SECURE);

    // Send a request.
    if (hRequest)
        bResults = WinHttpSendRequest(hRequest,
            WINHTTP_NO_ADDITIONAL_HEADERS, 0,
            WINHTTP_NO_REQUEST_DATA, 0,
            0, 0);


    // End the request.
    if (bResults)
        bResults = WinHttpReceiveResponse(hRequest, NULL);

    // Keep checking for data until there is nothing left.
    if (bResults)
    {
        do
        {
            // Check for available data.
            //应用程序可以使用 HINTERNET 句柄上的 WinHttpReadData 和 WinHttpQueryDataAvailable 函数下载服务器的资源。
            dwSize = 0;
            if (!WinHttpQueryDataAvailable(hRequest, &dwSize))
                printf("Error %u in WinHttpQueryDataAvailable.\n",
                    GetLastError());

            // Allocate space for the buffer.
            pszOutBuffer = malloc(dwSize + 1);
            if (!pszOutBuffer)
            {
                printf("Out of memory\n");
                dwSize = 0;
            }
            else
            {
                // Read the data.
                ZeroMemory(pszOutBuffer, dwSize + 1);

                if (!WinHttpReadData(hRequest, (LPVOID)pszOutBuffer,
                    dwSize, &dwDownloaded))
                    printf("Error %u in WinHttpReadData.\n", GetLastError());
                else
                    printf("%s", pszOutBuffer);

                // Free the memory allocated to the buffer.
                free(pszOutBuffer);
            }
        } while (dwSize > 0);
    }


    // Report any errors.
    if (!bResults)
        printf("Error %d has occurred.\n", GetLastError());

    // Close any open handles.
    if (hRequest) WinHttpCloseHandle(hRequest);
    if (hConnect) WinHttpCloseHandle(hConnect);
    if (hSession) WinHttpCloseHandle(hSession);
}

```

