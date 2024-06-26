---
title: wiki-tool-逆向工具-IDA-IDC-练习手册
---
---
title: IDA脚本编写-IDC练习手册
categories: wiki
---



# 练习手册

# HeloWorld

```c
#include <idc.idc>

static main()
{
    Message("HelloWorld \n");
}
```

这个师傅写了很多的IDC例子

你自己可以跟着学习

# patch练习

```c
//文件名：test.idc
#include <idc.idc>
static main()
{
    auto x,FBin,ProcRange;
    auto start_addr=MinEA();
    FBin = "F7 05";//75
    
    for (x = FindBinary(start_addr,SEARCH_DOWN,FBin);x != BADADDR;x = FindBinary(x,SEARCH_DOWN,FBin))
    {
        x=x+5; //返回的x是第一个E8的地址，
        //加上5是第二个E8的地址
        PatchByte (x,0x90);//nop掉
        x = x + 3; //00
        PatchByte (x,0x90);
        x++;  //00 E8
        PatchWord (x,0x9090);
        x =x + 2 ; //F6 FF FF FF
        PatchDword(x,0x90909090);
    }
}
```

把出现的`E9 00 00 00 00` 给nop掉

```c
#include <idc.idc>
static main()
{
    auto start = 0x0000000000400620; // 起始地址
    auto end  = 0x0000000000402144; // 结束地址
    auto addr;
    Message("work start\n");
    for (addr = start; addr < end; addr++)
    {
        if (Byte(addr) == 0xE9 && Dword(addr + 1) == 0x00000000)
        {
            Message("%x\n",addr);
            PatchByte (addr, 0x90); // 替换第一个字节为nop指令
            PatchDword(addr + 1, 0x90909090); // 替换第二个字节为nop指令
        }
    }
    Message("work done\n");
}

```

题目: 把出现过`ds:zero2`附近的jnz修改为jmp

目的: 去除冗余代码,非花指令

```c
#include <idc.idc>
static main()
{
    auto start = 0x0000000000400620; // 起始地址
    auto end  = 0x0000000000402144; // 结束地址
    auto addr = start;
    auto addr2;
    auto sz_asm;
    while (addr < end)
    {
        sz_asm = GetDisasm(addr);
        if (strstr(sz_asm, "ds:zero2") != -1)
        {
            Message("Found at address: %X,", addr);

            for(addr2=addr;addr2<addr+120;addr2=addr2+ItemSize(addr2))
            {
                sz_asm = GetDisasm(addr2);
                if (strstr(sz_asm, "jnz") != -1)
                {
                    Message("%X\n", addr2);
                    PatchWord(addr2,0xE990);
                    break;
                }
            }
            if(addr2==addr+120)
            {
                Message("no\n");
            }
        }
        addr=addr+ItemSize(addr);
    }
}
```

# 寻找字节码

```c
//文件名：test.idc
#include <idc.idc>
static main()
{
    auto x,FBin;
    FBin = "E8 0A 00 00 00 E8 EB 0C 00 00 E8 F6 FF FF FF";
     Message("start\n");
    for (x = FindBinary(MinEA(),0x03,FBin);x != BADADDR;x = FindBinary(x,0x03,FBin))
    {
        Message("%X",x);
    }
    Message("end\n");
}
```

# 高亮

```c
#include <idc.idc>
static main(void)
{
    auto head, op;
    head = NextHead(0x00000000, 0xFFFFFFFF);
    while ( head != BADADDR )
    {
        op = GetMnem(head);
        Message("%x %s \n",head,op);
        if ( op == "jmp" || op == "call" )
            SetColor(head, CIC_ITEM, 0x010187);

        if (op == "xor")
            SetColor(head, CIC_ITEM, 0x010198);
        head = NextHead(head, 0xFFFFFFFF);
    }
}
```

在当前函数实现一个高亮

