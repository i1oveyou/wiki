---
title: wiki-Reverse-winRe-shellcode-核心API加载
---
# x86之shellcode如何获取GetProcAddress和LoadLibrary

# 步骤如下

下面4个步骤的寄存器是有关联的

环境有关系



## 首先获取kernel32.dll的基地址



```assembly
xor ecx, ecx;
mov eax, fs: [ecx + 0x30] ;//获取PEB
mov eax, [eax + 0xc];	// 获取LDR
mov esi, [eax + 0x14]; //获取 InMemOrder,然后已经指向了当前进程
lodsd;  //指向ntdll
xchg eax, esi;   //数据交换
lodsd; //指向Kernel32.dll
mov ebx, [eax + 0x10]; //获取Base address
```



这里是简单的获取kernel32.dll基地址

获取kernel32.dll基地址方法很多,,,挑一个喜欢的



## 然后找到kernel32.dll的导出表



```assembly
mov edx, [ebx + 0x3c]; //获取偏移
add edx, ebx; //来到PE头
mov edx, [edx + 0x78]; //获取导出表
add edx, ebx; 
mov esi, [edx + 0x20]; //获取 AddressOfNames
add esi, ebx; 
```



这里是通过PE结构,,,然后找到导出表

导出表结构如下

```c
struct _IMAGE_EXPORT_DIRECTORY
{
    DWORD   Characteristics;    	//+0 未使用 导出表的特征标志，一般为0 
    DWORD   TimeDateStamp;      	//+4 时间戳 导出表的创建时间戳。
    WORD    MajorVersion;       	//+8h 未使用 导出表的主版本号
    WORD    MinorVersion;       	//+10 未使用 导出表的次版本号。

    DWORD   Name;               	//+12 字符串指针 dll的名字
    DWORD   Base;               	//+16 基址编号 导出表中所有函数的序号起始值，默认为1
    DWORD   NumberOfFunctions;  	//+20 导出表中的导出函数数量,其中是有空函数的
    DWORD   NumberOfNames;      	//+24 导出表中有字符串名称的导出函数数量
    DWORD   AddressOfFunctions;     //+28  dword数组, 实际函数的RvA数组 导出表中所有导出函数
    DWORD   AddressOfNames;         //+32 dword数组 导出表中所有有名称的导出函数的名称
    DWORD   AddressOfNameOrdinals;  //+36 word数组  导出表中所有有名称的导出函数序号,成员是(序号-BASE)的序列
} IMAGE_EXPORT_DIRECTORY, *PIMAGE_EXPORT_DIRECTORY;
```





## 然后遍历导出表信息,获取GetProcAddress



```assembly
	xor ecx, ecx;
Get_Function:
    ; //ebx 是基地址
    ; //esi 是AddressOfNames
    ; //ecx 是遍历的次数
    ; //edx是导出表结构体的起始地址
    inc ecx; //次数增加
    lodsd; //mov eax,[esi]
    add eax, ebx; //获取真实的地址
    cmp dword ptr[eax], 0x50746547; 
    jnz Get_Function;
    cmp dword ptr[eax + 0x4], 0x41636f72; rocA
    jnz Get_Function;
    cmp dword ptr[eax + 0x8], 0x65726464; ddre
    jnz Get_Function;

    //找到了
    mov esi, [edx + 0x24]; //获取AddressOfNameOrdinals
    add esi, ebx; 

    dec ecx
    mov cx, [esi + ecx * 2];//基于word的数组
    mov esi, [edx + 0x1c]; //获取 AddressOfFunctions
    add esi, ebx; 
    mov edx, [esi + ecx * 4]; 
    add edx, ebx; //最后得到真实的地址
```



这是一个简单的遍历`AddressOfNameOrdinals,AddressOfFunctions,AddressOfNames`

其中字符串的比较我之前没有遇到过

```assembly
cmp dword ptr[eax], 0x50746547; 
jnz Get_Function;
cmp dword ptr[eax + 0x4], 0x41636f72; rocA
jnz Get_Function;
cmp dword ptr[eax + 0x8], 0x65726464; ddre
```

