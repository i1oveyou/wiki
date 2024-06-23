# grub开启启动时间



```
su
mousepad  /etc/default/grub
```

会看到如下内容

```
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
GRUB_CMDLINE_LINUX=""
```

把GRUB_TIMEOUT设置为你需要的时间即可

然后输入 `update-grub`





# ssh

https://www.cnblogs.com/wlanjsfx/p/15150196.html



```
┌──(kali㉿G16-7620)-[~]
└─$ sudo vim /etc/ssh/sshd_config


passworAuthentication yes
```

,

```

┌──(kali㉿G16-7620)-[~]
└─$ sudo service ssh start
Starting OpenBSD Secure Shell server: sshd.

┌──(kali㉿G16-7620)-[~]
└─$ sudo update-rc.d ssh enable

┌──(kali㉿G16-7620)-[~]
└─$ sudo service ssh status
sshd is running.
```



# 软件 



查看已安装的软件

```
1), dpkg -l 
2), sudo apt list --installed
3), 分页查看 sudo apt list --installed | less
```



## 卸载



```
# 删除软件及其配置文件
apt --purge remove <package>


# 删除没用的依赖包
apt autoremove <package>

# 此时dpkg的列表中有“rc”状态的软件包，可以执行如下命令做最后清理：
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P
```

## 环境变量



输出环境变量

```
echo $PATH    
```



临时修改环境变量

```
 export PATH=/usr/local/webserver/mysql/bin:$PATH
```



永久修改环境变量（比如当前用户是dqx）` .profile`和`.bashrc`都可以,但喜欢用`.profile`

```
┌──(dqx㉿D0g3)-[~]
└─$ vim ~/.profile
```

然后在文本最后一行添加你要的环境变量

比如添加 /home/dqx/.local/bin

写入的内容是

```
export PATH="/home/dqx/.local/bin:$PATH"
```

之后保存，然后

```
┌──(dqx㉿D0g3)-[~]
└─$ source ~/.profile
```

输出一下是否成功修改

```
echo $PATH 
```

