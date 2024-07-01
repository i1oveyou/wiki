# Reference Documents

https://juejin.cn/post/7308240524964134924

https://blog.csdn.net/weixin_38819889/article/details/119845994



# 函数重载



案例1

```js
function Hook2(){
	Java.perform(function(){
        console.log("Frida Test Hook2");
		var cls = Java.use("cn.gemini.k.fridatest.FridaHook1");

		// 重载方法hook
		cls.func2_add_overload.overload('int', 'int').implementation = function(arg1,arg2){
        console.log("func2_add_overload --> hook arg1:",arg1," hook arg2:",arg2);
		    arg1 = arg1 + 1;
		    arg2 = arg2 + 1;
		    var ret = this.func2_add_overload(arg1,arg2);
            return ret + 3;
        }
		
		cls.func2_add_overload.overload('int', 'int', 'int').implementation = function(arg1,arg2,arg3){
            console.log("func2_add_overload --> hook arg1:",arg1," hook arg2:",arg2," hook arg3:",arg3);
    	    arg1 = arg1 + 1;
		    arg2 = arg2 + 1;
		    arg3 = arg3 + 1;
	        var ret = this.func2_add_overload(arg1,arg2,arg3);
            return ret + 3;
        }
	});
}

```

案例2

```js
console.log(cls.func2_add_overload.overloads.length);
for(var i = 0; i < cls.func2_add_overload.overloads.length; i++){
	cls.func2_add_overload.overloads[i].implementation = function(){
		if(arguments.length == 2){
			var arg1 = arguments[0] + 1;
			var arg2 = arguments[1] + 1;
			console.log("func2_add_overload --> hook arg1:",arg1," hook arg2:",arg2);
			return this.func2_add_overload.apply(this,arguments) + 3;
		}else if(arguments.length == 3){
			var arg1 = arguments[0] + 1;
			var arg2 = arguments[1] + 1;
			var arg3 = arguments[2] + 1;
			console.log("func2_add_overload --> hook arg1:",arg1," hook arg2:",arg2," hook arg3:",arg3);
			return this.func2_add_overload.apply(this,arguments) + 3;
		}
	}
}

```



## hook类中所有成员方法



```js
function hookMain(){
	Java.perform(function(){
		console.log("[dqx] hello frida");
		var Student = Java.use("com.example.helloworld.test.Student");
		// 先枚举类的所有方法
		var methods = Student.class.getDeclaredMethods();
		for(var i = 0; i < methods.length; i++){
			var methodName = methods[i].getName();	// 获取到每个方法的名字
			console.log(methodName);
			console.log(Student[methodName].overloads.length);

			// 重载方法的处理
			for(var j = 0; j < Student[methodName].overloads.length; j++){
				Student[methodName].overloads[j].implementation = function(){
					for(var k = 0;k < arguments.length; k++){
						console.log(this + " arg"+ k + ":" + arguments[k]);
					}
					return this[methodName].apply(this, arguments);
				}
			}
		}
	});
}
setImmediate(hookMain)
```









# 构造方法

有点不一样

```js
function Hook3(){
	Java.perform(function(){
        console.log("Frida Test Hook3");
		var cls = Java.use("cn.gemini.k.fridatest.FridaHook1");

		cls.$init.implementation = function(){
			console.log("$init --> hook");
			//this.$init();
		}
	});
}

```



# hook静态方法

静态方法的hook实际上和一般方法的hook类似。

```js
function Hook4(){
	Java.perform(function(){
        console.log("Frida Test Hook4");
		var cls = Java.use("cn.gemini.k.fridatest.FridaHook1");

		cls.func3_verify_static.implementation = function(arg1){
			console.log("func3_verify_static --> hook arg1:",arg1);
			return this.func3_verify_static(arg1);
		}
	});
}
```





# 匿名类



```js
Java.perform(
    function(){
        console.log("[*] Hook begin")
        var mainActivity$1 = Java.use("sg.vantagepoint.uncrackable1.MainActivity$1");
        mainActivity$1.onClick.implementation = function(){
            console.log("[*] Hook mainActivity$1.onClick")
        }
    }
)

```



