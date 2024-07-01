---
title: wiki-Reverse-Android-防守-金钟罩铁布衫
---




> handleLoadPackage(称之为A)回调函数会在apk加载时, 由xposed的在XposedInit函数调用
>



related: https://blog.51cto.com/u_16213702/8681813

1),

handlebindapplication(称之为B) 被Xposed Hook了

A: handleLoadPackage

B: handlebindapplication

A函数会先于B函数执行

B函数会进行一些初始化并调用Application的attachBaseContext函数。

通常情况下壳代码是在自己的Application.attachBaseContext函数中修正classloader为自定义的classloader并动态加载源程序的dex文件

所以xposed在B调用之前获取的classloader并作为参数传递给A函数并不是有效的classloader，

所以对于加壳的apk需要通过反射获取修正后的真正的classloader。hook操作时使用此ClassLoader即可，其他操作与为加壳apk一致。



2),

自定义classloader的hook和加壳apk的hook的情况很相似，重点就是找到正确的classloader。

apk通过自定义classloader加载apk的dex文件，这个时候需要获取到apk自定义的classloader后才能对此自定义的classloader加载的dex文件中的java类进行hook。

方法就是对DexClassLoader，PathClassLoade和InMemoryDexClassLoader的构造函数并获取到返回的classloader。