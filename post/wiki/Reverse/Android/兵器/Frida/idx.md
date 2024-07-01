



# 说明文档

https://frida.re/docs/home/



# 下载+安装



去官方下载  frida-server-android-arm64  https://github.com/frida/frida

直接去release列表可能找不到, 需要点击asset下拉列表,因为它release发布的文件有很多很多, Android只是一下部分

eg: 比如下载得到frida-server-16.3.3-android-arm64, 然后adb push到 /data/local/tmp/

push到手机后,可以重命名一下文件` frida-server-16.3.3-android-arm64  ---> frida-server`



本机环境安装: 

```
pip install frida       # Python bindings
pip install frida-tools # CLI tools

# 呃,说新版本不稳定,于是下载稳定的版本, 运行某个js代码却发现frida崩溃
# 为什么版本会更新,为什么会崩溃,各有他的道理
# 最后我选择下载最新版

#  Android10.0环境
pip install frida==14.2.9
pip install frida-tools==9.2.5
frida-server:  https://github.com/frida/frida/releases/tag/14.2.9 
```



所以我当前的环境是

```
C:\mm_djx\code
λ frida --version
16.3.3
```





# 开发环境vscode+frida

写frida毕竟是写js, 涉及一些包的语法提示还是很重要的

环境:

kali vscode

安装node (不知道为什么要安装node)



安装npm

```
npm  i -g @types/frida-gum
```

要有语法展示的话, 写代码时需要在头部导入, 

```
import 'frida-gum' 
//..hook code
```

但是这样会导致我js代码运行失败,语法错误. 所以酌情考虑

ps: 写代码时,前期自我感觉多数在cv, 没在思考用什么api



关于其它的下载,不知道有没有用

```
npm install @types/node 
npm install frida-compile
```







# hook模式

frida hook有两种模式，如下

attach 模式:  Hook 已经存在的进程，

spawn 模式: 重启一个进程,在开始的时候进行hook



shell 启动frida的指令

```bash
frida -U -f "package包名" -l asset\f1.js  #spawn模式
frida -U -f "re.pwnme" -l asset\f1.js --pause  #spawn模式,但启动时暂停下, 等待我们输入指令再run
 
frida -U -n "进程名" -l asset\f2.js  #attach模式,进程名可用frida-ps -Ua查看
frida -U -n "Uncrackable Level 2" -l asset\f2.js  #attach 
```



# Hello Frida



启动

```
C:\mm_djx\code
λ adb shell
PBCM10:/ $ su
PBCM10:/ # /data/local/tmp/frida/frida-server
```



端口转发

```
C:\mm_djx\code
λ adb forward tcp:27042 tcp:27042
27042

C:\mm_djx\code
λ adb forward tcp:27043 tcp:27043
27043
```



准备一个简单的apk: 显示helo android

![image-20240630170357231](./img/image-20240630170357231.png)

我们尝试把它的文本内容给hook掉

hook.js如下

```js
function hello_frida(){
    Java.perform(
        function () 
        {
            let tmp_TextView = Java.use("android.widget.TextView");
            tmp_TextView.setText.overload('java.lang.CharSequence').implementation = function (args) 
            {

                var String = Java.use("java.lang.String");
                var text = String.$new("you are hooked"); // 创建一个CharSequence对象

                console.log("org text :",args)
                console.log("new text :",text)

                return this.setText(text);
        
            }
        }); 
}
Java.perform(function(){
    hello_frida();
})
```



然后运行它

```
C:\mm_djx\code\src\frida
λ frida -U -f com.example.helloworld -l asset\f4.js
     ____
    / _  |   Frida 16.3.3 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://frida.re/docs/home/
   . . . .
   . . . .   Connected to PBCM10 (id=1d518c72)
Spawned `com.example.helloworld`. Resuming main thread!
[PBCM10::com.example.helloworld ]-> org text : test for debug
new text : you are hooked
```



![image-20240630172955774](./img/image-20240630172955774.png)



# 指令

```
frida-ps -U #列出usb所连设备的所有进程
frida-ps -Uai  	# 列出安装的程序
frida-ps -Ua	# 列出正在运行中的程序
```



