

# 遇到的问题

https://www.xitmi.com/10831.html



# 下载+安装



1), 

下载: https://github.com/LSPosed/LSPosed

下载结果是一个zip安装包, 我们用magisk安装它即可.

magisk: 模块-=> 从本地安装-> 选择下载的zip文件

之后重启



2), 之后发现lsposed还是不能用

见文章 https://www.xitmi.com/10831.html

要在主界面开启某个选项



3), 安装后没图标?

在通知状态栏,你注意看看





# helloworld



1), 当前项目的build.gradle

作用:  配置依赖相关

```
dependencies {

    implementation libs.appcompat
    ......

    compileOnly 'de.robv.android.xposed:api:82'
    // compileOnly 'de.robv.android.xposed:api:82:sources' // 不要导入源码，这会导致idea无法索引文件，从而让语法提示失效
}
```



2), 根项目的setting.gradle

作用:  配置依赖相关

```
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url 'https://api.xposed.info/' }  // 添加这一行即可
    }
}
```



3), 当前项目的 src/main/res/value目录中新建`arrays.xml`,内容如下

作用: xposed会作用于一些app,下面内容中包含的apk 会被xposed hook作为推荐项

```
<resources>
    <string-array name="xposedscope" >
        <!-- 这里填写模块的作用域应用的包名，可以填多个。 -->
        <item>ceui.lisa.pixiv</item>
        <item>com.xjs.ehviewer</item>
        <item>com.picacomic.fregata</item>
    </string-array>
</resources>
```



4), 当前项目的AndroidManifest (无activity版)中配置如下

作用:  声明xposed模块的身份信息

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name">

        <!-- 是否是xposed模块，xposed根据这个来判断是否是模块 -->
        <meta-data
            android:name="xposedmodule"
            android:value="true" />
        <!-- 模块描述，显示在xposed模块列表那里第二行 -->
        <meta-data
            android:name="xposeddescription"
            android:value="不可以涩涩" />
        <!-- 最低xposed版本号(lib文件名可知,一般填54即可) -->
        <meta-data
            android:name="xposedminversion"
            android:value="54" />
        <!-- 模块作用域 -->
        <meta-data
            android:name="xposedscope"
            android:resource="@array/xposedscope"/>

    </application>

</manifest>
```





5), 在当前项目 src/main/目录新建目录`assets`,在`assets`中新建文件`xposed_init`

作用: 大概是声明入口类吧

```
├── AndroidManifest.xml
├── assets
│   └── xposed_init
├── java
│   └── com
│       └── example
│           └── x01
│               └── MainHook.java
└── res
    ├── layout
    │   └── activity_main.xml
```

`xposed_init`的文本内容是: 你的当前项目 `包名.入口类`

```
com.example.x01.MainHook
```





6), 下面是一个垃圾的hello world代码

当前xposed模块叫做 `com.example.x01`, 作用于`com.example.xposed`



com.example.x01.MainHook内容如下

```java
package com.example.x01;

import android.util.Log;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

public class MainHook implements IXposedHookLoadPackage {
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        // 过滤不必要的应用
        if (!lpparam.packageName.equals("com.example.xposed"))
            return;
        // 执行Hook
        hook(lpparam);
    }

    private void hook(XC_LoadPackage.LoadPackageParam lpparam) {
        // 具体流程
        Log.d("xposed","Hello Xposed");
    }
}

```

