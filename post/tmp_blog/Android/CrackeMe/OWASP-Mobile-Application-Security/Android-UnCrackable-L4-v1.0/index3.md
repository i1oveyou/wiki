

查看导入表的一些信息

```
[0x000052b0]> ii
[Imports]
nth vaddr      bind   type lib name
―――――――――――――――――――――――――――――――――――
5   0x00005130 GLOBAL FUNC     mprotect
13  0x00005140 GLOBAL FUNC     pthread_create
18  0x00005150 GLOBAL FUNC     isdigit
27  0x00005160 GLOBAL FUNC     open
31  0x00005170 GLOBAL FUNC     printf
39  0x00005180 GLOBAL FUNC     __cxa_finalize
58  0x00005190 GLOBAL FUNC     calloc
75  ---------- GLOBAL OBJ      __progname
78  0x000051a0 GLOBAL FUNC     closedir
100 0x000051b0 GLOBAL FUNC     snprintf
106 0x000051c0 GLOBAL FUNC     sscanf
121 0x000051d0 GLOBAL FUNC     gmtime_r
123 0x000051e0 GLOBAL FUNC     rand
144 0x000051f0 GLOBAL FUNC     __stack_chk_fail
166 0x00005200 GLOBAL FUNC     nanosleep
172 0x00005210 GLOBAL FUNC     opendir
193 0x00005220 GLOBAL FUNC     strcmp
222 0x00005230 GLOBAL FUNC     readdir
242 0x00005240 GLOBAL FUNC     malloc
245 0x00005250 GLOBAL FUNC     memcpy
250 0x00005260 GLOBAL FUNC     memset
262 0x00005270 GLOBAL FUNC     free
263 0x00005280 GLOBAL FUNC     __system_property_get
268 0x00005290 GLOBAL FUNC     __cxa_atexit
269 0x000052a0 GLOBAL FUNC     isspace
```



监视一下open 和sprintf

```
function hook_C_open(){
    var open_address = Module.findExportByName("libc.so","open")
    Interceptor.attach(open_address,{
        onEnter:function(args){
            this.open_args = args[0]
            console.log("[+] Open ==> "+ this.open_args.readCString())
        }
    })
}

function hook_C_snprintf(){
    var snprintf_address = Module.findExportByName("libc.so","snprintf")
    Interceptor.attach(snprintf_address,{
        onEnter: function(args){
            this.snprintf_args = args[0]
        },
        onLeave: function(retval){
            console.log("[+] Snprintf(arg0,) ==>: "+ this.snprintf_args.readCString())
        }
    })
}

Java.perform(function(){
    hook_C_open();
    hook_C_snprintf();
})
```



第一次运行如下

```
λ frida -U -f re.pwnme -l asset\f1.js
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
Spawned `re.pwnme`. Resuming main thread!
[PBCM10::re.pwnme ]-> [+] Open ==> /proc/self/cmdline
[+] Open ==> /data/app/re.pwnme-zTbqjxGxX-j6lOJvkpbGsg==/base.apk
[+] Snprintf(arg0,) ==>: 50000
[+] Open ==> /proc/27445/timerslack_ns
[+] Open ==> /data/vendor/gpu/esx_config_re.pwnme.txt
[+] Open ==> /data/vendor/gpu/esx_config.txt
[+] Open ==> /data/misc/gpu/esx_config_re.pwnme.txt
[+] Open ==> /data/misc/gpu/esx_config.txt
[+] Open ==> /data/app/re.pwnme-zTbqjxGxX-j6lOJvkpbGsg==/lib/arm64/libnative-lib.so
[+] Open ==> /data/local/su
[+] Open ==> /data/local/bin/su
[+] Open ==> /data/local/xbin/su
[+] Open ==> /sbin/su
[+] Snprintf(arg0,) ==>: /proc/self/task/27410/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27420/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27421/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27422/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27423/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27424/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27425/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27426/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27428/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27429/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27430/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27431/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27432/status
[+] Open ==> /proc/cpuinfo
Process crashed: Bad access due to invalid address

***
Process name is com.android.chrome:sandboxed_process0, not key_process
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'OPPO/PBCM10/PBCM10:10/QKQ1.191224.003/1615196842:user/release-keys'
Revision: '0'
ABI: 'arm64'
Timestamp: 2024-06-28 16:51:40+0800
pid: 27410, tid: 27449, name: re.pwnme  >>> com.android.chrome:sandboxed_process0 <<<
uid: 10246
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xfabb11cd
    x0  0000007dfe6fe710  x1  000000008a3bda98  x2  0000000000000000  x3  0000000000000000
    x4  00000000ffffffff  x5  0000000000000000  x6  0000007dfe6fed50  x7  0000000000ffd888
    x8  00000000000067c8  x9  00000000fabb11cd  x10 0000000085b34305  x11 0000000000000001
    x12 000000000739dade  x13 00000000fffffff6  x14 000000000739dade  x15 0000000000000000
    x16 0000000000000001  x17 0000007eef9f240c  x18 0000007dfd4c4000  x19 0000007dfe6fe710
    x20 0000007ef135f6fc  x21 0000007dfe6fed50  x22 0000007dfe6ff060  x23 0000007dfe6fedd8
    x24 0000007dfe6fed50  x25 0000007dfe6fed50  x26 0000007dfe6ff020  x27 0000007ef465d020
    x28 0000007dfeb244dc  x29 0000007dfe6fecf0
    sp  0000007dfe6fe710  lr  0000007eef9f240c  pc  0000007dfeb556cc

backtrace:
      #00 pc 000000000007b6cc  /data/app/re.pwnme-zTbqjxGxX-j6lOJvkpbGsg==/lib/arm64/libnative-lib.so (BuildId: f87b3bd9fcae36e63939958f412d03a42e0ce406)
      #01 pc 00000000000d9720  /apex/com.android.runtime/lib64/bionic/libc.so!libc.so (offset 0xd9000) (__pthread_start(void*)+36) (BuildId: 20c7dfeb41468016772e288818fb55e7)
      #02 pc 0000000000075f2c  /apex/com.android.runtime/lib64/bionic/libc.so!libc.so (offset 0x75000) (__start_thread+64) (BuildId: 20c7dfeb41468016772e288818fb55e7)
***
[PBCM10::re.pwnme ]->

Thank you for using Frida!
```



