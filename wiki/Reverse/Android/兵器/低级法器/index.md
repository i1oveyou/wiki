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

