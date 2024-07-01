

# Reference Documents

https://juejin.cn/post/7308240524964134924

https://blog.csdn.net/weixin_38819889/article/details/119845994



未看

https://xz.aliyun.com/t/12088?time__1311=GqGxR70Qit0%3DqGN4eeTwUDn7AIrMx0I3x

http://www.shibaking.com/blog/2023-03-20-frida-hook-native%E5%B1%82%E6%96%B9%E6%B3%95.html

https://kevinspider.github.io/frida/frida-hook-so/

https://bbs.kanxue.com/thread-280812.htm

https://bbs.kanxue.com/thread-274838.htm#msg_header_h2_1



吴瑞 share

https://m.sohu.com/a/439633861_120054144

https://www.jianshu.com/p/59d1d3054abe



# method operate





## find method



```
way1), 

Module.findExportByName('libc.so', 'printf'), 



way2),

var sobase=Module.findBaseAddress('libfoo.so');
var tarFunc = sobase.add(0x10E0);
```







## listen method



```js
function()
{
    //不需要java.perform也可以作用
    
    Interceptor.attach(
        Module.findExportByName('libc.so', 'printf'), 
        {
            onEnter: function (args) //函数进入开始
            {
                //args[0], args[1],... 
                console.log('printf() called with format string: ' + Memory.readUtf8String(args[0]));
            },
            onLeave: function (retval) //函数离开结束的时候
            {
                console.log('printf() returned: ' + retval.toInt32());
            }
		}
    );
}
```





## replace method



```js
function(){

    Java.perform(
        function () 
        {
            var pthread_create = Module.findExportByName('libc.so', 'pthread_create');

            var pthread_create_signature = new NativeFunction(
                pthread_create, 
                'int', 
                ['pointer', 'pointer', 'pointer', 'pointer']);

            Interceptor.replace(
                pthread_create, 
                new NativeCallback(
                    function (thread, attr, start_routine, arg) 
                    {
                        if ((start_routine.toInt32()& 0xfff) == 0x0d0) 
                        {
                            // 如果第四个参数是 0x20,直接返回0
                            return 0;
                        } else 
                        {
                            // 否则调用原始的 pthread_create 函数
                            return pthread_create_signature(thread, attr, start_routine, arg);
                        }
                    }, 
                    'int', 
                    ['pointer', 'pointer', 'pointer', 'pointer']));
    	});
}
```







# 主动调用

3.frida主动调用so中的方法。
对so方法的直接调用需要用到frida的NativeFunction方法，方法原型如下：
NativeFunction(address, returnType, argTypes[, abi])
1）address：要hook的方法地址
2）returnType：返回值类型
3）argTypes[, abi]: 参数类型 这里参数可以是多个



```js
function Hook9(){
	Java.perform(
        function()
        {
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





# 信息遍历|获取



```js
//Get base address of library
var libfoo = Module.findBaseAddress("libfoo.so");

//Calculate address of variable
var initialized = libfoo.add(ptr("0x400C"));
```







枚举: var imports = Module.enumerateImportsSync("libfoo.so");

```js
// 枚举 libfoo.so 中的导入
var imports = Module.enumerateImportsSync("libfoo.so");

// 查找并打印导入的函数
for (var i = 0; i < imports.length; i++) {
    console.log("Import: " + imports[i].name + " at " + imports[i].address);
}
```



# 数据处理



```js
var str1=args[0].readCString();

this.arg1.writeUtf8String("fake_status_path")
```