他不是利用全局的字符串

而是通过4字节写到机器码中, ` 0x50746547,0x41636f72,0x65726464`









## 通过GetProcAddress获取LoadLibrary



```assembly
xor ecx, ecx; ECX = 0
push ebx; Kernel32 base address
push edx; GetProcAddress

push ecx; 0
push 0x41797261; aryA
push 0x7262694c; Libr
push 0x64616f4c; Load

push esp; "LoadLibrary"
push ebx; Kernel32 base address
call edx; //获取LoadLibrary
add esp, 0xc;
```



# 总的如下





```assembly
    _asm
    {
        xor ecx, ecx;
        mov eax, fs: [ecx + 0x30] ;//获取PEB
        mov eax, [eax + 0xc];// 获取LDR
        mov esi, [eax + 0x14]; //获取 InMemOrder,然后已经指向了当前进程
        lodsd;  //指向ntdll
        xchg eax, esi;   //数据交换
        lodsd; //指向Kernel32.dll
        mov ebx, [eax + 0x10]; //获取Base address
            
        mov edx, [ebx + 0x3c]; //获取偏移
        add edx, ebx; //来到PE头
        mov edx, [edx + 0x78]; //获取导出表
        add edx, ebx; 
        mov esi, [edx + 0x20]; //获取 AddressOfNames
        add esi, ebx; 

        xor ecx, ecx;
    Get_Function:
        ; //ebx 是基地址
        ; //esi 是AddressOfNames
        ; //ecx 是遍历的次数
        ; //edx是导出表结构体的起始地址
        inc ecx; //次数增加
        lodsd; //mov eax,[esi]
        add eax, ebx; //获取真实的地址
        cmp dword ptr[eax], 0x50746547; 
        jnz Get_Function;
        cmp dword ptr[eax + 0x4], 0x41636f72; rocA
        jnz Get_Function;
        cmp dword ptr[eax + 0x8], 0x65726464; ddre
        jnz Get_Function;

        //找到了
        mov esi, [edx + 0x24]; //获取AddressOfNameOrdinals
        add esi, ebx; 
        
        dec ecx
        mov cx, [esi + ecx * 2];//基于word的数组
        mov esi, [edx + 0x1c]; //获取 AddressOfFunctions
        add esi, ebx; 
        mov edx, [esi + ecx * 4]; 
        add edx, ebx; //最后得到真实的地址

        xor ecx, ecx; ECX = 0
        push ebx; Kernel32 base address
        push edx; GetProcAddress

        push ecx; 0
        push 0x41797261; aryA
        push 0x7262694c; Libr
        push 0x64616f4c; Load

        push esp; "LoadLibrary"
        push ebx; Kernel32 base address
        call edx; //获取LoadLibrary
        add esp, 0xc;
        
        //一些自定义的代码
	}
```



另外一个大佬的版本,使用nasm进行一个编译

