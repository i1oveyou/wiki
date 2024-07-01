---
title: "env-Python"
---



# pip卸载



查看安装的包

```
$ pip list
```



卸载

```
$ pip uninstall django
```



# pip下载



下载默认最新版

```
pip install ...
```



下载指定版本

```
pip install xxx==yyy
```



清楚缓存

```
pip cache purge

```

# pip永久修改源



临时

```
pip3 install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```



永久修改

> linux：



创建目录 ~/.pip

创建文件 ~/.pip/pip.conf

写入内容

```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

然后输出查看一下

```
pip3 config list 
```



> win10:

创建目录 C:\Users\用户名\pip

创建文件 C:\Users\用户名\pip\pip.ini

一样的写入之前的文件内容