```c
#include <idc.idc>
static main()
{
    auto head, endEA,op;
    head  = GetFunctionAttr(ScreenEA(),FUNCATTR_START); 
    endEA = GetFunctionAttr(ScreenEA(), FUNCATTR_END);
    
    Message("|---- work ----|\n");
    while ((head < endEA) && (( head != BADADDR )))
    {
        op = GetMnem(head);
        if ( op == "call")
            SetColor(head, CIC_ITEM, 0x00FF00);
        head = NextHead(head, 0xFFFFFFFF);
    }
    Message("|---- end  ----|\n");
}
```

# dump数据

```
auto i,fp;
fp = fopen("d:\\dump.dex","wb");
for(i=0x46B6D000;i<0x46B6f000;i++)
{
    fputc(Byte(i),fp);
}
```

将函数的名字dump到本地,dump出的文件名字是xxxfile_name_dump.log

文件的路径与你的xxx.exe相同

# 未命名

```c
#include <idc.idc>

static main(void)
{

    auto decode = 0x401000;
    auto xref;
    Message("xref: start\n");
    for(xref = RfirstB(decode); xref != BADADDR; xref = RnextB(decode,xref))
    {
        Message("xref: %x\n",xref);//交叉引用的上一个地址

        auto i = 0;
        auto inst = xref;
        auto op;

        while((i < 100) )
        {
            inst    = FindCode(inst,0x00); // flag set to backwards
            op      = GetDisasm(inst); // get
            Message("%x --> %s \n",inst,op);
            i++;
        }
    }
    Message("xref: end");
}
```

```c
#include <idc.idc>
static Find01(sz_name)
{
    auto i;
    auto inst;
    auto op,op1,op2;
    auto decode = LocByName(sz_name);//参数是函数的名字.然后返回函数的起始地址
    inst = RfirstB(decode);//参数是一个地址,返回交叉引用该地址的地址
    i = 0;
    while(i < 32)//默认遍历32个指令
    {
        inst = FindCode(inst,0x01);
        //参数是 地址,返回对应标志的地址,
        //标志0返回上一个指令的地址
        //标志1返回下一个指令的地址

        //op = GetDisasm(inst); //指令+操作数
        op1= GetMnem(inst);// 指令
        //op2= GetOpnd(inst,0);//操作数
        if(op1=="call")
        {
            Message("1,");
            return 1;
        }
        if(op1=="retn")
        {
            Message("0,");
            return 0;
        }
        i++;
    }
    Message("\n2\n");
    return 0;
}
static FindFunctionXref(func_name)
{
    auto func,addr,xref,who_call_it;

    func = LocByName(func_name);
    if(func == BADADDR)//没找到该函数
    {
        who_call_it="no";
        return who_call_it;
    }
    else
    {
        for(addr = RfirstB(func);addr != BADADDR; addr = RnextB(func,addr))
        {
            xref = XrefType();//不知道该函数是干嘛的
            if(xref == fl_CN || xref == fl_CF)
            {
                who_call_it = GetFunctionName(addr);
                //参数是一个地址,
                //如果该地址属于某一个函数,那么就返回该函数的名字
                //如果该地址不属于某一个函数,那么就返回空格" "字符串

                //Message("%s call => %0x in %s \n",func_name,addr,who_call_it);//返回函数,函数的被调用的地址,调用该函数的名
                return who_call_it;
            }
        }
    }
}

static main()
{
    auto x="flag";
    auto i=0;
    //最后输出的0/1是额外的函数,比如start调用main,main调用main_main,
    while(1)
    {
        Find01(x);
        x=FindFunctionXref(x);//推进函数的遍历,也就是不断的寻找上一个是谁调用了它
        if(x=="no")
            break;
        i++;
        if(i%8==0)
                Message("\n");
    }
}
```

