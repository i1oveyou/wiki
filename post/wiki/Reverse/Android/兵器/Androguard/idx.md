https://github.com/androguard/androguard

# analyze

https://blog.csdn.net/qq_40644809/article/details/106814146

```bash
┌──(dqx㉿D0g3)-[~/tmp]
└─$ androguard analyze app-debug.apk 
>>> filename
app-debug.apk
>>> a
<androguard.core.apk.APK object at 0x7f4fa55cd510>
>>> d
[<androguard.core.dex.DEX object at 0x7f4fa54f1d50>, <androguard.core.dex.DEX object at 0x7f4fa54f0690>, <androguard.core.dex.DEX object at 0x7f4f9fdb0690>, <androguard.core.dex.DEX object at 0x7f4f9fd56610>]
>>> dx
<analysis.Analysis VMs: 4, Classes: 7791, Methods: 62128, Strings: 77109>

```

## a

a：表示 APK 对象，在其中可以找到有关 APK 的信息，例如包名、权限、AndroidManifest.xml、resources。 AndroidManifest.xml：每一个 Android 项目的根目录下都包含一个 Manifest 文件 AndroidManifest.xml，它是 XML 格式的 Android 程序声明文件。其中包含 Android 系统运行程序前所必须掌握的重要信息，例如应用程序名称、图标、包名称、模块组成、授权和 SDK 最低版本等。

## d

d：表示 DalvikVMFormat 对象数组，DalvikVMFormat 对应 apk 文件中的 dex 文件，从 dex 文件中我们可以获取类、方法和字符串。 dex 是 Android 平台上( Dalvik 虚拟机)的可执行文件，相当于 Windows 平台中的 exe 文件，每个 Apk 安装包中都有 dex 文件，里面包含了该 app 的所有源码，通过反编译工具可以获取到相应的 java 源码。

```
In [16]: d
Out[16]: 
[<androguard.core.dex.DEX at 0x7f4fa54f1d50>,
 <androguard.core.dex.DEX at 0x7f4fa54f0690>,
 <androguard.core.dex.DEX at 0x7f4f9fdb0690>,
 <androguard.core.dex.DEX at 0x7f4f9fd56610>]
In [14]: type(d)
Out[14]: list
In [18]: type(d[0])
Out[18]: androguard.core.dex.DEX
```

## dx

dx：表示 Analysis 对象，其包含链接了关于 classes.dex 信息的特殊的类，甚至可以一次处理许多 dex 文件 