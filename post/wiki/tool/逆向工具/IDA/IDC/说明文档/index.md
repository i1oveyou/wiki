---
title: wiki-tool-逆向工具-IDA-IDC-说明文档
---
---
title: IDA脚本编写-IDC说明文档
categories: wiki
---

# 说明文档

学习链接:

[https://blog.csdn.net/weixin_44531336/article/details/125076279](

# 参考链接

🧡参考链接: lyshark [https://www.cnblogs.com/LyShark/p/13100048.html](https://www.cnblogs.com/LyShark/p/13100048.html)

[https://introspelliam.github.io/2017/09/18/tools/IDA%E7%9A%84%E8%B0%83%E8%AF%95%E8%84%9A%E6%9C%ACidc/](https://introspelliam.github.io/2017/09/18/tools/IDA%E7%9A%84%E8%B0%83%E8%AF%95%E8%84%9A%E6%9C%ACidc/)

在IDA中按下【shift + F2】可调出脚本编辑器

就IDApython的话,感觉比价火

但是,我喜欢C,IDC的参考指令可以说,巨少

[https://www.hex-rays.com/products/ida/support/idadoc/](https://www.hex-rays.com/products/ida/support/idadoc/)

# 数据类型

他们的数值比较都是有符号的,且一般为4字节比较(猜测的)

无符号比较需要去除符号位,比如&0xff的Byte

x86的IDC,,,0xffffffff==-1,但是0xffffffffffffffff≠-1

IDC中所有变量都被定义成auto类型，会自动进行类型转换，一般类型有整数型、字符串类型、浮点型

变量在没有赋予初始值的情况下,为0

- 局部变量：auto counter;
- extern 引入全局变量的声明，extern outsideGlobal;
- 字符串支持加好连接：auto str = "hello" + "world";
- 字符串支持分片操作：str1 = str[7:9];
- 没有strcat...等等函数

```
auto addr, reg, val;    //没有初始化声明的多个变量
auto count = 0;         //已声明和初始化
```

```
extern outsideGlobal;

static main()
{
    extern insideGlobal;
    outsideGlobal = "Global";
    insideGlobal = 1;
}
```

虽然IDC没有数组数据类型,但你可以使用分片运算符来处理IDC字符串,

就好像他们是数组一样,IDC分片的用法：

```
auto str = "String to slice";
auto s1, s2, s3, s4;
s1 = str[7:9];          //'to'
s2 = str[ :6];         //'String'
s3 = str[10: ];        //'slice'
s4 = str[5];               //'g'
```

# 字符串操作

```
if ( op == "jmp" || op == "call" )
{
...
}
```

```
#include <idc.idc>

static main()
{
    // 格式化字符串,类似于sprintf
    auto name = form("hello %s","lyshark");
    Message("格式化后的内容: %s \n",name);

    Message("十六进制转为整数: %d \n",xtol("0x41"));
    Message("十进制100转为八进制: %d \n",ltoa(100,8));
    Message("十进制100转换二进制: %d \n",ltoa(100,2));
    Message("字符A的ASCII: %d \n",ord("A"));
    Message("计算字符串长度: %d \n",strlen("hello lyshark"));

    // 在著字符串中寻找子串
    auto main = "hello lyshark";
    auto sub = "lyshark";
    Message("寻找子串: %d \n",strstr(main,sub));
}
```

# 数组

一个例子就可以搞懂

```
#include <idc.idc>

static main()
{
    // 创建数组元素
    auto ObjArr = CreateArray("array");
    // 获取数组指针
    auto lp_Arr = GetArrayId("array");

    Message("Arr: %X\n", lp_Arr);

    // 设置两个字符串变量
    SetArrayString(lp_Arr, 0, "hello");
    SetArrayString(lp_Arr, 1, "re4mile");

    // 设置两个整数变量
    SetArrayLong(lp_Arr, 2, 100);
    SetArrayLong(lp_Arr, 3, 200);

    // 如果提取字符串使用 AR_STR 标记 ，提取整数使用 AR_LONG
    auto sz1 = GetArrayElement(AR_STR, lp_Arr, 0);
    auto sz2 = GetArrayElement(AR_STR, lp_Arr, 1);
    Message("字符串: %s %s !\n", sz1, sz2);

    auto num1 = GetArrayElement(AR_LONG, lp_Arr, 2);
    auto num2 = GetArrayElement(AR_LONG, lp_Arr, 3);
    Message("整数: %d %d\n", num1,num2);

    // 删除数组的0号元素
    DelArrayElement(AR_STR, lp_Arr, 0);
    // 注销整个数组
    DeleteArray(lp_Arr);
}
```

# 运算符

许多标准的C语言操作符（+、-、*、/、%、<<、>>、++、--）包括三元运算符（?:)

在IDC同样适用，但复合赋值运算符+=不支持、逗号操作符也不被支持。

IDC几乎支持C中的所有运算和逻辑操作符，但是所有整数操作数均作为有符号的值处理。

这会影响到整数比较与右移位运算。如果需要进行逻辑右移位运算，你必须修改结果的最高位，自己移位，

如下代码：

result = ( x >> 1 ) & 0x7fffffff;   //将最大有效位设置为0

与C语言一样，IDC所有简单语句均以分号结束。

Switch语句是IDC唯一不支持的C风格复合语句。

在使用for语句时IDC不支持复合赋值运算符，如果你希望以除1以外的其他值为单位进行计数，就需要注意这一点，

如下代码：

```
auto i;
for (i = 0; i < 10; i += 2)
{

}       //不合法，不支持 +=
for (i = 0; i < 10; i = i + 2)
{

}    //合法
```

# 函数定义

定义一个函数

```
#include < idc>

// 定义一个函数
static OutPutAddress(My)
{
    auto tmp;
    tmp = 0x1300 + My;
    return tmp;
}

static main()
{
    auto ret = OutPutAddress(0x14);
    Message("%x \n",ret);
}
```

# 宏定义

BADADDR = -1

# API 手册

[https://www.hex-rays.com/products/ida/support/idadoc/162.shtml](https://www.hex-rays.com/products/ida/support/idadoc/162.shtml)

其实就是

![Untitled](%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3%2000f0fc98b7e949fbbbc0a3f932629dde/Untitled.png)

jmp 到当前位置+1

```
EB FF           jmp     short near ptr loc_1144+1
-------------------------------------------------------------
                dw 0BFC0h
                dq 0FFFEDFE800000068h, 65BFC0FFEBFFh, 0FFEBFFFFFED2E800h
                dq 0C5E80000006CBFC0h, 6CBFC0FFEBFFFFFEh, 0FFFFFEB8E8000000h
                dq 6FBFC0FFEBh, 0C0FFEBFFFFFEABE8h, 0FE9EE800000020BFh
                dq 77BFC0FFEBFFFFh, 0EBFFFFFE91E80000h, 0E80000006FBFC0FFh
```

他的特征代码是EB FF

EB是jmp FF是偏移

于是这种没有意义的跳转应该给nop掉

```
EB                                      db 0EBh
;---------------------------------------------------------------------------
FF C0                                   inc     eax
BF 68 00 00 00                          mov     edi, 68h ; 'h'
E8 DF FE FF FF                          call    _putchar
```

如果程序中有大量的这种花指令.那么你不可能手动的一个一个去nop掉

用脚本

```
#include < idc>
static main()
{
    auto x, target_str, ProcRange;
    target_str = "EB FF C0 BF";
    for (x = FindBinary(MinEA(), 0x03, target_str); x != BADADDR; x = FindBinary(x, 0x03, target_str))
    {
        PatchByte(x, 0x90);
    }
}
```

FindBinary(MinEA(), 0x03, target_str)的意思是?

从地址MinEA()处按0x03的模式遍历字节码target_str

MinEA()是最小的地址

PatchByte(x, 0x90);是把x指向的第一个字节给nop掉

# 数据读取修改

### PatchByte/Word/Dword

void PatchByte(long addr , long val)

设置虚拟地址addr处的一个字节值，

PatchByte可更换为

PatchWord，PatchDword

设置虚拟地址addr处的2字节和4字节值。

### Byte/Word/Dword/Qword

long Byte( long addr)，从虚拟地址 addr处读取一个字节值。

long word(long addr)，从虚拟地址addr处读取一个字（2字节）值。

1ong Dword(long addr)，从虚拟地址addr处读取一个双字（4字节)值。

### isLoaded

boo1 isLoaded(long addr)，如果addr包含有效数据，则返回1，否则返回0。

5）long atol（string val），将10进制val转化成对应整数值。

6）long xtol（string val），将16进制val转化成对应整数值。

7）long ord（string ch），返回单字符字符串ch的ASCII值。

8）string Name（long addr），返回与给定地址有关的名称，如果该位置没有名称，则返回空字符串。

# 用户交互函数

### Message

void Message(string format....)，

在输出窗口打印一条格式化消息。这个函数类似于C语言的printf函数，并接受printf风格的格式化字符串。

### print

void print( . ..)，

在输出窗口中打印每个参数的字符串表示形式。

### warning

void warning(string format. ...)，

在对话框中显示一条格式化消息。

### AskStr

string AskStr(string default, string prompt)，

显示一个输入框，要求用户输入一个字符串值。

如果操作成功，则返回用户的字符串;

如果对话框被取消，则返回0。

### AskFile

string AskFile(1ong doSave，string mask,string prompt)，

显示一个文件选择对话框，以简化选择文件的任务。

你可以创建新文件保存数据( doSave=1)，或选择现有的文件读取数据（ doSave=0)。

你可以根据mask （如* .*或*. idc)过滤显示的文件列表。

如果操作成功，则返回选定文件的名称;

如果对话框被取消,则返回O。

### AskYN

long AskYN( long default, string prompt)，

用一个答案为“是”或“否”的问题提示用户，

突出一个默认的答案(1为是，0为否，-1为取消)。

返回值是一个表示选定答案的整数。

### ScreenEA

long ScreenEA(),

返回当前光标所在位置的虚拟地址

```
#include < idc>

static main()
{
    auto CurrAddress = ScreenEA();
    //ScreenEA() 返回当前光标所在的虚拟地址
     Message("程序OEP => 0x%x \n",CurrAddress);
}
```

### Jump

boo1 Jump( 1ong addr)，跳转到反汇编窗口的指定地址。

因为IDC没有任何调试工具，你可能需要将Message 函数作为你的主要调试工具。

其他几个AskXXX函数用于处理更加专用的输人，如整数输人。请参考帮助系统文档了解可用的 AskXXX函数的完整列表。

如果希望创建一个根据光标位置调整其行为的脚本，这时，ScreenEA函数就非常有用，因为你可以通过它确定光标的当前位置。

同样，如果你的脚本需要将用户的注意力转移到反汇编代码清单中的某个位置，也需要用到Jump函数。

# 字符串操作函数

### form

string form(string format，...)

//preIDA5.6，返回一个新字符串，该字符串根据所提供的格式化字符串和值进行格式化。这个函数基本上等同于C语言的sprintf函数

### sprintf

string sprintf(string format . . . .)

//IDA5.6+，在 IDA5.6中，sprintf用于替代form(参见上面)。

### atol

1ong ato1(string va1)，将十进制值va1转换成对应的整数值。

### xtol

1ong xtol(string val)，将十六进制值val(可选择以0x开头）转换成对应的整数值。

Message("十六进制转为整数: %d \n",xtol("0x41"))

### ltoa

string ltoa(1ong va1，1ong radix)，

以指定的radix (2、8、10或16)返回va1的字符串值。

Message("十进制100转为八进制: %d \n",ltoa(100,8));

### ord

long ord(string ch)，返回单字符字符串ch 的ASCI值。

Message("字符A的ASCII: %d \n",ord("A"));

### strlen

long strlen(string str)，返回所提供字符串的长度。

Message("计算字符串长度: %d \n",strlen("hello re4mile"));

### strstr

long strstr(string str. string substr)，

返回str中 substr 的索引。

如果没有发现子字符串，则返回-1。

类似于python的语法 if "dqx" in "I am dqx"

```
if(strstr(op,"push    esi")==0)
{
    ...
    }
其实他就是一个strcmp的作用,如果返回0,说明字符串刚好匹配
```

### substr

string substr(string str. long start.1ong end)，

返回包含 str 中由start到end-1位置的字符的子字符串。

如果使用分片（IDA5.6及更高版本)，此函数等同于str[start:end]。如前所述，IDC中没有任何字符数据类型，它也不支持任何数组语法。

如果你想要遍历字符串的每个字符，必须把字符串中的每个字符当成连续的单字符子字符串处理。

# 文件操作

输出窗口并不总是显示脚本输出的理想位置

对于生成大量文本或二进制数据的脚本，你可能希望将其结果输出到磁盘文件上。

我们已经讨论了如何使用AskFi1e函数要求用户输入文件名。

但是，AskFi1e仅返回一个包含文件名的字符串值。

IDC的文件处理函数如下所示。

### fopen

long fopen(string filename，string mode)

返回一个整数文件句柄（如果发生错误，则返回0)

