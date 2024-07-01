# Reference Documents




[1](https://blog.ketal.icu/cn/Xposed%E6%A8%A1%E5%9D%97%E5%BC%80%E5%8F%91%E5%85%A5%E9%97%A8%E4%BF%9D%E5%A7%86%E7%BA%A7%E6%95%99%E7%A8%8B/#%E4%BB%8B%E7%BB%8D)

[2](https://zwc365.com/2020/06/09/xposed-hook)

[3](https://blog.51cto.com/u_16213702/8681813)

[4,不错的文章](https://blog.51cto.com/u_16213702/8681813)

[5](https://www.eet-china.com/mp/a161045.html)

[6,不错的文章](http://nunu03.github.io/2019/07/02/xposed/)



# Xposed原理分析	



Xposed框架的原理是修改系统文件，替换了`/system/bin/app_process`可执行文件，

Zygote=`/system/bin/app_process`, zygote进程是由init进程启动起来,  

- Zygote 是 Android 系统启动时最先启动的进程之一,它是系统中所有应用程序进程的父进程。 Zygote是所有进程的孵化进程
- 当 Android 系统需要启动一个新的应用程序进程时,会通过 fork 出一个新的进程,并由这个新进程加载应用程序的代码和资源。这个新进程就是从 Zygote 进程 fork 出来的。
- Zygote 进程在启动时会预加载大量的系统库和资源,包括 Java 虚拟机、Android 系统库等,这些内容会被所有后续启动的应用程序进程共享,从而减少内存占用。

安装了Xposed的手机, 在启动Zygote时加载额外的jar文件（`/data/data/de.robv.android.xposed.installer/bin/XposedBridge.jar`）

并执行一些初始化操作(执行XposedBridge的main方法), 然后开发人员就可以在这个Zygote上下文中进行某些Hook操作。

Xposed 提供了几个接口类供 Xposed 模块继承,不同的接口类对应不同的 hook 时机:

- `IXposedHookZygoteInit`   Zygote 初始化前就执行挂钩,即 `loadModule()` 执行时就挂钩了。

- `IXposedHookLoadPackage`  当 APK 包加载时执行挂钩。它会先将挂钩函数保存起来,等加载 APK 函数执行后触发回调 (这里的回调是 Xposed 框架自己挂钩的函数),再执行模块注册的挂钩函数。

- `IXposedHookInitPackageResources `  当 APK 资源实例化时执行挂钩,同上



# Hello Xposed



从本质上来讲，Xposed 模块也是一个 Android 程序



```java
package com.example.x01;

import android.util.Log;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

public class MainHook implements IXposedHookLoadPackage {
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        // 过滤不必要的应用
        if (!lpparam.packageName.equals("com.example.helloworld"))
        {
            //不是com.example.helloworld就返回
             return;
        }
        // 执行Hook
        hook(lpparam);
    }

    private void hook(XC_LoadPackage.LoadPackageParam lpparam) {
        // 具体流程
        Log.d("echo_xposed","Hello,Xposed!");
    }
}
```





xposed能干嘛?

- hook 函数
  - 修改入口参数 
  - 修改返回结果
  - 提前返回 return
  - 替换函数
- 调用内部函数

# handleLoadPackage



## XposedHelpers.findAndHook



```java
package com.example.x01;

import android.util.Log;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;


public class MainHook implements IXposedHookLoadPackage {

    static  String strTag="echo_Xposed";
    
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable 
    {
        
        
        // 构造函数
        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",//这个是具体的class类的路径
                loadPackageParam.classLoader,
            	//... 参数类型
                new XC_MethodHook() {});
        
        //普通函数
        XposedHelpers.findAndHookMethod(
                "com.example.demo.MortgageActivity", 
                loadPackageParam.classLoader,
                "showLoan", 
                //有参数就写,没就不写
                new XC_MethodHook() {});
    }
}
```





### XC_Method



#### 类型

```java

//import de.robv.android.xposed.XC_MethodHook;

new XC_MethodHook() 
{
    @Override
    protected void beforeHookedMethod(MethodHookParam param) throws Throwable 
    {
        super.beforeHookedMethod(param);
        //在before中设置返回值,可跳过函数执行
    }

    @Override
    protected void afterHookedMethod(MethodHookParam param) throws Throwable 
    {
        super.afterHookedMethod(param);


    }
}


new XC_MethodReplacement() {
    @Override
    protected Object replaceHookedMethod(MethodHookParam methodHookParam) throws Throwable 
    {
        // 直接替换原来要执行的逻辑代码,目标方法就不在执行了
        try 
        {
            // 直接替换原来要执行的逻辑代码,目标方法就不在执行了
        } 
        catch (Throwable t) 
        {
            XposedBridge.log(t);
        }  
        return null;
    }
}

```





#### 对field做出行为



```java
//修改参数
Object[] objectArray = param.args;
objectArray[0] = "{XXXX:";



//静态field
Field school_id_Field = param.thisObject.getClass().getDeclaredField("school_id");
school_id_Field.setAccessible(true);
school_id_Field.setInt(null, 8);

//普通field
Field student_name_Field = param.thisObject.getClass().getDeclaredField("student_name");
student_name_Field.setAccessible(true);
student_name_Field.set(param.thisObject, "hacker-01");


//通过xposed接口设置static属性
XposedHelpers.setStaticObjectField(
    param.thisObject.getClass(),//class类,它的获取方式有很多
    "school_id", 
    12
);


//通过xposed接口设置对象属性
XposedHelpers.setObjectField(
    param.thisObject, 
    "student_name", 
    new String("hacker-02")
);

//XposedHelpers.findField()

```



#### 返回值



```
//设置返回值
param.setResult("YYYY");
//得到返回值
param.getResult()
```





#### 函数调用

```java
1),
Object object = XposedHelpers.callStaticMethod(clazz, "staticPrivateMethod", "callStaticMethod 静态函数调用");

2),
XposedHelpers.callMethod(param.thisObject, "getinfo", "{XXXX: ");

3),
Method SetSchoolIDAndGetNameMethod = param.thisObject.getClass().getDeclaredMethod(
    "getinfo",
    String.class
);
SetSchoolIDAndGetNameMethod.setAccessible(true);
String result=(String) SetSchoolIDAndGetNameMethod.invoke(param.thisObject, "{XXXX: ");
```



# so

此处这个hook指的是 替换加载的so文件, 而不是对so自身内容进行一个hook



xposed本身是一个java层的hook框架，因此使用xposed的接口只能实现对apk的java层代码的hook。

要想进行native层（so文件）的hook需要结合其他hook 框架，例如android-inline-hook。



apk一般通过System.LoadLibrary加载自己的so库，要想在so库中函数没有执行前就进行hook的话需要在利用xposed对System.LoadLibrary函数设置hook，

并在此函数调用之后调用自己的回调函数并对native层的代码进行hook。

 

 但hook时,我们是对`java.lang.Runtime.LoadLibrary0`

为什么不`java.lang.System.LoadLibrary`, 而是`java.lang.Runtime.LoadLibrary0`?



```java
public static void loadLibrary(String libname) {
    Runtime.getRuntime().loadLibrary0(Reflection.getCallerClass(), libname);
}
    
void loadLibrary0(Class<?> fromClass, String libname) {
    ClassLoader classLoader = ClassLoader.getClassLoader(fromClass);
    loadLibrary0(classLoader, fromClass, libname);
} 
```





因为`java.lang.System.LoadLibrary`的原理是获取调用者当前函数所归属的类和so的名字,

然后作为参数传递给`java.lang.Runtime.LoadLibrary0`

如果Xposed Hook了java.lang.System.LoadLibrary,那么Reflection.getCallerClass()返回值就是Xposed, 这样就会导致找不到so的文件





```java
public class XposedHookTest implements IXposedHookLoadPackage {
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable {
        XposedBridge.log("load apk: " + loadPackageParam.packageName);
        XposedHelpers.findAndHookMethod(
                "java.lang.Runtime",
                loadPackageParam.classLoader,
                "loadLibrary0",
                Class.class,
                String.class,
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        //to native hook
                    }
                }
        );
    }
}
```



# class的获取方式



## 常见的



```java
String.class,
int.class
byte.class
byte[].class

XposedHelpers.findAndHookConstructor(
        "com.example.helloworld.test.Student",//这个是具体的class类的路径
        loadPackageParam.classLoader,
        new XC_MethodHook()
);

Class StudentClass = loadPackageParam.classLoader.loadClass("com.example.helloworld.test.Student");

final Class<?> tarClass = XposedHelpers.findClass(“全路径类名”, loadPackageParam.classLoader);

param.thisObject.getClass()
```



## 内部类

内部类尽管是内部, 但它始终是有名字的

所以内部类的获取如下 `主类$内部类类目`

```java
package com.example.helloworld.test;

public class Student {

    public class calcScore {

    }
   
}
```



那么获取的话

```java
final Class<?> clazz1 = XposedHelpers.findClass(
    "com.example.helloworld.test.Student$calcScore", 
    loadPackageParam.classLoader
);
```





## 匿名类

这个因为是匿名的,所以没有具体的字符串名字, 但同内部类一样,作用域属于父类

```
├── Student$1.smali
├── Student$calcScore.smali
├── Student$echo_info.smali
└── Student.smali
```

`Student$1.smali`就属于一个匿名类, 类的获取如下

```java
final Class<?> clazz1 = XposedHelpers.findClass(
    "com.example.helloworld.test.Student$1", 
    loadPackageParam.classLoader
);
```





## 复杂类



```java
public void paramsClass(
    ClasName cn, 
    String value,
    Intent intent,
    int key,
    Map map,
    List list){  
	//...
}
-------------------------------------------------------------------
final Class<?> clazz = XposedHelpers.findClass("全路径类名", loadPackageParam.classLoader);
Class cnClazz  = loadPackageParam.classLoader.loadClass("com.xxxx. ClasName");
Class cnMap = XposedHelpers.findClass("java.util.Map", loadPackageParam.classLoader);
Class cnArrayList = XposedHelpers.findClass("java.util.ArrayList", loadPackageParam.classLoader);

XposedHelpers.findAndHookMethod(
	clazz, 
	"paramsClass", 
	cnClazz, 
	String.class, 
	Intent.class,
	int.class,
	Map.class,
	ArrayList.class 
	new XC_MethodHook() {
        @Override
        protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
        
        	//...
    	}
});
```

