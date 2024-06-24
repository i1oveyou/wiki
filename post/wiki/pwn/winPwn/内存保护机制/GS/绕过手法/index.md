---
title: wiki-pwn-winPwn-内存保护机制-GS-绕过手法
---


# GS绕过

# links

```
https://www.kn0sky.com/?p=159#%E5%88%A9%E7%94%A8%E8%99%9A%E5%87%BD%E6%95%B0%E7%AA%81%E7%A0%B4gs%E4%BF%9D%E6%8A%A4
https://blog.wohin.me/posts/0day-chp10/
https://ceyewan.top/p/e36cdb8.html
https://tzhuobo.gitee.io/2020/05/30/Windows%E5%AE%89%E5%85%A8%E6%9C%BA%E5%88%B6/
https://introspelliam.github.io/2017/07/04/0day/%E7%BB%95%E8%BF%87GS%E5%AE%89%E5%85%A8%E7%BC%96%E8%AF%91%E7%9A%84%E6%96%B9%E6%B3%95/
```



# 利用未被保护的内存突破GS保护

未实现



# 利用虚函数突破GS保护

实验的环境

```
比较的苛刻...也就是要在保护都没开,只开了GS的保护下进行
尽管都关闭了保护,,我也还是失败,,,,不知道为什么...
```



要么是虚函数劫持

感觉要么是this指针替换

我都没有成功的实现

可能是因为我对LinuxPwn忘记了,,,