供所有IDC文件输入/输出函数使用

mode参数与C语言的fopen 函数使用的模式( r表示读取，w表示写入，等等）类似

### fclose

void fclose(long hand1e)

关闭fopen中文件句柄指定的文件。

### filelength

long filelength(long handle)

返回指定文件的长度，

如果发生错误，则返回-1。

### fgetc

1ong fgetc(long handle)，从给定文件中读取一个字节

如果发生错误，则返回-1。

### fputc

long fputc(long val. long handle)，写入一个字节到给定文件中

如果操作成功，则返回0;

如果发生错误，则返回-1。

### fprintf

long fprintf(1ong handle, string format，...)

将一个格式化字符串写入到给定文件中。

### writestr

long writestr(long handle. string str)，将指定的字符串写入到给定文件中。

### readstr

string/long readstr(1ong handle)，从给定文件中读取一个字符串

这个函数读取到下一个换行符为止的所有字符（包括非ASCII字符)，包括换行符本身(ASCII OxA )。

如果操作成功，则返回字符串;

如果读取到文件结尾，则返回-1。

### writelong

long writelong(long handle. long va1， long bigendian)

使用大端(bigendian-1)或小端( bigendian=0)字节顺序将一个4字节整数写入到给定文件。

### readlong

long readlong( long handle,long bigendian)

