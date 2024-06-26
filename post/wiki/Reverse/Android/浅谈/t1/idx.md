# ---Android 入门的一点心得 

# JAVA 层的逆向



## 常见静态分析手法



### 信息收集

一个 apk，前期对其的一些信息收集是很有必要的，别拿到一个 apk 就马上反编译看代码去了。注意抓住重点。打蛇打七寸。首先关注其字符串信息，服务，广播等等



### 关键位置定位	

定位，是一个技术活。这里面有很多的奇淫巧计，需要大家练习。通过“特征函数”定位，

比如说控件的事件函数 onXXXClick, Show(),

如果你要找网络方面的信息HttpGet、HttpPost、HttpUriRequest、socket 等等，

追踪隐私 IMSI、IMEI,敏感操作，发送短信、拨打电话等等



### 活用 logcat

logcat 在之前还未出现动态调试 smali 的时候，可谓是逆向分析者们手中的一大利器。logcat 中包含了程序原有的一些调试信息，这些往往是不够用的。这便有了“smali 注入”



### smali 注入

通过向反编译之后的代码中插入自己的代码，重打包之后，使程序运行之后，在 log 中打印出目标函数的参数，返回值等我们想知道的任何东西。这样，就达到了半动态调试 apk 的作用。smali 注入对 smali 语法的功能要求得稍微高一点，而且会遇到很多不确定因素。需要多多尝试。

## 常见动态调试手法

听说有些工具可以 可以在配置文件中预下断点，批量下断点，给系统函数下断点 

# Native 层的逆向

## Native 的开发

要想学好逆向，首先得会编写 native 程序。熟练常见的系统 api 以及开发流程等等

## Native 层相关机制的学习

这部分需要去分析源代码中 jni 的部分内容

## 静态分析+动态分析

# 进阶篇之源码分析

和 windows 平台上的逆向差不多，要想更深入的学习下去 ，了解这个系统的一些原理，底层上的东西是很有必要的 。android 给我们提供了很大的便利。它是开源的。

# ---浅谈 android 逆向分析那些拦路虎

# 混淆

普通混淆：类名、变量名、函数名变成 a、b、c 这种，最常见

自定义混淆：类名、变量名、函数名变成 0oOO0o、li1Ll 这种，你看 smali 就眼花撩乱

unicode 混淆： ?类名、变量名、函数名变成 中文乱码，样本是 豌豆荚

## 反混淆？

这和IDA分析exe一样，不断的理解代码，然后重命名。

如果敌人混淆不完全，留下一些蛛丝马迹，比如留下混淆前的类名

```
.class public interface abstract La/b/a;
.super Ljava/lang/Object;
.source "IWindowManager.java"
```

# 触发反编译工具的 bug

触发反编译工具漏洞的 bug 使反编译工具崩溃而正常的反编译

- 加入垃圾类，里面包含不正确的指令
- 超长类或数组
- 不存在的类指向
- 文件后缀和文件魔术头不符
- .9 文件
- values 里加一个字符串资源，值等于“/res”
- 空资源

这种五花八门，就不再列举，apktool 现在修复了好多 bug，目前碰到问题大多是资源那块

# 完整性检测

签名、dex 文件 md5 和 hash 等

# 动态加载

# dex 修改处理

现在主流加固商都对 dex 的结构进行修改，内存我们内存 dump 出来的 dex 不是完整的，需要经过修正，碰到样本特征如下:

- 方法隐藏，指向空函数
- 函数方法都是 native
- 动态修改字节码
- 函数 hook 重定向

可以看看这样子：

```assembly
# direct methodsisters 1
.prologue
.line 34
nop
nop
nop
nop可以看看这样子：
.end method
```





# so 加壳

这个就不详谈了，大概的原理是：把源码的 dlopen 复制出来修改，在把自己 so 加载起来的时候 ,把自己内存里面某部分地址解密后,用自己的 dlopen 打开返回一个 soinfo 结构体 然后把当前 soinfo 结构体替换原来的 soinfo 结构体

> 谈谈我对脱壳的想法

经过一段时间的研究，也大概了解 apk 加固的基本原理。不管如何加固，apk 运行时终归要把隐藏的 dex 解密加载，虽然可以 dump，但是 dex 解密修改一般是修正内存的 DexFile 结构，而不影响到内存映射的那部分 dex（因此我们 dump 出来还是未修正的），我们想拿到一个正确的 dex，要从修正内存的 DexFile 结构开始解析。跟加固的小伙伴提过我的想法:

- [0]从内存修正的 dexfile 逆推回去，还原正确的 dex

- [1]在内存中反编译

hoho，后面出现了脱壳神器 ZjDroid，移植了 baksmali，把正确的 dex 内存指向给 baksmali，在内存中反编译，