# adb



```
adb forward tcp:23946 tcp:23946 #端口转发
adb install -t loadso-middle.apk # 测试模式安装
adb logcat | find "dqx_logcat" # 日志过滤输出
adb logcat -c # 清除日志 
adb logcat -s System.err:V*:W #
```



关于 logcat输出乱码问题,在终端输入

```
chcp 65001 
```



# Android shell



am 代表活动管理器

pm 代表包管理器



查看已经安装的apk包

```
pm list packages 
```



进行一个过滤

```
pm list packages uncrackable
```



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





查看apk进程

```
ps -A | grep owasp

# root用户和普通用户都可查看
# 必须输入-A指令,才可与看到大多数进程
# grep做一个筛选
```





查看手机架构

```
getprop ro.product.cpu.abi
```





# wsl中启动adb

貌似linux的adb和win10的exe不能一起用, 导致Linux的adb不能直接连设备

但是我突然发现, wsl可以运行exe,我震惊了, 所以在wsl中启动adb.exe 就可以连接手机了



# ssh连接

https://wiki.termux.com/wiki/Remote_Access

https://oddity.oddineers.co.uk/2020/01/26/ssh-sftp-support-on-android-via-termux/

手机下载apk: Termux

进入Termux终端

```
pkg upgrade
pkg install openssh

whoami #查看用于连接的用户名

passwd #设置当前用户的密码

sshd #开启ssh服务,端口是8022,不是22

ssh-keygen -t rsa -b 2048 -f id_rsa #在home目录,输入指令,生成密钥
```



$PREFIX/etc/ssh/sshd_config



sftp

```
pkg install openssh-sftp-server
sftp -P 8022 192.168.1.20
```



```
pkill sshd
termux-setup-storage
```