使用大端(bigendian=1)

或小端( bigendian=-Q)字节顺序从给定的文件中读取一个4字节整数。

### writeshort

long writeshort(long handle，long va1,long bigendian)

使用大端( bigendian=1)或小端( bigendian=0)字节顺序将一个2字节整数写入到给定的文件。

### readshort

long readshort( 1ong handle,long bigendian)

使用大端(bigendian-1)或小端( bigendian=0)字节顺序从给定的文件中读取一个2字节整数。

### loadfile

bool loadfile(long handle ,long pos，long addr. long length)

从给定文件的pos位置读取length数量的字节，并将这些字节写入到以addr地址开头的数据库中。

### savefile

bool savefile(long handle，1ong pos., long addr. long length)

将以addr数据库地址开头的length数量的字节写入给定文件的pos位置。

eg

```c
#include <idc.idc>

static getFuncName(ea)
{
    auto funcName = get_func_name(ea);

    auto dm = demangle_name(funcName, get_inf_attr(INF_LONG_DN));
    if (dm != 0)
    {
        funcName = dm;
    }
    return funcName;
}

static functionDump(ip_CurFuncStart)
{
    auto funcName = 0;
    auto ip_CurFuncEnd = 0x0;
    auto ip_NextFuncStart;
    auto sz_FileName = get_idb_path()[0:-4] + "_dump.txt";
    auto fp = fopen(sz_FileName, "w");
    auto appendData = 0;

    while (ip_CurFuncStart != BADADDR)
    {
        ip_CurFuncStart     = NextFunction(ip_CurFuncStart);
        ip_CurFuncEnd       = FindFuncEnd(ip_CurFuncStart);
        ip_NextFuncStart    = NextFunction(ip_CurFuncStart);
        funcName            = getFuncName(ip_CurFuncStart);

        if (ip_NextFuncStart == BADADDR)
        {
            fprintf(fp, "0x%08X --> 0x%08X %s\n", ip_CurFuncStart, ip_CurFuncEnd, funcName);
            ip_CurFuncStart = ip_NextFuncStart;
            continue;
        }
        appendData = ip_NextFuncStart - ip_CurFuncEnd;
       // ip_CurFuncEnd = ip_NextFuncStart - 1;//他们之间的差别不仅仅是1,因为会有字节的填充
        fprintf(fp, "0x%08X --> 0x%08X + 0x%08X %s\n", ip_CurFuncStart, ip_CurFuncEnd, appendData,funcName);
    }
    fclose(fp);
}

static main()
{
    Message("Start\n");
    functionDump(0x00040000);
    Message("End\n");
}
```

