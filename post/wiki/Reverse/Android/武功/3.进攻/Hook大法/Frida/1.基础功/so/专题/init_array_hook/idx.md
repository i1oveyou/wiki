# Reference Documents

https://www.jianshu.com/p/59d1d3054abe

# dlopen

为了hook dll的 init_array, 我尝试去hook dlopen, 发现hook不到



```js
Java.perform(function () 
{

    var funcAddress = Module.findExportByName("libc.so", 'dlopen')

    var pmValue = '';
    Interceptor.attach(funcAddress, 
    {
        onEnter:
            function (args) 
            {
                pmValue = Memory.readUtf8String(args[0]);
                console.log(pmValue);
            },
        onLeave:
            function (retval) 
            {
                if (pmValue.indexOf('libfoo.so') != -1) 
                {
                    console.log('get in libfoo');
                    Interceptor.attach(Module.findBaseAddress('libfoo.so').add(0x12C0), 
                    {
                        onEnter: function (args) {
                            console.log("Secret generator on enter, address of secret: " + args[0]);
                            this.answerLocation = args[0];
                            console.log(hexdump(this.answerLocation, 
                            {
                                offset: 0,
                                length: 0x20,
                                header: true,
                                ansi: true
                            }));
                        },
                        onLeave: function (retval) 
                        {
                            console.log("Secret generator on leave");
                            console.log(hexdump(this.answerLocation, 
                            {
                                offset: 0,
                                length: 0x20,
                                header: true,
                                ansi: true
                            }))
                        }
                    });
                    //sub hook
                }
            
            }
        
    })
});

```







# elf_init_array_hook

init > init_array > start

就图一个乐,发现啥也没用.



```js
function hookInit(soName,isHooked){

    if(!isHooked){
        console.log("hook init",soName);
        var targetSoAddr=Module.findBaseAddress(soName);
        var init_proc_addr=targetSoAddr.add(0x1000);
        Interceptor.replace(init_proc_addr,new NativeCallback(function(){
            console.log("init_proc replaced");
        },'void',[]));

        return true;
    }
}
function hookInitArray(soName,isHooked){

    if(!isHooked){
        var targetSoAddr=Module.findBaseAddress(soName);
        var func1=targetSoAddr.add(0x031B0);
        Interceptor.replace(func1,new NativeCallback(function(){
            console.log("init_array replaced");
        },'void',[]));
        console.log("[+] init_array hook down");
        return true;
    }else{
        console.log("[X] init_array not perminted hook");
        return false;
    }
}

function hook_call_constructor(soName){
    console.log("call_constructor",soName);
    // /system/bin/linker64 -->_dl__ZN6soinfo17call_constructorsEv
    var symbols=Process.getModuleByName("linker64").enumerateSymbols();
    var callConstructorAdd=null;
    for(var i=0;i<symbols.length;i++){
        const sym=symbols[i];
        if(sym.name.indexOf("_dl__ZN6soinfo17call_constructorsEv")!=-1){
            callConstructorAdd=sym.address;
        }
    }

    if(callConstructorAdd!=null){
        var isHooked=false;
        Interceptor.attach(callConstructorAdd,{
            onEnter: function(args){
               // console.log("[+] Enter->_dl__ZN6soinfo17call_constructorsEv");
                if(isHooked==false){
                    //hookInit(soName,isHooked);
                    isHooked=hookInitArray(soName,isHooked);

                }
            },
            onLeave: function(retval){
               // console.log("[+] Leave->_dl__ZN6soinfo17call_constructorsEv");
            }
        });
    }else{
        console.log("_dl__ZN6soinfo17call_constructorsEv not found");
    }

}

function hook_dlopen(addr,soName){
    console.log(addr,soName);
    Interceptor.attach(addr,{
        onEnter: function(args){
            var soPath=args[0].readCString();
            if(soPath.indexOf(soName)!=-1){
                hook_call_constructor(soName);
            }
        },
        onLeave: function(retval){
            //console.log("dlopen returned: " + retval)
        }
    });

}
function myFunction() {
    var android_dlopen_ext_addr=Module.findExportByName("libdl.so","android_dlopen_ext");
    hook_dlopen(android_dlopen_ext_addr,"libfoo.so");
}

myFunction();
```



