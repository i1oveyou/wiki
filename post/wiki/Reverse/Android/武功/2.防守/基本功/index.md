---
title: wiki-Reverse-Android-防守-基本功
---




# root 检测



## 环境变量中的su

在 Android-UnCrackable-L1,  Android-UnCrackable-L2, Android-UnCrackable-L3 有应用

检测一些环境变量中有没有su

一个root的设备是可以直接输入 su 进行提权的. 同时su存在于环境变量中. 以此作为root的检测手段



```java
    public static boolean checkRoot1(){
        for(String pathDir : System.getenv("PATH").split(":")){
            if(new File(pathDir, "su").exists()) {
                return true;
            }
        }
        return false;
    }
```



## 和root有关的apk或者可执行程序

在 Android-UnCrackable-L1,  Android-UnCrackable-L2, Android-UnCrackable-L3 有应用



有些软件可以把手机root掉,

有些软件是利用root干其它事情

如果手机安装了这些软件,大概说明当前手机已经被root了



```java
    public static boolean checkRoot3() {
        String[] paths = { "/system/app/Superuser.apk", "/system/xbin/daemonsu",  "/system/etc/init.d/99SuperSUDaemon", "/system/bin/.ext/.su", "/system/etc/.has_su_daemon", "/system/etc/.installed_su_daemon", "/dev/com.koushikdutta.superuser.daemon/" };

        for (String path : paths) {
            if (new File(path).exists()) return true;
        }
        return false;
    }
```



```
"/system/app/Superuser.apk",
"/system/xbin/daemonsu", 
"/system/etc/init.d/99SuperSUDaemon", 
"/system/bin/.ext/.su",
"/system/etc/.has_su_daemon",
"/system/etc/.installed_su_daemon", 
"/dev/com.koushikdutta.superuser.daemon/"
```





# 检测当前设备是不是 开发者模式

在 Android-UnCrackable-L1,  Android-UnCrackable-L2, Android-UnCrackable-L3 有应用



```java
   public static boolean checkRoot2() {
        String buildTags = android.os.Build.TAGS;
        return buildTags != null && buildTags.contains("test-keys");
    }
```









# 反调试



## java: FLAG_DEBUGGABLE

在 Android-UnCrackable-L1,  Android-UnCrackable-L2, Android-UnCrackable-L3 有应用

检测标志位,这个貌似在AndroidManifest.xml中有

检测当前apk是否具备可调式的属性, 作为一个release的apk是不可调试的.



```java
    public static boolean isDebuggable(Context context){

        return ((context.getApplicationContext().getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0);

    }
```



## java: 检测是否被调试器连接

在Android-UnCrackable-L2, Android-UnCrackable-L3,有应用



开一后台线程,一直检测是否有调试器连接当前apk进程,

```java
        // Debugger detection
        new AsyncTask<Void, String, String>() {

            @Override
            protected String doInBackground(Void... params) {
                while (!Debug.isDebuggerConnected()) {
                    SystemClock.sleep(100);
                }
                return null;
            }

            @Override
            protected void onPostExecute(String msg) {
                showDialogAndExit("Debugger detected!");
            }
        }.execute(null, null, null);
```





## so: 子进程attach父进程



大概的效果, apk变为了2个进程

父进程被子进程调试

子进程一直处于debug循环,又没啥好调试的.











# 防篡改



在 Android-UnCrackable-L3, 有应用



java层, 也就是检测 class.dex , xxx.so 是否被修改过