# 操作数据库名称

在脚本中，你经常需要操纵已命名的位置。下面的IDC函数用于处理IDA数据库中已命名的位置。

### Name

string Name(1ong addr)，

返回与给定地址有关的名称，

如果该位置没有名称，则返回空字符串。

如果名称被标记为局部名称，这个函数并不返回用户定义的名称。

### NameEx

string NameEx(long from，long addr)，返回与addr有关的名称。如果该位置没有名称，则返回空字符串。

如果 from是一个同样包含addr的函数中的地址，则这个函数返回用户定义的局部名称。

### MakeNameEx

bool MakeNameEx(1ong addr. string name. long flags)，

将给定的名称分配给给定的地址。该名称使用flags位掩码中指定的属性创建而成。

这些标志在帮助系统中的MakeNameEx文档中有记载描述，

可用于指定各种属性，如名称是局部名称还是公共名称、名称是否应在名称窗口中列出

### LocByName

long LocByName(string name)，返回一个位置（名称已给定）的地址。如果数据库中没有这个名称，则返回BADADDR ( -1 )。

### LocByNameEx

long LocByNameEx(long funcaddr， string loca 1name)，在包含funcaddr的函数中搜索给定的局部名称。如果给定的函数中没有这个名称，则返回BADADDR ( -1 )o