```assembly
; exec_calc.asm
global Start
section .data
section .text
Start:
    push ebp
    mov ebp, esp
    sub esp, 0x12
    call GetKernel32BaseAddr
    mov dword [ebp-4],eax ; Kernel32.dll Base Addr
    push eax
    call GetProcAddrFuncAddr
    mov dword [ebp-8],eax ; GetProcAddress
    push 0x00636578 ; xec,0x00
    push 0x456e6957 ; WinE
    push esp
    push dword [ebp-4] ; [ebp-4] -> Kernel32.DLL Base Addr
    call dword [ebp-8] ; [ebp-8] -> GetProcAddress Addr
    push 0                ; WinExec uCmdShow
    push 0x6578652e       ; exe. : 6578652e
    push 0x636c6163       ; clac : 636c6163
    push esp
    call eax
    nop
    nop
    add esp,0x12
    mov esp,ebp
    pop ebp
    ret
GetKernel32BaseAddr:
    push ebp
    mov ebp,esp
    sub esp,0x40
    xor ebx, ebx            ; EBX = 0x00000000
    mov ebx, [fs:ebx+0x30]  ; EBX = Address_of_PEB
    mov ebx, [ebx+0xC]      ; EBX = Address_of_LDR
    mov ebx, [ebx+0x1C]     ; EBX = 1st entry in InitOrderModuleList / ntdll.dll
    mov ebx, [ebx]          ; EBX = 2nd entry in InitOrderModuleList / kernelbase.dll
    mov ebx, [ebx]          ; EBX = 3rd entry in InitOrderModuleList / kernel32.dll
    mov eax, [ebx+0x8]      ; EAX = &kernel32.dll / Address of kernel32.dll
    add esp,0x40
    mov esp,ebp
    pop ebp
    ret
GetProcAddrFuncAddr:
    push ebp
    mov ebp,esp
    sub esp,0x40
    xor ecx, ecx
    mov ebx, [ebp + 8] ; EBX = Base address
    mov edx, [ebx + 0x3c]    ; EDX = DOS->e_lfanew
    add edx, ebx             ; EDX = PE Header
    mov edx, [edx + 0x78]    ; EDX =  export table
    add edx, ebx             ; EDX = Export table
    mov esi, [edx + 0x20]    ; ESI =  namestable
    add esi, ebx             ; ESI = Names table
    xor ecx, ecx             ; EXC = 0
    Get_Function:
            inc ecx                  ; Increment the ordinal
            lodsd                    ; Get name
            add eax, ebx             ; Get function name
            cmp dword [eax], 50746547h       ; GetP
            jnz Get_Function
            cmp dword [eax + 0x04], 41636f72h ; rocA
            jnz Get_Function
            cmp dword [eax + 0x08], 65726464h ; ddre
            jnz Get_Function
    mov esi, [edx + 0x24]                ; ESI =  ordinals
    add esi, ebx                         ; ESI = Ordinals table
    mov cx, [esi + ecx * 2]              ; Number of function
    dec ecx
    mov esi, [edx + 0x1c]                ;  address table
    add esi, ebx                         ; ESI = Address table
    mov edx, [esi + ecx * 4]             ; EDX = Pointer()
    add edx, ebx                         ; EDX = GetProcAddress
    mov eax,edx
    add esp,0x40
    mov esp,ebp
    pop ebp
    ret

```





# 关于hash 函数名的算法



其实就是,,我们已经拿到了 GetProcAddress 和 LoadLibrary

当我们去获取一个目标函数的时候 GetProcAddress (xx_base,xx_name)

想这种方式去获取API的话,,,有点赤裸裸的,,,也就是比较暴露目标API的string



于是网上出现了另外一种方法,,,,

假设我们有这么一种hash算法, ROR13

假设我们已经有了目标API的hash是A, 目标dll的hash是B

我们先遍历每一个模块,,,计算他们的ROR13 hash,然后我们提供的hash做一个比较

当我们找到目标DLL后,,,然后遍历他们导出的函数,,计算他们的ROR13,,,,然后我们提供的hash做一个比较

通过这样的方式,,,我们就可以避免提供明文字符串来获取API

当然我还见过一种方式,只提供一个ROR13,,就获取目标API的

也就是遍历已装载dll的所有导出函数,,,然后计算他们dllname和funcname的ROR13哈希,,然后和我们提供的hash做一个人比较



ROR13 hash算法实现

ps: 最好别用这种,,任意被查杀

```c
DWORD __stdcall unicode_ror13_hash(const WCHAR *unicode_string)
{
    DWORD hash = 0;

    while (*unicode_string != 0)
    {
        DWORD val = (DWORD)*unicode_string++;
        hash = (hash >> 13) | (hash << 19); // ROR 13
        hash += val;
    }
    return hash;
}

DWORD __stdcall ror13_hash(const char *string)
{
    DWORD hash = 0;

    while (*string) {
        DWORD val = (DWORD) *string++;
        hash = (hash >> 13)|(hash << 19);  // ROR 13
        hash += val;
    }
    return hash;
}

```



我们提供的dll好像一般都是英文名字,,,好像也有其它乱七八糟的字符,,但是函数的名字一定是中文