观察一下这个, apk放问了当前进程的子进程, 一个正常的apk应该不会去访问. 

```
[+] Snprintf(arg0,) ==>: /proc/self/task/27410/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27420/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27421/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27422/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27423/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27424/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27425/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27426/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27428/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27429/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27430/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27431/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27432/status
```

估计是在做检测..通过结果,发现最后停在了27432子进程



我们尝试再运行一下

```
λ frida -U -f re.pwnme -l asset\f1.js --pause
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
Spawned `re.pwnme`. Use %resume to let the main thread start executing!

[PBCM10::re.pwnme ]-> %resume
```

然后查看apk进程的一些信息

```
PBCM10:/ $ ps -A | grep "re.pwnme"
u0_a246      27678  1805 5744660  37140 0                   0 S re.pwnme
```

所以, 当前进程是PID=27678

然后查看 `/proc/27678/task`, 关注一下 `Name:   gmain Pid:    27700`  这个子进程好像是frida的

```
PBCM10:/ $ cd /proc/27678/task
PBCM10:/proc/27678/task $ cat ./*/status | awk "/(Name:)|(^Pid:)/"
Name:   re.pwnme
Pid:    27678
Name:   Jit thread pool
Pid:    27688
Name:   Runtime worker
Pid:    27689
Name:   Runtime worker
Pid:    27690
Name:   Runtime worker
Pid:    27691
Name:   Runtime worker
Pid:    27692
Name:   Signal Catcher
Pid:    27693
Name:   ADB-JDWP Connec
Pid:    27694
Name:   HeapTaskDaemon
Pid:    27696
Name:   ReferenceQueueD
Pid:    27697
Name:   FinalizerDaemon
Pid:    27698
Name:   FinalizerWatchd
Pid:    27699
Name:   gmain
Pid:    27700
Name:   gdbus
Pid:    27701
Name:   Thread-3
Pid:    27702
Name:   re.pwnme
Pid:    27704
```

然后我们恢复apk进程执行, 发现最后停在了`/proc/self/task/27700/status` 

`gmain` 是 `frida`hook 时产生的进程，因此这里主要是检测 `frida`，从这一条我们就可以知道是如何检测 `frida` 的了，

该 `Native` 库会读主要进程下面所有子进程的 `status`，如果检测到 `frida` 产生的进程，则直接退出。