# 内部类



```js
function Hook5(){
	Java.perform(function(){
        console.log("Frida Test Hook5");
		// hook内部类方法
		var innercls = Java.use("cn.gemini.k.fridatest.FridaHook1$inner_class");
		innercls.inner_class_func.implementation = function(arg1){
			console.log("inner_class_func arg1:",arg1);
			return this.inner_class_func(arg1);
		}
	});
}

```



# 修改字段

一个类的字段包括静态字段和非静态字段。

 静态字段的访问可以直接通过 类.字段名.value = “XXX” 的方式进行修改。

非静态字段则需要先拿到对象实例才能修改，获取对象实例可使用Java.choose()。

同时还需要注意非静态字段又分为有同名方法的字段和无同名方法的字段

对于有同名方法的字段，在访问时需要在字段名前面加一个下划线"_"才能访问。

对于无同名方法的字段，则直接可以访问

对象实例化则通过$new方法即可创建一个新的对象。



```js
function Hook8(){
	Java.perform(function(){
		console.log("Frida Test Hook8");
		var clazz = Java.use("cn.gemini.k.fridatest.FridaHook1");
		// 修改类中的静态字段
		console.log("修改前静态字段的值:" + clazz.password.value);
		clazz.password.value = "9"; // 静态字段的修改
		console.log("修改后静态字段的值:" + clazz.password.value);

		// 实例化类对象
		var newcls = clazz.$new();  // 通过$new方法对类进行实例化
		console.log("实例化一个类对象"+newcls)
		console.log("修改前的字段值: abc=="+newcls._abc.value+" cde=="+newcls.cde.value);

		// 修改类中的非静态字段
		Java.choose("cn.gemini.k.fridatest.FridaHook1",{
			onMatch: function(obj){
				obj.cde.value = 100;    // 非静态字段修改方式
				obj._abc.value = 200;   // 非静态字段修改:这里需要注意因为类中存在一个同名的方法,所以访问该字段时需要加个下划线"_"
				console.log("修改后的字段值: abc=="+obj._abc.value+" cde=="+obj.cde.value);
			},
			onComplete: function(){
			}
		});

	});
}
```







# 枚举所有类与类的所有方法



Java.enumerateLoadedClasses(callbacks)：无返回值，参数是一个回调方法，功能是列出当前已经加载的类，用回调方法处理。
回调方法：

- onMath:function(name){}
  找到加载的每个类的时候被调用，参数就是类的名字，可以将name传入Java.use()来获得一个js类，还可以通过name对枚举的类进行过滤

- onComplete:function(){}
  枚举完所有类之后被调用，用来做一些完成后的收尾工作

Java.enumerateLoadedClassesSync()：无参数，方法返回所有已经加载的类的数组。





```js
 
function hookMain(){
	Java.perform(function(){
		// 枚举所有类
		console.log("[dqx]: 枚举所有类");
		
		Java.enumerateLoadedClasses({
			onMatch: function(name){
				console.log(name);//好像是遍历当前设备的所有类,


				// 这里可以添加过滤逻辑用来过滤我们关注的类
				//if(name.indexOf("cn.gemini.k.fridatest") != -1){
				//	console.log(name);
				//}
			},
			onComplete: function(){
                console.log("[dqx]: 遍历完毕");
			}
		});

		// 打印类中的所有方法
		console.log("[dqx]: 打印类中的所有方法");
		var Student = Java.use("com.example.helloworld.test.Student");
		var methods = Student.class.getDeclaredMethods(); // 获取类中的所有方法可使用反射获得
		//console.log(methods);
        for (var i=0; i < methods.length; i++){
            console.log(methods[i])
          }
	});
}
setImmediate(hookMain)
```



# 主动函数调用

