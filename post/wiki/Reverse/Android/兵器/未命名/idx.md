# 大杂烩

https://book.crifan.org/books/android_re_static_analysis/website/

# MOSF

一个类似于virustotal东西, 扫描apk,然后解析它

https://mobsf.live/

### Androguard

https://github.com/androguard/androguard

功能：

- 主要用来进行静态分析安卓程序

- 也可以用第三方库去反编译安卓

  包括多个模块/子功能

- `androrisk.py`：该模块用于分析apk危险级别
- `androapkinfo.py`：该模块分析apk列出其中的文件类型、权限、4大组件、是否NDK反射等信息
- `androaxml.py`：该模块用于解密 androidmanifest.xml
- `androgexf.py`：该模块生成函数调用图
- `apkviewer.py`：该模块生成指令级别的调用图
- `androlyze.py`：该模块为交互分析环境
- androdd.py: 用来生成apk每个类的调用流程图
- androidff.py: 对比2个apk的差异
- androdump.py: dump linux进程信息
- androguard+Gehpi：蜘蛛网的交叉引用
