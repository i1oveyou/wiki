

# so

对比0.9和1.0的elf

共同的导入符号:
```
mprotect
pthread_create
isdigit
open
printf
__cxa_finalize
calloc
__progname
closedir
snprintf
sscanf
gmtime_r
rand
__stack_chk_fail
nanosleep
opendir
readdir
malloc
memcpy
free
__system_property_get
__cxa_atexit
isspace
```

只在1.0 中的导入符号:
```
signal
lstat
tan
getpid
fork
strstr
exit
```

只在 0.9 中的导入符号:
```
strcmp
memset
```

# asm



```

[A]18D28 MOV             W11, #0x34A5           
[A]18D2C STUR            W11, [lp_var1]       ;var1 = 0x34A5
[A]18D30 ADRP            X10, #dword_1B4008@PAGE 
[A]18D34 LDR             W11, [X10,#dword_1B4008@PAGEOFF] // 
[A]18D38 MOV             W10, W11               
[A]18D3C STUR            X10, [lp_gVar]       
[A]18D40 LDUR            W11, [lp_var1]       
[A]18D44 LSL             W11, W11, #1           ; w11=var1*2
[A]18D48 LDUR            X10, [lp_gVar]       
[A]18D4C ADD             X10, X10, W11,SXTW#2   ; X10 = gVar + var*8
[A]18D50 STUR            X10, [lp_gVar]         ; gVar= gVar + var*8
[A]18D54 LDUR            X10, [lp_gVar]         ; X10 = gVar + var*8
[A]18D58 LDR             W11, [X10]             ; W11 = *(gVar + var*8) Exception_1
[A]18D5C LDUR            W12, [lp_var1]         ; w12=var1
[A]18D60 MOV             W13, WZR               ; W13 = 0
[A]18D64 SUBS            W11, W13, W11          ; W11 = 0 - *(gVar + var*8)
[A]18D68 MOV             W14, #0xCF5D1FB6       ; W14 = 0xCF5D1FB6
[A]18D70 SUBS            W11, W14, W11          ; W11 = 0xCF5D1FB6 + *(gVar + var*8)
[A]18D74 SUBS            W12, W13, W12          ; W12 = 0 - var1
[A]18D78 SUBS            W11, W11, W12          ; W11 =  0xCF5D1FB6 + *(gVar + var*8) +var1
[A]18D7C MOV             W12, #0xDA65FB6F       ; W12 = r2
[A]18D84 SUBS            W11, W12, W11          ; W11 = r2 - (r1 + *(gVar + var*8) +var1)
[A]18D88 MOV             W12, #0xB08DBB9        ; W12 = r3
[A]18D90 SUBS            W11, W12, W11          ; W11 = r3 - r2 + (r1 + *(gVar + var*8) +var1)
[A]18D94 LDUR            X8, [lp_gVar]           
[A]18D98 ADD             X8, X8, W11,SXTW#2     ; X8 = gVar + (r3 - r2 + (r1 + *(gVar + var*8) +var1))*4
[A]18D9C STUR            X8, [lp_gVar]          ; gvar= gVar + (r3 - r2 + (r1 + *(gVar + var*8) +var1))*4
[A]18DA0 MOV             X8, XZR                ; X8 = 0
[A]18DA4 STUR            X8, [lp_gVar]          ; gVar=0
[A]18DA8 LDUR            X8, [lp_gVar]        	
[A]18DAC LDRSW           X8, [X8]               ; X8 =*0  Exception_2
[A]18DB0 LDUR            X10, [lp_gVar]         ; X10 = 0
[A]18DB4 ADD             X8, X10, X8,LSL#2      ; X8 = 0 + *0 x4
[A]18DB8 STUR            X8, [lp_gVar]          ; gVar= 0 + *0 x4
[A]18DBC LDUR            X8, [lp_gVar]          ; 
[A]18DC0 LDR             W11, [X8]              ; W11 = *(0 + *0 x4) Exception_3
[A]18DC4 STR             W11, [X19,#0x1CD4]     ; var3=w11

[A]18DC8 ADRP            X8, #x.91_ptr@PAGE      
[A]18DCC LDR             X8, [X8,#x.91_ptr@PAGEOFF]
[A]18DD0 LDR             W11, [X8]
[A]18DD4 ADRP            X8, #y.92_ptr@PAGE
[A]18DD8 LDR             X8, [X8,#y.92_ptr@PAGEOFF]
[A]18DDC LDR             W12, [X8]
[A]18DE0 MOV             W13, #0x3293E9F2
[A]18DE8 SUBS            W13, W13, W11
[A]18DEC MOV             W14, #0x3293E9F1
[A]18DF4 SUBS            W13, W14, W13
[A]18DF8 MUL             W11, W11, W13
[A]18DFC ANDS            W11, W11, #1
[A]18E00 CSET            W13, EQ
[A]18E04 SUBS            W14, W12, #0xA
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
    
'''
0x9E7F4: MOV             W11, #0x9218
0x9E940: MOV             W11, #0x9218
0xEEC20: MOV             W11, #0x9218
0xEED1C: MOV             W11, #0x9218
这4个地方,貌似都是crash
'''
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
    search_string = "ADRP            X10, #dword_1B4008@PAGE"
    results = search_for_string_in_code(search_string)
    cnt=0
    for ea, disasm in results:
        cnt=cnt+1
        print(f"[{cnt:02}]:Address 0x{ea:X}: {disasm}")

if __name__ == "__main__":
    main()

'''
[01]:Address 0x18D30: ADRP            X10, #dword_1B4008@PAGE
[02]:Address 0x18EC8: ADRP            X10, #dword_1B4008@PAGE
[03]:Address 0x192B8: ADRP            X10, #dword_1B4008@PAGE
...
[84]:Address 0xEAD4C: ADRP            X10, #dword_1B4008@PAGE
[85]:Address 0xEEC28: ADRP            X10, #dword_1B4008@PAGE
[86]:Address 0xEED24: ADRP            X10, #dword_1B4008@PAGE
一共86处
'''
```