frida的方法主动调用，主要分以下几种情况
1.frida主动调用Java类中的静态方法，也就是使用static关键字声明的。
2.frida主动调用对象的Java成员方法，通过对象才能调用的方法，非static方法。

    方法一：创建一个新对象完成主动调用
    方法二：搜索内存中已有对象完成主动调用（推荐使用内存中原有的对象，因为内存中的对象才是应用真实的应用使用的对象，自己创建对象的数据可能与应用当时实际使用的数据不一致，一般协议分析会存在上面的情况（那么问题来了，如果内存中有多个对象该如何区分哪个是我们要的对象呢？），如果只是单纯使用对象方法的功能那么一般问题不大）

3.frida主动调用so中的方法。
对so方法的直接调用需要用到frida的NativeFunction方法，方法原型如下：
NativeFunction(address, returnType, argTypes[, abi])
1）address：要hook的方法地址
2）returnType：返回值类型
3）argTypes[, abi]: 参数类型 这里参数可以是多个



```js
function Hook9(){
	Java.perform(function(){
		console.log("Frida Test Hook9");
        
		// 主动调用类静态方法
		var clszz = Java.use("cn.gemini.k.fridatest.FridaHook1");
		clszz.func3_verify_static(">>>pwd<<<");

		// 主动调用类成员方法
		// 第一种方式：创建一个新对象完成主动调用
		var obj = clszz.$new();
		var ret = obj.func2_add_overload(11,22);
		console.log("返回值: " + ret);

		// 第二种方式：搜索内存中已有对象完成主动调用
		Java.choose("cn.gemini.k.fridatest.FridaHook1",{
			onMatch: function(instance){
                console.log("found instance :"+ instance);
                console.log("返回值: "+ instance.func2_add_overload(33,44));
			},
			onComplete: function(){
                console.log("Search Completed!");
			}
		})

		// 主动调用so的native方法
		var str_name_so = "libnative-lib.so";    //要hook的so名
		var str_name_func = "JNI_Frida_Test";    //要hook的方法名
		// 获取方法地址
		var addr_func = Module.findExportByName(str_name_so , str_name_func);
		console.log("func addr is ---" + addr_func);
		//定义NativeFunction 等下要调用
		var func_JNI_Frida_Test = new NativeFunction(addr_func,"void",[]);
		func_JNI_Frida_Test();
	});
}
```










# 其它



让原本函数什么也不做

```
function hookMain(){ 
    Java.perform(
        function(){
            console.log("[*] Hook begin")
            var mainActivity = Java.use("sg.vantagepoint.uncrackable1.MainActivity");
            mainActivity.a.implementation = function(){
                console.log("[*] Hook mainActivity.a")
                //不调用原始函数
                //hook后,什么也不做
            }

        }
    )
    
}
setImmediate(hookMain)

```



调用原本的函数,但是还是要执行以前的

这里修改了返回值

```
function hookMain(){ 
    Java.perform(
        function(){
            console.log("[*] Hook begin")
            var vantagePoint = Java.use("sg.vantagepoint.a.c") // 
            vantagePoint.a.implementation = function(){
                console.log("[*] Hook vantagepoint.a.c.a")
                this.a(); //执行原有的方法
                return false;
            }
            vantagePoint.b.implementation = function(){
                console.log("[*] Hook vantagepoint.a.c.b")
                this.b();
                return false;
            }
            vantagePoint.c.implementation = function(){
                console.log("[*] Hook vantagepoint.a.c.c")
                this.c();
                return false;
            }
        }
    )
    
}
setImmediate(hookMain)

```





貌似, function()不用设置参数

```
Java.perform(
    function(){
        console.log("[*] Hook begin")
        var javaSystem = Java.use("java.lang.System");
        javaSystem.exit.implementation = function(){
            console.log("[*] Hook system.exit")
        }
    }
)
```





```
Java.perform(
    function(){
        var cryptoAES = Java.use("sg.vantagepoint.a.a");
        cryptoAES.a.implementation = function(bArr, bArr2){
            console.log("[*] Hook cryptoAES")
            var secret = "";
            var decryptValue = this.a(bArr, bArr2);
            console.log("[*] DecryptValue:", decryptValue)
            for (var i=0; i < decryptValue.length; i++){
              secret += String.fromCharCode(decryptValue[i]);
            }
            console.log("[*] Secret:", secret)
            return decryptValue;
        }
    }
)

```






