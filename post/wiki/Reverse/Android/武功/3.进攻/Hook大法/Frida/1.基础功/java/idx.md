

# 找到类

```js
var var_tarClas = Java.use("clas的路径");
```

不管是 匿名类, 还是内部类

重点在于找到类的路径,那么就没什么难度了







# find method 

有的函数有重载,有的函数没有重载

eg: 

```js
function hello_frida(){
    Java.perform(
        function () 
        {
            let var_tarClas = Java.use("android.widget.TextView");
            var_tarClas.setText.overload('java.lang.CharSequence').implementation = function (text) 
            {
                var ret =this.setText(text);//原始函数调用, 也可以选择不去调用
                return ret;//返回值
            }
        }); 
}
Java.perform(function(){
    hello_frida();
})
```



构造函数

```js
function  hello_frida){
	Java.perform(
        function()
    	{
            var var_tarClas = Java.use("android.widget.TextView");

            var_tarClas.$init.implementation = function()
            {
                this.$init();
            }
        }
    );
}
```



静态函数

静态函数的hook和普通函数的hook 没什么特别的



# method call



frida的方法主动调用，主要分以下几种情况

1.frida主动调用Java类中的静态方法，也就是使用static关键字声明的。

2.frida主动调用对象的Java成员方法，通过对象才能调用的方法，非static方法。

方法一：创建一个新对象完成主动调用

方法二：搜索内存中已有对象完成主动调用



 



```js
function Hook9(){
	Java.perform(
        function()
        {
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
	});
}
```







# change field



一个类的字段包括静态字段和非静态字段。

静态字段的访问可以直接通过 类.字段名.value = “XXX” 的方式进行修改。

非静态字段则需要先拿到对象实例才能修改，获取对象实例可使用Java.choose()。

对象实例化则通过$new方法即可创建一个新的对象。



同时还需要注意非静态字段又分为有同名方法的字段和无同名方法的字段

对于有同名方法的字段，在访问时需要在字段名前面加一个下划线`"_"`才能访问。

对于无同名方法的字段，则直接可以访问





```js
function Hook8(){
	Java.perform(
        function()
        {
            console.log("Frida Test Hook8");
            var clazz = Java.use("cn.gemini.k.fridatest.FridaHook1");
            // 修改类中的静态字段
            clazz.password.value = "9"; // 静态字段的修改


            // 实例化类对象
            var newcls = clazz.$new();  // 通过$new方法对类进行实例化

            // 修改类中的非静态字段
            Java.choose(
                "cn.gemini.k.fridatest.FridaHook1",
                {
                    onMatch: function(obj)
                    {
                        obj.cde.value = 100;   
                        obj._abc.value = 200;   
                    },
                    onComplete: function()
                    {

                    }
                });
		});
}
```

