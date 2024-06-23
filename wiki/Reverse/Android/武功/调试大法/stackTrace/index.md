



链接：https://pan.baidu.com/s/15E-3v4wSRaZWbmqaJTLW_A?pwd=rpu7 

提取码：rpu7

通过输出函数的调用栈来查看调用的流程

从方法角度来讲，和log的smali注入没太大的区别

于是我

呃，为了方便注入，依照log.d的l0gcat.smali文件，插入一函数

实现的效果是 `new Exception("print trace").printstackTrace();`

具体如下

```smali
.class public Ll0gcat;
.super Ljava/lang/Object;
.source "l0gcat.java"
 
.method public static log_str(Ljava/lang/String;)V
    .locals 1
    .prologue
 
    const-string v0, "apple_string"
    invoke-static {v0, p0}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    return-void
.end method

.method public static log_int(I)V
    .locals 2
 
    .prologue
 
    const-string v0, "apple_int"
 
    invoke-static {p0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;
 
    move-result-object v1
 
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
 
    return-void
.end method

.method public static log_stack()V
    .locals 2
 
    .prologue
 
    # new Exception("print trace").printstackTrace();

    new-instance v0, Ljava/lang/Exception;

    const-string v1, "apple_stack"

    invoke-direct {v0,v1}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V 

    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V 
 
    return-void
.end method
```

逆向分析apk：crackme_01-debug.apk

发现他有一个弹窗toast，于是我们找到API: Toast的位置

然后在它那里插入打印函数栈的代码

```smali
.method private c()V
    .locals 2

    .line 32
    const-string v0, "who called me?"

    const/4 v1, 0x0

    invoke-static {p0, v0, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    # 插入部分
    invoke-static {}, Ll0gcat;->log_stack()V

    .line 33
    return-void
.end method
```

其它的操作什么的，效仿log注入



我们打开adb的logcat，然后启动apk

发现输出如下。

调用层次是onCreate()->a()->b()->c()

```bash 
C:\Users\xxxx>adb logcat -c

C:\Users\xxxx>adb logcat -s System.err:V*:W
--------- beginning of main
--------- beginning of system
06-16 17:12:06.771  6609  6609 W System.err: java.lang.Exception: apple_stack
06-16 17:12:06.771  6609  6609 W System.err:    at l0gcat.log_stack(l0gcat.java)
06-16 17:12:06.771  6609  6609 W System.err:    at com.example.crackme_01.MainActivity.c(MainActivity.java:32)
06-16 17:12:06.771  6609  6609 W System.err:    at com.example.crackme_01.MainActivity.b(MainActivity.java:28)
06-16 17:12:06.771  6609  6609 W System.err:    at com.example.crackme_01.MainActivity.a(MainActivity.java:24)
06-16 17:12:06.771  6609  6609 W System.err:    at com.example.crackme_01.MainActivity.onCreate(MainActivity.java:20)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.Activity.performCreate(Activity.java:6237)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1107)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2369)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:2476)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.ActivityThread.-wrap11(ActivityThread.java)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1344)
06-16 17:12:06.771  6609  6609 W System.err:    at android.os.Handler.dispatchMessage(Handler.java:102)
06-16 17:12:06.771  6609  6609 W System.err:    at android.os.Looper.loop(Looper.java:148)
06-16 17:12:06.771  6609  6609 W System.err:    at android.app.ActivityThread.main(ActivityThread.java:5417)
06-16 17:12:06.771  6609  6609 W System.err:    at java.lang.reflect.Method.invoke(Native Method)
06-16 17:12:06.771  6609  6609 W System.err:    at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
06-16 17:12:06.771  6609  6609 W System.err:    at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
```

