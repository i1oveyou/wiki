---
title: tmp_blog-Android-CrackeMe-OWASP-Mobile-Application-Security-Android-UnCrackable-L4-v0.9
---



# 1



pin: 4

amount: <=8




# java

检测当前手机有没有安装一些软件,比如magisk

```java
    public final boolean f11(List<String> packages) {
        boolean result = false;
        PackageManager pm = this.env_ctx.getPackageManager();
        for (String packageName : packages) {
            try {
                pm.getPackageInfo(packageName, 0);//查看有没有安装,没有就抛出异常
                b.a.a.c.a.a(packageName + " ROOT management app detected!");
                result = true;
            }
            catch (PackageManager.NameNotFoundException e) {
                Log.d("dqx","nth");
            }
        }
        return result;
    }

```





在所有环境变量中,检测有没有su

```java
    public boolean f3("su") {
        String[] pathsArray = res_Class.a();
        boolean result = false;
        for (String path : pathsArray) {
            String completePath = path + filename;
            File f = new File(path, filename);
            boolean fileExists = f.exists();
            if (fileExists) {
                b.a.a.c.a.b(completePath + " binary detected!");
                result = true;
            }
        }
        return result;
    }
```





"getprop"环境检测

```
    public boolean f4() {
        Map<String, String> dangerousProps = new HashMap<>();
        dangerousProps.put("ro.debuggable", "1");
        dangerousProps.put("ro.secure", "0");
        boolean result = false;
        String[] lines = m511b();
        if (lines == null) {
            return false;
        }
        for (String line : lines) {
            for (String key : dangerousProps.keySet()) {
                if (line.contains(key)) {
                    String badValue = "[" + dangerousProps.get(key) + "]";
                    if (line.contains(badValue)) {
                        b.a.a.c.a.b(key + " = " + badValue + " detected!");
                        result = true;
                    }
                }
            }
        }
        return result;
    }
```





输出指令,然后检查结果 `which su`

```
    public boolean f7() {
        Process process = null;
        try {
            process = Runtime.getRuntime().exec(new String[]{"which", "su"});
            BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
            boolean z = in.readLine() != null;
            process.destroy();
            return z;
        } catch (Throwable th) {
            if (process != null) {
                process.destroy();
            }
            return false;
        }
    }
```



# Frida



```js
Interceptor.attach(Module.findExportByName(null, "android_dlopen_ext"), {
  onEnter: function(args){
	  console.log("\nlib: ", Memory.readUtf8String(args[0]));
	  },
  onLeave: function(retval){
	  }
});




Interceptor.attach(Module.findExportByName("libc.so", "lstat"), {
	onEnter : function(args) {
		console.warn("lstat ", args[0].readUtf8String());
		var buf;
		if(args[0].readUtf8String().indexOf("/fd/") > -1) {
			buf = Memory.allocUtf8String('/proc/self/fd/0');
			this.buf = buf;
			args[0] = buf;
			console.log("change to " + args[0].readUtf8String() + "\n");
		}
	},
	onLeave : function(retval) {
	}
});

var tmp;
Interceptor.attach(Module.findExportByName("libc.so", "snprintf"), {
	onEnter : function(args) {
		tmp = args[0];	
	},
	onLeave : function(retval) {
		console.warn("snprintf ", tmp.readUtf8String());
	}
})
```





# assembly



```
.text:0000000000020E78                               loc_20E78                               ; CODE XREF: sub_20954+394↑j
.text:0000000000020E78 08 32 90 52                   MOV             W8, #0x8190             ; W8=0x8190
.text:0000000000020E7C 68 C6 31 B9                   STR             W8, [X19,#0x31C4]       ; [X19+0x31c4]=W8
.text:0000000000020E80 09 0A 00 F0                   ADRP            X9, #dword_163008@PAGE  ; X9=lp_gVar
.text:0000000000020E84 28 09 40 B9                   LDR             W8, [X9,#dword_163008@PAGEOFF] ; W8=gVar
.text:0000000000020E88 E9 03 08 2A                   MOV             W9, W8                  ; W9=W8=gVar
.text:0000000000020E8C 69 DE 18 F9                   STR             X9, [X19,#0x31B8]       ; [X19+#0x31B8]=gVar
.text:0000000000020E90 68 C6 71 B9                   LDR             W8, [X19,#0x31C4]       ; W8=0x8190
.text:0000000000020E94 08 79 1F 53                   LSL             W8, W8, #1              ; W8=0x8190*2
.text:0000000000020E98 69 DE 58 F9                   LDR             X9, [X19,#0x31B8]       ; X9=gVar
.text:0000000000020E9C 29 C9 28 8B                   ADD             X9, X9, W8,SXTW#2       ; gVar=0x8190*2+gVar
.text:0000000000020EA0 69 DE 18 F9                   STR             X9, [X19,#0x31B8]       ; [X19+#0x31B8]=gVar=0x8190*2+gVar
.text:0000000000020EA4 69 DE 58 F9                   LDR             X9, [X19,#0x31B8]
.text:0000000000020EA8 28 01 40 B9                   LDR             W8, [X9]                ; w8=*(0x8190*2+gVar)
.text:0000000000020EAC 6A C6 71 B9                   LDR             W10, [X19,#0x31C4]      ; W10=0x8190
.text:0000000000020EB0 EB 03 1F 2A                   MOV             W11, WZR
.text:0000000000020EB4 68 01 08 6B                   SUBS            W8, W11, W8
.text:0000000000020EB8 48 01 08 6B                   SUBS            W8, W10, W8             ; w8=0x8190+*(0x8190*2+gVar)
.text:0000000000020EBC 69 DE 58 F9                   LDR             X9, [X19,#0x31B8]
.text:0000000000020EC0 29 C9 28 8B                   ADD             X9, X9, W8,SXTW#2       ; X9=0x8190*2+gVar+0x8190+*(0x8190*2+gVar)
.text:0000000000020EC4 69 DE 18 F9                   STR             X9, [X19,#0x31B8]       ; [X19+#0x31B8]=xx
.text:0000000000020EC8 E9 03 1F AA                   MOV             X9, XZR
.text:0000000000020ECC 69 DE 18 F9                   STR             X9, [X19,#0x31B8]       ; X19,#0x31B8]=0
.text:0000000000020ED0 69 DE 58 F9                   LDR             X9, [X19,#0x31B8]
.text:0000000000020ED4 29 01 80 B9                   LDRSW           X9, [X9]                ; X9=*0
.text:0000000000020ED8 6C DE 58 F9                   LDR             X12, [X19,#0x31B8]
.text:0000000000020EDC 89 09 09 8B                   ADD             X9, X12, X9,LSL#2       ; X9=0+(*0)*4
.text:0000000000020EE0 69 DE 18 F9                   STR             X9, [X19,#0x31B8]       ; [X19,#0x31B8]=(int*)0+(*0)*4
.text:0000000000020EE4 69 DE 58 F9                   LDR             X9, [X19,#0x31B8]
.text:0000000000020EE8 28 01 40 B9                   LDR             W8, [X9]                ; maybe end
```