```
[PBCM10::re.pwnme ]-> %resume
[PBCM10::re.pwnme ]-> [+] Open ==> /proc/self/cmdline
[+] Open ==> /data/app/re.pwnme-zTbqjxGxX-j6lOJvkpbGsg==/base.apk
[+] Snprintf(arg0,) ==>: 50000
[+] Open ==> /proc/28008/timerslack_ns
[+] Open ==> /data/vendor/gpu/esx_config_re.pwnme.txt
[+] Open ==> /data/vendor/gpu/esx_config.txt
[+] Open ==> /data/misc/gpu/esx_config_re.pwnme.txt
[+] Open ==> /data/misc/gpu/esx_config.txt
[+] Open ==> /data/app/re.pwnme-zTbqjxGxX-j6lOJvkpbGsg==/lib/arm64/libnative-lib.so
[+] Snprintf(arg0,) ==>: /proc/self/task/27678/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27688/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27689/status
[+] Open ==> /data/local/su
[+] Open ==> /data/local/bin/su
[+] Open ==> /data/local/xbin/su
[+] Open ==> /sbin/su
[+] Snprintf(arg0,) ==>: /proc/self/task/27690/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27691/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27692/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27693/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27694/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27696/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27697/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27698/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27699/status
[+] Snprintf(arg0,) ==>: /proc/self/task/27700/status
[+] Snprintf(arg0,) ==>: 50000
[+] Open ==> /proc/28015/timerslack_ns
[+] Open ==> /proc/cpuinfo
[+] Snprintf(arg0,) ==>: 0
[+] Snprintf(arg0,) ==>: 0
[+] Snprintf(arg0,) ==>: 0
[+] Snprintf(arg0,) ==>: 0
Process crashed: Bad access due to invalid address

***
Process name is com.google.process.gservices, not key_process
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'OPPO/PBCM10/PBCM10:10/QKQ1.191224.003/1615196842:user/release-keys'
Revision: '0'
ABI: 'arm64'
Timestamp: 2024-06-28 16:58:17+0800
pid: 27678, tid: 28012, name: re.pwnme  >>> com.google.process.gservices <<<
uid: 10246
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xfabb11cd
    x0  0000007e057fb710  x1  000000008a3bda98  x2  0000000000000000  x3  0000000000000000
    x4  00000000ffffffff  x5  0000000000000000  x6  0000007e057fbd50  x7  0000000000ffd888
    x8  00000000000067c8  x9  00000000fabb11cd  x10 0000000085b34305  x11 0000000000000001
    x12 000000000739dade  x13 00000000fffffff6  x14 000000000739dade  x15 0000000000000000
    x16 0000000000000001  x17 0000007eef9f240c  x18 0000007dfd440000  x19 0000007e057fb710
    x20 0000007ef135f6fc  x21 0000007e057fbd50  x22 0000007e057fc060  x23 0000007e057fbdd8
    x24 0000007e057fbd50  x25 0000007e057fbd50  x26 0000007e057fc020  x27 0000007ef465d020
    x28 0000007e05c0f4dc  x29 0000007e057fbcf0
    sp  0000007e057fb710  lr  0000007eef9f240c  pc  0000007e05c406cc

backtrace:
      #00 pc 000000000007b6cc  /data/app/re.pwnme-zTbqjxGxX-j6lOJvkpbGsg==/lib/arm64/libnative-lib.so (BuildId: f87b3bd9fcae36e63939958f412d03a42e0ce406)
      #01 pc 00000000000d9720  /apex/com.android.runtime/lib64/bionic/libc.so!libc.so (offset 0xd9000) (__pthread_start(void*)+36) (BuildId: 20c7dfeb41468016772e288818fb55e7)
      #02 pc 0000000000075f2c  /apex/com.android.runtime/lib64/bionic/libc.so!libc.so (offset 0x75000) (__start_thread+64) (BuildId: 20c7dfeb41468016772e288818fb55e7)
***
[PBCM10::re.pwnme ]->

Thank you for using Frida!
```





```
PBCM10:/proc/27678/task $ ps -A | grep "re.pwnme"
u0_a246      32190  1805 5761400  37264 0                   0 S re.pwnme
PBCM10:/proc/27678/task $ cd /proc/32190/task
PBCM10:/proc/32190/task $ cat ./*/status | awk "/(Name:)|(^Pid:)/"
Name:   re.pwnme
Pid:    32190
Name:   Jit thread pool
Pid:    32200
Name:   Runtime worker
Pid:    32201
Name:   Runtime worker
Pid:    32202
Name:   Runtime worker
Pid:    32203
Name:   Runtime worker
Pid:    32204
Name:   Signal Catcher
Pid:    32205
Name:   ADB-JDWP Connec
Pid:    32206
Name:   HeapTaskDaemon
Pid:    32208
Name:   ReferenceQueueD
Pid:    32209
Name:   FinalizerDaemon
Pid:    32210
Name:   FinalizerWatchd
Pid:    32211
Name:   gmain
Pid:    32212
Name:   gdbus
Pid:    32213
Name:   Thread-3
Pid:    32214
Name:   re.pwnme
Pid:    32216
PBCM10:/proc/32190/task $ cat /proc/32201/status > /data/local/tmp/status
```



