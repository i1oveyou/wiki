

# 可Hook项



## Constructor

XposedHelpers.findAndHookConstructor



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
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable {
        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",//这个是具体的class类的路径
                loadPackageParam.classLoader,	
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(strTag, "无参构造 hook success!");
                    }
                }
        );

        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",
                loadPackageParam.classLoader,
                String.class,
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(strTag, "有参构造 hook success!");
                    }
                }
        );
    }
}
```





## Field

我们在构造函数之中修改class成员为例,  不一定是在构造函数





```
final Class<?> clazz = XposedHelpers.findClass(“全路径类名”, loadPackageParam.classLoader);

// XposedHelpers.setStaticObjectField( clazz, )
// XposedHelpers.setStaticObjectField( param.thisObject.getClass(), )
```





XposedHelpers.setObjectField( param.thisObject)

貌似他们 都是这么用的



```java
package com.example.x01;

import android.util.Log;


import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

import java.lang.reflect.*;

public class MainHook implements IXposedHookLoadPackage {

    static  String strTag="echo_Xposed";
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable {
        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",
                loadPackageParam.classLoader,
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(strTag, "无参构造hook success!");

                        //通过反射设置static属性
                        Field school_id_Field = param.thisObject.getClass().getDeclaredField("school_id");
                        school_id_Field.setAccessible(true);
                        school_id_Field.setInt(null, 8);
                        
                        //通过反射设置对象属性
                        Field student_name_Field = param.thisObject.getClass().getDeclaredField("student_name");
                        student_name_Field.setAccessible(true);
                        student_name_Field.set(param.thisObject, "hacker-01");
                    }
                }
        );

        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",
                loadPackageParam.classLoader,
                String.class,
                int.class,
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(strTag, "有参构造hook success!");

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
                    }
                }
        );
    }

}

```











```
lpparam.packageName.equals("com.example.xposed")
```



函数执行前

```
beforeHookedMethod
```



函数执行后的调用

```
afterHookedMethod
```



```
XposedHelpers.findField()
```



# findAndHookMethod

XposedHelpers.findAndHookMethod()函数一般四个参数，分别为完整类名、ClassLoader对象、函数名以及一个回调接口

```java
XposedHelpers.findAndHookMethod(
	"com.example.demo.MortgageActivity", 
	loadPackageParam.classLoader,
        "showLoan", 
        //有参数就写,没就不写
        new XC_MethodHook() {}
);
```

new XC_MethodHook()有两个重要的内部函数beforeHookedMethod()和afterHookedMethod()，

通过重写它们可以实现对任意方法的挂钩，它们的区别在于Hook前调用还是后调用

```
beforeHookedMethod 该方法在hook目标方法执行前调用，
其中，参数param指的是目标方法的相关参数、回调、方法等信息

afterHookedMethod 该方法在hook目标方法执行后调用，
其中，参数param指的是目标方法的相关参数、回调、方法等信息。

Xposed运行多个模块对同一个方法进行hook时，
框架就会根据Xposed模块的优先级来排序
```









##  修改函数的参数和返回值





```java
package com.example.x01;



import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;


public class MainHook implements IXposedHookLoadPackage {

    static  String strTag="echo_Xposed";
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable {

        Class StudentClass = loadPackageParam.classLoader.loadClass("com.example.helloworld.test.Student");

        XposedHelpers.findAndHookMethod(
                StudentClass,
                "getinfo",//函数名字
                String.class,//参数列表

                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);

                        //修改参数
                        Object[] objectArray = param.args;
                        objectArray[0] = "{XXXX:";
                    }

                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        super.afterHookedMethod(param);

                        //设置返回值
                        param.setResult(param.getResult()+":YYYY}");
                    }
                }
        );
    }

}