```
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
        if "ADRP            X10, #dword_1B4008@PAGE" == st_asm1:
            idx_movw8=i-2
            st_asm2 = get_disassembly(arr_address[idx_movw8])
            if "MOV             W11" in st_asm2:
                #cnt=cnt+1
                #print(f"[{cnt}]Address 0x{arr_address[idx_movw8]:X}: {st_asm2}")
                idx_LDRW8X9=idx_movw8+25
                for j in range(20):
                    st_asm3 = get_disassembly(arr_address[idx_LDRW8X9+j])
                    st_asm4 = get_disassembly(arr_address[idx_LDRW8X9+j-1])
                    st_asm5 = get_disassembly(arr_address[idx_LDRW8X9+j-2])
                    if "LDR             W11, [X8]"==st_asm3 and "LDUR" in st_asm4 and "STUR" in st_asm5:
                        cnt=cnt+1
                        len_code=arr_address[idx_LDRW8X9+j]- arr_address[idx_movw8]
                        print(f"[{cnt:02}]==> {arr_address[idx_movw8]:X}~{arr_address[idx_LDRW8X9+j]:X} len {len_code}")
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



# 进程查看





```
C:\mm_dqx\code
λ frida-ps -Ua
  PID  Name         Identifier
-----  -----------  --------------------------------
17384  Radare2 Pay  re.pwnme
 3371  SIM 卡应用程序    com.android.stk
 3371  SIM 卡应用程序    com.android.stk
17528  mm_dqx       yustd.ybrn.t
 7022  应用宝          com.tencent.android.qqdownloader
 3772  我的 OPPO      com.oppo.usercenter
12260  手机管家         com.coloros.phonemanager
12496  文件           com.android.documentsui
 8283  日历           com.coloros.calendar
16277  设置           com.android.settings
16946  软件商店         com.heytap.market
```



```
PBCM10:/ # ps -a | grep "Pay"
PBCM10:/ # (nothing)
PBCM10:/ # ps -a | grep "re.pwnme"
PBCM10:/ # (nothing)
```



# out

![image-20240628132800213](./img/image-20240628132800213.png)