```c
#include <idc.idc>
static FindFunctionXref(func_name)
{
    auto func,addr,xref,who_call_it;

    func = LocByName(func_name);
    if(func == BADADDR)//没找到该函数
    {
        who_call_it="no";
        return who_call_it;
    }
    else
    {
        for(addr = RfirstB(func);addr != BADADDR; addr = RnextB(func,addr))
        {
            xref = XrefType();//不知道该函数是干嘛的
            if(xref == fl_CN || xref == fl_CF)
            {
                who_call_it = GetFunctionName(addr);
                //参数是一个地址,
                //如果该地址属于某一个函数,那么就返回该函数的名字
                //如果该地址不属于某一个函数,那么就返回空格" "字符串

                //Message("%s call => %0x in %s \n",func_name,addr,who_call_it);//返回函数,函数的被调用的地址,调用该函数的名
                return who_call_it;
            }
        }
    }
}

static main()
{
    auto x="flag";
    auto i=0;
    //最后输出的0/1是额外的函数,比如start调用main,main调用main_main,
    while(1)
    {
        Message("%s\n",x);
        x=FindFunctionXref(x);//推进函数的遍历,也就是不断的寻找上一个是谁调用了它
        if(x=="no")
            break;
    }
}
```

```c
//文件名：test.idc
#include <idc.idc>
static main()
{
    auto x,y,FBin,flag,origEA,jmp_addr,ret_addr,funcStart,funcEnd,funcStart2,funcEnd2;

    origEA=0x00411D30;
    funcStart = GetFunctionAttr(origEA,FUNCATTR_START);
    funcEnd = GetFunctionAttr(origEA,FUNCATTR_END);
    FBin = "6A 00 E8";//push 0 ; call xxx
    flag="5D C3";
    //6A 00
    //E8 xx xx xx xx
    //
    for (x =  FindBinary(funcStart, SEARCH_DOWN,FBin) ; x < funcEnd ;x =  FindBinary(x, SEARCH_DOWN,FBin))
    {
        x=x+2;//来到call的位置
        PatchByte(x,0xE9);
        ret_addr=FindCode(x,1);
        jmp_addr=ret_addr+Dword(x+1);
        funcStart2=FindCode(jmp_addr,1)+Dword(jmp_addr+1);
        Message("%x\n",funcStart2);
        for (y = funcStart2 ;y < funcStart2+0x100; y = y+1)
        {
            if(Word(y)==0xC35D)
            {
                Message("%x\n",y);
                y=y+1;//来到retn
                PatchByte(y,0xE9);
                PatchDword(y+1,ret_addr-(y+5));
                break;
            }
        }
    }
    Message("end\n");
}
```

# patch90

函数: patch90

参数1: 要patch的起始地址

参数2: 要patch的长度

返回值: 无

```c
#include <idc.idc>
static patch90(lp_start,plen)
{
	auto i;
	for(i=0;i<plen;i++)
	{
		PatchByte(lp_start+i,0x90);
	}
	return;
}
static main()
{
	Message("|-----BEGIN-----|\n");
	patch90(0x080486A1,7);
	Message("|------END------|\n");
	return ;
}
```

# 文件操作

不是完整的版本,但是可以借鉴

```c
#include<idc.idc>
static format_C()//一开始
{

    auto i=0;
    auto start_addr=0x000001719ACE9040;
    auto fd = fopen("data.txt", "w");

 
     
    for(i=0;i<8717;i=i+1)
    {

        fprintf(fd,"0x%02X,",Byte(start_addr));
        start_addr=start_addr+1;
        if((i+1)%8==0)
        {
            fputc('\n',fd);
        }
    }
    fclose(fd);
}
static format_Hex()//一开始
{

    auto i=0;
    auto start_addr=0x000001719ACE9040;
    auto fd = fopen("data.txt", "w"); 
    for(i=0;i<8717;i=i+1)
    {

        fprintf(fd,"%02X",Byte(start_addr));
        start_addr=start_addr+1;
    }
    fclose(fd);
}
static format_binFile()
{
    auto i;
    auto flen=8717;
    auto start_addr=0x000001719ACE9040;
    auto fd = fopen("data.txt", "w"); 
    for(i=0;i<flen;i=i+1)
    {
        fputc(Byte(start_addr+i),fd);
    }
    fclose(fd);
}
static main()
{
    Message("| -- Y -- |\n");
    format_binFile();
    Message("| -- N -- |\n");
}
```