```



这个参数 Object[] objectArray = param.args; 有点意思





## 替换函数



```java
//hook私有函数 sg.vantagepoint.uncrackable1.MainActivity.a
XposedHelpers.findAndHookMethod(
        "sg.vantagepoint.uncrackable1.MainActivity",
        loadPackageParam.classLoader,
        "a",
        String.class,
        new XC_MethodReplacement() {
            @Override
            protected Object replaceHookedMethod(MethodHookParam methodHookParam) throws Throwable {
                // 直接替换原来要执行的逻辑代码,目标方法就不在执行了
                try {
	            			// 直接替换原来要执行的逻辑代码,目标方法就不在执行了
			    } catch (Throwable t) {
                    XposedBridge.log(t);
			    }  
                return null;
            }
        }
);
```





# 调用函数

```
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





```java
package com.example.x01;

import android.util.Log;

import java.lang.reflect.Method;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;


public class MainHook implements IXposedHookLoadPackage {

    static  String strTag="echo_Xposed";
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable {
        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",//这个是具体的class类的路径
                loadPackageParam.classLoader,
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(strTag, "无参构造 hook success!");


                        //反射调用函数
                        Method SetSchoolIDAndGetNameMethod = param.thisObject.getClass().getDeclaredMethod(
                                "getinfo",
                                String.class
                        );
                        SetSchoolIDAndGetNameMethod.setAccessible(true);

                        String result=(String) SetSchoolIDAndGetNameMethod.invoke(param.thisObject, "{XXXX: ");
                        Log.i(strTag, result+":YYYY}");
                    }
                }
        );

        XposedHelpers.findAndHookConstructor(
                "com.example.helloworld.test.Student",
                loadPackageParam.classLoader,
                String.class,
                int.class,
                new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(strTag, "有参构造 hook success!");


                        String result=(String)  XposedHelpers.callMethod(param.thisObject, "getinfo", "{XXXX: ");
                        Log.i(strTag, result+":YYYY}");
                    }
                }
        );
    }


}

```



# so hook



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



# XposedBridge

XposedBridge类中hookAllMethods和log方法主要用于一次hook每个类的所有方法或够造函数

```
hookAllMethods(
	Class hookClass,//需要进行hook的类
	String methodName,//需要进行hook的方法名
	XC_MethodHook callback//回调函数
)
```



# Hook函数



## 复杂的函数



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



## 内部类中的函数



**注：hook内部类中的函数和变量，跟以上的hook方式没有区别，唯一的区别是，XposedHelpers.findClass中的路径名不同。**



```java
public class HookDemo {
    private String Tag = "HookDemo";
    class InnerClass{
        public int innerPublicInt = 10;
        private int innerPrivateInt = 20;
        public InnerClass(){
        
        }
        public void InnerFunc(String value){
        
        }
    }
}

-------------------------------------------------------------------
final Class<?> clazz1 = XposedHelpers.findClass("com.xxxxxx.HookDemo$InnerClass", loadPackageParam.classLoader);
XposedHelpers.findAndHookMethod(
    clazz1, 
    "InnerMethod", 
    String.class, 
    new XC_MethodHook() {
        @Override
        protected void beforeHookedMethod(MethodHookParam param) throws Throwable {

        }
     });
```









# 附录





## demo





```java
public class XposedInit implements IXposedHookLoadPackage {
@Override
public void handleLoadPackage(final XC_LoadPackage.LoadPackageParam lpparam) {
    if (lpparam.packageName.equals("com.wrbug.xposeddemo")) {
        XposedHelpers.findAndHookMethod("com.wrbug.xposeddemo.MainActivity", lpparam.classLoader, "onCreate", Bundle.class, new XC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                //不能通过Class.forName()来获取Class ，在跨应用时会失效
                Class c=lpparam.classLoader.loadClass("com.wrbug.xposeddemo.MainActivity");
                Field field=c.getDeclaredField("textView");
                field.setAccessible(true);
                //param.thisObject 为执行该方法的对象，在这里指MainActivity
                TextView textView= (TextView) field.get(param.thisObject);//这里比较有意思
                textView.setText("Hello Xposed");
            }
        });
    }
}
```