# 操作数据库的函数

有大量函数可用于对数据库的内容进行格式化。这些函数如下所示。

### MakeUnkn

void MakeUnkn(long addr. long flags)，

取消位于指定地址的项的定义。

这里的标志(参见IDC的MakeUnkn文档）指出是否也取消随后的项的定义

以及是否删除任何与取消定义的项有关的名称。

相关函数MakeUnknown 允许你取消大块数据的定义。

### MakeCode

long MakeCode(1ong addr)，

将位于指定地址的字节转换成一条指令。

如果操作成功，则返回指令的长度，

否则返回0。

### MakeByte

bool MakeByte(long addr)，

将位于指定地址的项目转换成一个数据字节。

类似的函数还包括Makeword和 MakeDword。

### MakeComm

boo1 MakeComm(long addr. string comment)，

在给定的地址处添加一条常规注释。

### MakeFunction

bool MakeFunction(long begin，long end)，

将由begin到end 的指令转换成一个函数。如果end被指定为BADADDR ( -1)，IDA会尝试通过定位函数的返回指令，来自动确定该函数的结束地址。

开始的地址,比如说push esi

结束的地址, retn那个地址不是结束,retn之外那个地址,才是,结束的地址不属于函数地址,是函数地址的边界

```
#include <idc.idc>
static Y_MakeFunction(IP_start,IP_end)
{
    auto tmp=0;//先从开始的IP取消定义,然后再生成函数
    tmp=MakeFunction(IP_start,IP_end);
    if(tmp==1)
    {
        Message("make func ok\n");
    }
    else
    {
        Message("make func failed\n");
    }
}
static main(void)
{

    Message("work begin\n");

    Y_MakeFunction(0x0040A188,0x0040A1AA);

    Message("work done\n");
}
```

运行输出

```
work begin
make func ok
work done
```

### MakeStr

bool MakeStr(1ong begin，long end)，

创建一个当前字符串(由GetStringType返回)类型的字符串,

涵盖由begin到end-1之间的所有字节。

如果end被指定为BADADDR,IDA会尝试自动确定字符串的结束位置。

# 数据库搜索函数

在IDC中，IDA的绝大部分搜索功能可通过各种FindXXX函数来实现，下面我们将介绍其中一些函数。FindXXX函数中的flags参数是一个位掩码，可用于指定查找操作的行为。3个最为常用的标志分别为SEARCH_DOWN，它指示搜索操作扫描高位地址;SEARCH_NEXT，它略过当前匹配项，以搜索下一个匹配项;SEARCH_CASE，它以区分大小写的方式进行二进制和文本搜索。

### FindCode

long FindCode(long addr, long flags)，

从给定的地址搜索一条指令的地址

### FindData

long FindData(long addr.long flags)，从给定的地址搜索一个数据项。

### FindBinary

long FindBinary(long addr，long flags，string binary)

从给定的地址addr搜索16进制字符串序列binary

返回该字节码出现的地址

```
flag取值有：可选项
SEARCH_DOWN 向下搜索
SEARCH_UP 向上搜索
SEARCH_NEXT 获取下一个找到的对象。
SEARCH_CASE 指定大小写敏感度
SEARCH_UNICODE 搜索 Unicode 字符串。
```

### FindText

long FindText(long addr.long flags.1ong row.long column，string text)，

在给定的地址，从给定行( row)的给定列搜索字符串text。注意，某个给定地址的反汇编文本.可能会跨越几行，因此,你需要指定搜索应从哪一行开始。还要注意的是，SEARCH_NEXT并未定义搜索的方向，根据SEARCH_DOWN 标志，其方向可能向上也可能向下。此外，如果没有设置SEARCH_NEXT，且 addr位置的项与搜索条件匹配，则FindXXX函数很可能会返回addr参数传递给该函数的地址。

# 操作函数

许多脚本专用于分析数据库中的函数。

IDA为经过反汇编的函数分配大量属性，如函数局部变量区域的大小、函数的参数在运行时栈上的大小。

下面的IDC函数可用于访问与数据库中的

### GetFunctionAttr

long GetFunctionAttr(long addr, 1ong attrib)，

返回包含给定地址的函数的被请求的属性

例如，要查找一个函数的结束地址，可以使用GetFunctionAttr(addr. FUNCATTR_END)

```
funcStart = GetFunctionAttr(origEA,FUNCATTR_START);
funcEnd = GetFunctionAttr(origEA,FUNCATTR_END)
```

### GetFunctionName

string GetFunctionName(long addr)

参数是一个指令的地址

返回当前指令属于哪个函数

如果给定的地址并不属于一个函数，则返回一个空格字符串" "

### NextFunction

auto NextFunction(auto addr)，

返回给定地址后的下一个函数的起始地址。

如果数据库中给定地址后没有其他函数，则返回-1。

### PrevFunction

1ong PrevFunction(1ong addr)，

返回给定地址之前距离最近的函数的起始地址。

如果在给定地址之前没有函数，则返回-1。

根据函数的名称，使用LocByName函数查找该函数的起始地址。

# 代码交叉引用函数

### Rfirst

long Rfirst(long from)，

返回给定地址向其转交控制权的第--个位置。

如果给定的地址没有引用其他地址，则返回BADADDR ( -1 )

### Rnext

long Rnext(1ong from，long current)，

如果current 已经在前一次调用Rfirst或Rnext时返回,

则返回给定地址( from )转交控制权的下一个位置。

如果没有其他交叉引用存在，则返回BADADDR。

### XrefType

long XrefType()，

返回-个常量，说明某个交叉引用查询函数（如Rfirst)