# ida python



```python

import idaapi
import idautils
import idc

def search_for_immediate_value(value):
    results = []
    for seg_ea in idautils.Segments():
        seg = idaapi.getseg(seg_ea)
        if seg.type == idaapi.SEG_CODE:
            for head in idautils.Heads(seg.start_ea, seg.end_ea):
                if idc.is_code(idc.get_full_flags(head)):
                    disasm_line = idc.generate_disasm_line(head, 0)
                    if f"#0x{value:X}" in disasm_line:
                        results.append((head, disasm_line))
    return results

def main():
    immediate_value = 0x9218
    results = search_for_immediate_value(immediate_value)

    for ea, disasm in results:
        print(f"0x{ea:X}: {disasm}")

if __name__ == "__main__":
    main()

```







```python
import idaapi
import idautils
import idc

def search_for_string_in_code(string):
    results = []
    for seg_ea in idautils.Segments():
        seg = idaapi.getseg(seg_ea)
        if seg.type == idaapi.SEG_CODE:
            for head in idautils.Heads(seg.start_ea, seg.end_ea):
                if idc.is_code(idc.get_full_flags(head)):
                    disasm_line = idc.generate_disasm_line(head, 0)
                    if string == disasm_line:
                        results.append((head, disasm_line))
    return results

def main():
    search_string = "ADRP            X9, #dword_163008@PAGE"
    results = search_for_string_in_code(search_string)
    cnt=0
    for ea, disasm in results:
        cnt=cnt+1
        print(f"[{cnt}]:Address 0x{ea:X}: {disasm}")

if __name__ == "__main__":
    main()

```





```py
import idaapi
import idautils
import idc
def nop_instruction(ea):
    # 获取指令长度
    length = idc.get_item_size(ea)
    
    # ARM64 的 NOP 指令是 4 字节
    nop_bytes = b'\x1F\x20\x03\xD5' * (length // 4)
    
    # 将地址处的指令替换为 NOP
    idaapi.patch_bytes(ea, nop_bytes)
    #print(f"Address 0x{ea:X}: NOPed {length} bytes")
    
def get_code_addresses():
    addresses = []
    for seg_ea in idautils.Segments():
        seg = idaapi.getseg(seg_ea)
        if seg.type == idaapi.SEG_CODE:
            for head in idautils.Heads(seg.start_ea, seg.end_ea):
                if idc.is_code(idc.get_full_flags(head)):
                    addresses.append(head)
    return addresses

def get_disassembly(ea):
    return idc.generate_disasm_line(ea, 0)

def get_crash_area():
    cnt=0
    idx_movw8=0
    idx_LDRW8X9=0
    arr_address = get_code_addresses()
    for i in range(2, len(arr_address)-40):  # 从第3个指令开始，确保可以向上检查两条指令
        st_asm1 = get_disassembly(arr_address[i])
        if "ADRP            X9, #dword_163008@PAGE" == st_asm1:
            idx_movw8=i-2
            st_asm2 = get_disassembly(arr_address[idx_movw8])
            if "MOV             W8" in st_asm2:
                #cnt=cnt+1
                #print(f"[{cnt}]Address 0x{arr_address[idx_movw8]:X}: {st_asm2}")
                idx_LDRW8X9=idx_movw8+24
                for j in range(10):
                    st_asm3 = get_disassembly(arr_address[idx_LDRW8X9+j])
                    if "LDR             W8, [X9]"==st_asm3:
                        cnt=cnt+1
                        print(f"[{cnt:02}]==> {arr_address[idx_movw8]:X}~{arr_address[idx_LDRW8X9+j]:X}")
                        idx_tmp=idx_movw8
                        while idx_tmp<=(idx_LDRW8X9+j):
                            nop_instruction(arr_address[idx_tmp])
                            idx_tmp=idx_tmp+1
                        break

def main():
    get_crash_area()
    

if __name__ == "__main__":
    main()

```
