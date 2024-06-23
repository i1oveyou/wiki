---
title: Hello World
tags: demo-tag
categories: demo-dir
---
Welcome to [Hexo](https://hexo.io/)! This is your very first post. Check [documentation](https://hexo.io/docs/) for more info. If you get any problems when using Hexo, you can find the answer in [troubleshooting](https://hexo.io/docs/troubleshooting.html) or you can ask me on [GitHub](https://github.com/hexojs/hexo/issues).

 	

# Quick Start

 

### Search

插件安装

```
npm install hexo-generator-search --save
```

在根目录的 _config.yml 添加如下
```
search:
  path: search.xml
  field: post
```



### npm国内源



一、修改成腾讯云镜像源

1),命令

npm config set registry http://mirrors.cloud.tencent.com/npm/

2),验证命令

npm config get registry

如果返回http://mirrors.cloud.tencent.com/npm/，说明镜像配置成功



一、修改成华为云镜像源

1. 命令

npm config set registry https://mirrors.huaweicloud.com/repository/npm/

2. 验证命令

npm config get registry

如果返回https://mirrors.huaweicloud.com/repository/npm/，说明镜像配置成功。



### hexo

```
mkdir hexo
cd hexo
hexo init
npm install
npm install hexo-deployer-git --save
```



```
git config --global user.name "你的昵称" 
git config --global user.email "你的邮箱"
ssh-keygen -t rsa -C "你的昵称"
```





```
deploy:
  type: git
  repository: 你复制的ssh
  branch: master
```