返回的最后一个交叉引用的类型。对于代码交叉引用，这些常量包括fl_CN(近调用)、fl_CF(远调用)、f1_JN（近跳转)、f1_JF（远跳转）和f1_F(普通顺序流)。

### RfirstB

long RfirstB(long to)，

返回 转交控制权到给定地址的第一个位置。

如果不存在对给定地址的交叉引用，则返回BADADDR( -1 )。

### RnextB

long RnextB(1ong to. long current)，

如果current 已经在前一次调用RfirstB或RnextB时返回，则返回下一个转交控制权到给定地址(to)的位置。

如果不存在其他对给定位置的交叉引用，则返回BADADDR ( -1 ).

每次调用一个交叉引用函数，

IDA都会设置一个内部 IDC状态变量,指出返回的最后一个交叉引用的类型。如果需要知道你收到的交叉引用的类型,那么在调用其他交叉引用查询函数之前，必须调用XrefType函数。

# 数据交叉引用

访问数据交叉引用信息的函数与访问代码交叉引用信息的函数非常类似。这些函数如下所示。

### Dfirst

long Dfirst(long from)，

返回给定地址引用一个数据值的第--个位置。

如果给定地址没有引用其他地址，则返回BADADDR ( -1 )。

### Dnext

long Dnext(1ong from，long current)