```
C:\mm_djx\code
λ frida --help
usage: frida [options] target

positional arguments:
  args                  extra arguments and/or target

optional arguments:
  -h, --help            show this help message and exit
  -D ID, --device ID    connect to device with the given ID
  -U, --usb             connect to USB device
  -R, --remote          connect to remote frida-server
  -H HOST, --host HOST  connect to remote frida-server on HOST
  --certificate CERTIFICATE
                        speak TLS with HOST, expecting CERTIFICATE
  --origin ORIGIN       connect to remote server with “Origin” header set to ORIGIN
  --token TOKEN         authenticate with HOST using TOKEN
  --keepalive-interval INTERVAL
                        set keepalive interval in seconds, or 0 to disable (defaults to -1 to auto-select based on
                        transport)
  --p2p                 establish a peer-to-peer connection with target
  --stun-server ADDRESS
                        set STUN server ADDRESS to use with --p2p
  --relay address,username,password,turn-{udp,tcp,tls}
                        add relay to use with --p2p
  -f TARGET, --file TARGET
                        spawn FILE
  -F, --attach-frontmost
                        attach to frontmost application
  -n NAME, --attach-name NAME
                        attach to NAME
  -N IDENTIFIER, --attach-identifier IDENTIFIER
                        attach to IDENTIFIER
  -p PID, --attach-pid PID
                        attach to PID
  -W PATTERN, --await PATTERN
                        await spawn matching PATTERN
  --stdio {inherit,pipe}
                        stdio behavior when spawning (defaults to “inherit”)
  --aux option          set aux option when spawning, such as “uid=(int)42” (supported types are: string, bool, int)
  --realm {native,emulated}
                        realm to attach in
  --runtime {qjs,v8}    script runtime to use
  --debug               enable the Node.js compatible script debugger
  --squelch-crash       if enabled, will not dump crash report to console
  -O FILE, --options-file FILE
                        text file containing additional command line options
  --version             show program's version number and exit
  -l SCRIPT, --load SCRIPT
                        load SCRIPT
  -P PARAMETERS_JSON, --parameters PARAMETERS_JSON
                        parameters as JSON, same as Gadget
  -C USER_CMODULE, --cmodule USER_CMODULE
                        load CMODULE
  --toolchain {any,internal,external}
                        CModule toolchain to use when compiling from source code
  -c CODESHARE_URI, --codeshare CODESHARE_URI
                        load CODESHARE_URI
  -e CODE, --eval CODE  evaluate CODE
  -q                    quiet mode (no prompt) and quit after -l and -e
  -t TIMEOUT, --timeout TIMEOUT
                        seconds to wait before terminating in quiet mode
  --pause               leave main thread paused after spawning program
  -o LOGFILE, --output LOGFILE
                        output to log file
  --eternalize          eternalize the script before exit
  --exit-on-error       exit with code 1 after encountering any exception in the SCRIPT
  --kill-on-exit        kill the spawned program when Frida exits
  --auto-perform        wrap entered code with Java.perform
  --auto-reload         Enable auto reload of provided scripts and c module (on by default, will be required in the
                        future)
  --no-auto-reload      Disable auto reload of provided scripts and c module
```













# 莫名其妙报错

https://blog.csdn.net/m0_54352040/article/details/115734161

报错如下

```
PBCM10:/data/local/tmp/frida # ./frida-server 
{"type":"error","description":"Error: invalid address","stack":"Error: invalid address\n    at Object.value [as patchC
ode] (frida/runtime/core.js:170:1)\n    at Jt (frida/node_modules/frida-java-bridge/lib/android.js:945:1)\n    at zt.a
ctivate (frida/node_modules/frida-java-bridge/lib/android.js:998:1)\n    at Ut.replace (frida/node_modules/frida-java-
bridge/lib/android.js:1045:1)\n    at Function.set [as implementation] (frida/node_modules/frida-java-bridge/lib/class
-factory.js:1010:1)\n    at Function.set [as implementation] (frida/node_modules/frida-java-bridge/lib/class-factory.j
s:925:1)\n    at installLaunchTimeoutRemovalInstrumentation (/internal-agent.js:249:24)\n    at init (/internal-agent.
js:33:3)\n    at c.perform (frida/node_modules/frida-java-bridge/lib/vm.js:11:1)\n    at g._performPendingVmOps (frida
/node_modules/frida-java-bridge/index.js:238:1)","fileName":"frida/runtime/core.js","lineNumber":170,"columnNumber":1}
^CPBCM10:/data/local/tmp/frida # adb shell setenforce 0
/system/bin/sh: adb: inaccessible or not found
```

