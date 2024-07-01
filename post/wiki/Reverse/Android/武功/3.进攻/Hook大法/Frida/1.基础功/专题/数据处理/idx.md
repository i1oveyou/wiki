

# String



```js
String.fromCharCode(buffer[i]) ;把一个int转化为字符
```



```
arg0.indexOf('frida'); 判断arg0是否函数字符串"frida"


args[2].toInt32();  转化为int值
```





# Memory 内存操作



读取内存,写入内存

```js
//Write 1 to the variable
Memory.writeInt(initialized,1);

var arg0 = Memory.readUtf8String(args[0]);
```



# debug输出



so层的

```js
function jhexdump(array,off,len) {
    var ptr = Memory.alloc(array.length);
    for(var i = 0; i < array.length; ++i)
        Memory.writeS8(ptr.add(i), array[i]);
    //console.log(hexdump(ptr, { offset: off, length: len, header: false, ansi: false }));
    console.log(hexdump(ptr, { offset: 0, length: array.length, header: true, ansi: true }));
}
```



字符串输出, int转char

```js
var retVal = [72, 101, 108, 108, 111];
var secret = String.fromCharCode.apply(null, retVal);
console.log(secret); // 输出 "Hello"

 
var result = ""
for(var i = 0; i < buffer.length; ++i){
        result+= (String.fromCharCode(buffer[i]));
}
```

