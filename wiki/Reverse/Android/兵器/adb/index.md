

# adb



```
adb forward tcp:23946 tcp:23946
adb install -t loadso-middle.apk
adb logcat | find "dqx_logcat"
adb logcat -c
adb logcat -s System.err:V*:W
```







# shell

am 代表活动管理器，

pm 代表包管理器







启动apk

```
am start -n com.example.txtshow/.MainActivity
```



临时设置为调试启动

```
am start -D -n xx/xx.yyyy
```





永远设置为调试启动

```
am set-debug-app -w --persistent owasp.mstg.uncrackable1

# 清空调试配置
adb shell am clear-debug-app
```



查看启动的类

```
pm resolve-activity --brief -c android.intent.category.LAUNCHER com.example.txtshow | tail -n1
com.example.txtshow/.MainActivity
```







查看已安装的包

```
pm list packages  
```



过率效果

```
pm list packages uncrackable
# 名称含有uncrackable的包
```



查看apk进程

```
ps -A | grep owasp

# root用户和普通用户都可查看
# 必须输入-A指令,才可与看到大多数进程
# grep做一个筛选
```



# wsl中启动adb

貌似linux的adb和win10的exe不能一起用, 导致Linux的adb不能直接连设备

但是我突然发现, wsl可以运行exe,我震惊了.