解决办法 https://github.com/frida/frida/issues/1768

turning off SELinux solved the problem

```
adb shell setenforce 0
# setenforce 0
```









# 附录



## py脚本使用



```python
# -*- coding: UTF-8 -*-
import frida,sys

# 目标包名
appPacknName = "cn.gemini.k.fridatest"
scriptFile = "hook_script.js"

# 输出日志的回调方法
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

device = frida.get_usb_device()
# spawn模式,找到目标包名并重启,在启动前注入脚本
pid = device.spawn([appPacknName])
session = device.attach(pid)
# 注意这里需要将device.attach(pid)这句代码写在前面,这样执行才符合预期(启动时程序白屏,等待下面这行代码来恢复执行)
# 其实在https://www.jianshu.com/p/b833fba1bffe这篇文章中有提到
device.resume(pid)

# 方式一: 通过js文件创建hook代码
with open(scriptFile, encoding='UTF-8') as f :
    script = session.create_script(f.read())
# 方式二: 直接将hook代码写在python文件中
# script = session.create_script(js_code)

script.on("message", on_message)
script.load()   #把js代码注入到目标应用中
# 避免结束
sys.stdin.read()

```



## frida-tools和frida 版本对应

```
frida-tools==1.0.0 ------ 12.0.0<=frida<13.0.0
frida-tools==1.1.0 ------ 12.0.0<=frida<13.0.0
frida-tools==1.2.0 ------ 12.1.0<=frida<13.0.0
frida-tools==1.2.1 ------ 12.1.0<=frida<13.0.0
frida-tools==1.2.2 ------ 12.1.0<=frida<13.0.0
frida-tools==1.2.3 ------ 12.1.0<=frida<13.0.0
frida-tools==1.3.0 ------ 12.3.0<=frida<13.0.0
frida-tools==1.3.1 ------ 12.3.0<=frida<13.0.0
frida-tools==1.3.2 ------ 12.4.0<=frida<13.0.0
frida-tools==2.0.0 ------ 12.5.3<=frida<13.0.0
frida-tools==2.0.1 ------ 12.5.9<=frida<13.0.0
frida-tools==2.0.2 ------ 12.5.9<=frida<13.0.0
frida-tools==2.1.0 ------ 12.5.9<=frida<13.0.0
frida-tools==2.1.1 ------ 12.5.9<=frida<13.0.0
frida-tools==2.2.0 ------ 12.5.9<=frida<13.0.0
frida-tools==3.0.0 ------ 12.6.17<=frida<13.0.0
frida-tools==3.0.1 ------ 12.6.17<=frida<13.0.0
frida-tools==4.0.0 ------ 12.6.21<=frida<13.0.0
frida-tools==4.0.1 ------ 12.6.21<=frida<13.0.0
frida-tools==4.0.2 ------ 12.6.21<=frida<13.0.0
frida-tools==4.1.0 ------ 12.6.21<=frida<13.0.0
frida-tools==5.0.0 ------ 12.6.21<=frida<13.0.0
frida-tools==5.0.1 ------ 12.7.3<=frida<13.0.0
frida-tools==5.1.0 ------ 12.7.3<=frida<13.0.0
frida-tools==5.2.0 ------ 12.7.3<=frida<13.0.0
frida-tools==5.3.0 ------ 12.7.3<=frida<13.0.0
frida-tools==5.4.0 ------ 12.7.3<=frida<13.0.0
frida-tools==6.0.0 ------ 12.8.5<=frida<13.0.0
frida-tools==6.0.1 ------ 12.8.5<=frida<13.0.0
frida-tools==7.0.0 ------ 12.8.12<=frida<13.0.0
frida-tools==7.0.1 ------ 12.8.12<=frida<13.0.0
frida-tools==7.0.2 ------ 12.8.12<=frida<13.0.0
frida-tools==7.1.0 ------ 12.8.12<=frida<13.0.0
frida-tools==7.2.0 ------ 12.8.12<=frida<13.0.0
frida-tools==7.2.1 ------ 12.8.12<=frida<13.0.0
frida-tools==7.2.2 ------ 12.8.12<=frida<13.0.0
frida-tools==8.0.0 ------ 12.10.4<=frida<13.0.0
frida-tools==8.0.1 ------ 12.10.4<=frida<13.0.0
frida-tools==8.1.0 ------ 12.10.4<=frida<13.0.0
frida-tools==8.1.1 ------ 12.10.4<=frida<13.0.0
frida-tools==8.1.2 ------ 12.10.4<=frida<13.0.0
frida-tools==8.1.3 ------ 12.10.4<=frida<13.0.0
frida-tools==8.2.0 ------ 12.10.4<=frida<13.0.0
frida-tools==9.0.0 ------ 14.0.0<=frida<15.0.0
frida-tools==9.0.1 ------ 14.0.0<=frida<15.0.0
frida-tools==9.1.0 ------ 14.2.0<=frida<15.0.0
frida-tools==9.2.0 ------ 14.2.9<=frida<15.0.0
frida-tools==9.2.1 ------ 14.2.9<=frida<15.0.0
frida-tools==9.2.2 ------ 14.2.9<=frida<15.0.0
frida-tools==9.2.3 ------ 14.2.9<=frida<15.0.0
frida-tools==9.2.4 ------ 14.2.9<=frida<15.0.0
frida-tools==9.2.5 ------ 14.2.9<=frida<15.0.0
frida-tools==10.0.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.1.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.1.1 ------ 15.0.0<=frida<16.0.0
frida-tools==10.2.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.2.1 ------ 15.0.0<=frida<16.0.0
frida-tools==10.2.2 ------ 15.0.0<=frida<16.0.0
frida-tools==10.3.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.4.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.4.1 ------ 15.0.0<=frida<16.0.0
frida-tools==10.5.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.5.1 ------ 15.0.0<=frida<16.0.0
frida-tools==10.5.2 ------ 15.0.0<=frida<16.0.0
frida-tools==10.5.3 ------ 15.0.0<=frida<16.0.0
frida-tools==10.5.4 ------ 15.0.0<=frida<16.0.0
frida-tools==10.6.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.6.1 ------ 15.0.0<=frida<16.0.0
frida-tools==10.6.2 ------ 15.0.0<=frida<16.0.0
frida-tools==10.7.0 ------ 15.0.0<=frida<16.0.0
frida-tools==10.8.0 ------ 15.0.0<=frida<16.0.0
frida-tools==11.0.0 ------ 15.2.0<=frida<16.0.0
frida-tools==12.0.0 ------ 16.0.0<=frida<17.0.0
frida-tools==12.0.1 ------ 16.0.0<=frida<17.0.0
frida-tools==12.0.2 ------ 16.0.0<=frida<17.0.0
frida-tools==12.0.3 ------ 16.0.0<=frida<17.0.0
frida-tools==12.0.4 ------ 16.0.0<=frida<17.0.0
frida-tools==12.1.0 ------ 16.0.0<=frida<17.0.0
frida-tools==12.1.1 ------ 16.0.9<=frida<17.0.0
frida-tools==12.1.2 ------ 16.0.9<=frida<17.0.0
frida-tools==12.1.3 ------ 16.0.9<=frida<17.0.0
frida-tools==12.2.0 ------ 16.0.9<=frida<17.0.0
frida-tools==12.2.1 ------ 16.0.9<=frida<17.0.0
frida-tools==12.3.0 ------ 16.0.9<=frida<17.0.0
```