```java
private void verifyLibs() {

        crc = new HashMap<String, Long>();
        //mips, mips64 and armeabi are no longer supported with the new buildtools
//        crc.put("armeabi", Long.parseLong(getResources().getString(R.string.armeabi))); //"1054637268"
//        crc.put("mips", Long.parseLong(getResources().getString(R.string.mips))); //"3104746423"
        crc.put("armeabi-v7a", Long.parseLong(getResources().getString(R.string.armeabi_v7a))); //"881998371"
        crc.put("arm64-v8a", Long.parseLong(getResources().getString(R.string.arm64_v8a))); //"1608485481"
//        crc.put("mips64", Long.parseLong(getResources().getString(R.string.mips64))); //"1319538057"
        crc.put("x86", Long.parseLong(getResources().getString(R.string.x86))); //"1618896864"
        crc.put("x86_64", Long.parseLong(getResources().getString(R.string.x86_64)));  //"2856060114"

        try {
            ZipFile zf = new ZipFile(getPackageCodePath());

            for (Map.Entry<String, Long> entry : crc.entrySet()) {

                String filename = "lib/" + entry.getKey() + "/libfoo.so";

                ZipEntry ze = zf.getEntry(filename);

                Log.v(TAG, "CRC[" + filename + "] = " + ze.getCrc());

                if (ze.getCrc() != entry.getValue()) {
                    //tampered = 31337;
                    Log.v(TAG, filename + ": Invalid checksum = " + ze.getCrc() + ", supposed to be " + entry.getValue());

                }

            }

            String filename = "classes.dex";
            ZipEntry ze = zf.getEntry(filename);

            Log.v(TAG, "CRC[" + filename + "] = " + ze.getCrc());

            if (ze.getCrc() != baz()) { // baz()=25235683LL
                //tampered = 31337;
                Log.v(TAG, filename + ": crc = " + ze.getCrc() + ", supposed to be " + baz());

            }

        } catch (IOException e) {
            Log.v(TAG, "Exception");
            System.exit(0);
        }
    }
```







# 混淆



## java层的混淆:

- Android-UnCrackable-L1 :轻度混淆, 只是修改一些变量,函数,类的名字.
- Android-UnCrackable-L2: 在L1的程度上, L2增添了很多无用的,  乱七八糟的类. 或者并没有增加,把已有的类修改的乱七八糟
- Android-UnCrackable-L3: 在L1的程度上, 3增添了很多无用的,  乱七八糟的类. 或者并没有增加,把已有的类修改的乱七八糟





解决办法:

理解相关代码, 分析并重命名



## so层混淆:llvm

见Android-UnCrackable-L4-0.9了



## so层混淆: 函数复杂多样化

函数复杂多样化就是把 一个很简单的东西写得很复杂复杂, 但因为本质很简单, 只要看破就很好理解.





>  Android-UnCrackable-L2

CodeCheck.bar中, out数组赋值代码, 是一个看上去简单, 实际上也很简单的一个数据赋值

但因为高内聚,低耦合, 复杂的函数功能却比较单一, 又因为编译器的原因

导致out数组的赋值变得很简单,甚至找不到复杂的痕迹

```
UnCrackable-Level2
--lib
----arm64-v8a
------libfoo.so
--------CodeCheck.bar(JNIEnv *env, jobject, jbyteArray in)
```







>  Android-UnCrackable-L3



```
UnCrackable-Level3
--lib
----arm64-v8a
------libfoo.so
--------CodeCheck.bar(JNIEnv *env, jobject, jbyteArray in)
----------- sub_doit((char*)out);
```



sub_doit(char* barr)是一个看上去很复杂的函数,

但是因为高内聚,低耦合的原因,功能又比较单一. 也就是一个赋值函数







# so层: init_array 手段

在 Android-UnCrackable-L3, 有应用

也就是在elf加载的时, 先于main函数的的一种东西

类似于exe的tls.

该函数的执行需要被注册. 注册后一般存在于`.init_array`节区

```
UnCrackable-Level3
--lib
----arm64-v8a
------libfoo.so
--------_start()

# 检测xposed,frida ???
# 数据初始化
```







```c
__attribute__((constructor)) static void _start(void) {
    pthread_t t;

    pthread_create( &t, NULL, __somonitor_loop, NULL );
	
    //__somonitor_loop 用于检测xposed,frida ???
    memset(x, 0, 25);

    initialized += 1;

    return;
}

void  __attribute__ ((visibility ("hidden"))) *__somonitor_loop(void *) {

    char line[512];

    FILE* fp;

    while (1) {
        fp = fopen("/proc/self/maps", "r");

        if (fp)
        {

            while (fgets(line, 512, fp))
            {
                if (strstr(line, "frida") || strstr(line, "xposed")) {

                    __android_log_print(ANDROID_LOG_VERBOSE, APPNAME, "Tampering detected! Terminating...");

                    goodbye();

                }

            }
            fclose(fp);
        } else {
            __android_log_print(ANDROID_LOG_VERBOSE, APPNAME, "Error opening /proc/self/maps! Terminating...");

            goodbye();
        }

        usleep(500);
    }

}
```











# 其它

通过源码,其实发现还有很多东西,很多知识点,很多反破解手法是我所不了解的, 所以此刻并未提出

日后有缘再来分析分析.