如果current已经在前--次调用Dfirst或Dnext时返回，则返回给定地址( from )

向其引用一个数据值的下一个位置。

如果没有其他交叉引用存在，则返回BADADDR。

### XrefType()

long XrefType()，返回一个常量，说明某个交叉引用查询函数（如 Dfirst)返回的最后一个交叉引用的类型。

对于数据交叉引用，这些常量包括dr_0(提供的偏移量)、dr_w(数据写人）和dr_R（数据读取)

### DfirstB

long DfirstB(1ong to)

返回将给定地址作为数据引用的第一个位置。

如果不存在引用给定地址的交叉引用，则返回BADADDR ( -1 )

### DnextB

long DnextB(long to，1ong current)，如果currnet 已经在前一次调用DfristB或DnextB时返回，则返回将给定地址( to)作为数据引用的下一次位置。如果没有其他对给定地址的交叉引用存在，则返回BADADDR。和代码交叉引用一样，如果需要知道你收到的交叉引用的类型，那么在调用另一个交叉引用查询函数之前，必须调用XrefType函数

# 反汇编提取

许多时候，我们需要从反汇编代码清单的反汇编行中提取出文本或文本的某个部分。下面的函数可用于访问反汇编行的各种组件

## GetDisasm

string GetDisasm(long addr)，返回给定地址的反汇编文本。返回的文本包括任何注释，但不包括地址信息

返回该地址的反汇编指令

```
#include <idc.idc>

static main()
{
    auto currAddr=0;
    auto op =" ";
    currAddr    = ScreenEA();
    op=GetDisasm(currAddr);
    Message("%s\n",op);
}
```

输出

`mov     edx, dword_445BD8`

注意返回的字符串,mov和edx之间是4个空格

## GetMnem

string GetMnem( auto addr)

返回位于给定地址的汇编指令,比如返回"call","jmp"

如果该地址没有指令与之匹配就返回" "

## GetOpnd

string GetOpnd(long addr. long opnum)，

返回指定地址汇编指令的的操作数

IDA以0为起始编号，从左向右对操作数编号。

## GetOpType

long GetOpType(long addr.long opnum)，返回一个整数，指出给定地址的给定操作数的类型。请参考GetOpType的 IDC文档，了解操作数类型代码。

## GetOperandValue

long GetOperandValue(long addr. long opnum)，返回与给定地址的给定操作数有关的整数值。返回值的性质取决于GetOpType指定的给定操作数的类型。15.5 IDC脚本示例211string CommentEx(long addr. long type)，返回给定地址处的注释文本。如果type为0,则返回常规注释的文本;如果type为1，则返回可重复注释的文本。如果给定地址处没有注释,则返回一个空字符串。

## ItemSize

返回汇编指令的长度

```
ItemSize(给定地址)
```

```
.text:00000000004018B6 8B 04 25 54 30 60 00          mov     eax, ds:zero2
```

如果addr是00000000004018B6,则函数返回7

如果addr是00000000004018B7,则函数返回6

...以此类推

## GetRegValue("RIP")

GetRegValue("RIP")

就这样就可以获取某个寄存器的值

## get_func_name

获取对应地址所在函数的名字

```c
auto funcName = get_func_name(start_func_addr);
```

# misc-func

MinEA() MaxEA() 获取当前idb 的最小地址 和 最大地址

ScreenEA() 获取当前光标所在行的地址, 返回一个 int 类型

SegName(ea) ea是一个变量存储当前地址, 这个api 是获取当前地址所在的段

GetDisasm(ea) 获取当前地址的反汇编代码

GetMnem(ea) 获取当前地址的操作码

GetOpnd(ea,0) 获取当前地址的操作数,第二个参数表示哪一个操作数

SegStart(ea) 获取当前地址所在段的起始地址

SegEnd(ea) 获取当前地址的段尾地址

NextSeg(ea) 获取下一个段的起始地址

idautils.Segments() 返回一个可迭代的对象数组

GetFunctionName(func) 通过地址,获取函数的名称

idautils.Functions() 返回一个可迭代的函数首地址数组,

idaapi.get_func(ea) 获取当前地址的函数首地址和尾地址

NextFunction(ea) 获取下一个函数地址,ea的值可能在函数里面,也可能在函数外面,但是会返回下一个函数的首地址

PrevFunction(ea) 获取前一个函数地址

GetFunctionAttr(ea,FUNCATTR_START) 获取一个函数的边界地址

GetDunctionAttr(ea,FUNCATTR_END) 获取一个函数的边界地址

NextHead

```
auto NextHead(auto 当前地址,auto 结尾地址)
//head = NextHead(startOEP, End_FUnc);
//head = NextHead(0x00000000, 0xFFFFFFFF);
```

获取一个当前指令的下一个指令的地址,遍历结束返回-1

函数的不足是:

如果遇到花指令,比如

```
A1AA F9                                                                       stc
CAT1:0040A1AB 72 03                                                           jb      short loc_40A1B0
CAT1:0040A1AD                                                                 db      64h
CAT1:0040A1AD 64 E3 8F                                                        jecxz   short loc_40A13F
```

他是不会返回db 64h的地址的

SetColor

SetColor(auto 地址, CIC_ITEM,  16进制颜色值);

get_idb_path()[0:-4]

```
#include <idc.idc>
static main(void)
{
    Message("%s\n",get_idb_path()[0:-4]);
}
//输出当前文件所在目录,具体是当前idb文件所在目录
```

# 附录

一个很好的IDA资源插件介绍,没去下载应用

[https://www.dazhuanlan.com/sisiyoki/topics/1183415](https://www.dazhuanlan.com/sisiyoki/topics/1183415)