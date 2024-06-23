# DEP

DEP保护机制，用于限制某些内存页不具有可执行权限

### **如何绕过DEP**

`VirtualProtect`这个API能够更改内存页的属性为可执行或不可执行，对于二进制漏洞利用来说，

溢出的时候，把返回地址设计为`VirtualProtect`的地址，再精心构造一个栈为调用这个API的栈，

就可以改变当前栈的内存页的属性，使其从"不可执行"变成"可执行"。



`VirtualProtect`这个API能够更改内存页的属性为可执行或不可执行，对于二进制漏洞利用来说，

溢出的时候，把返回地址设计为`VirtualProtect`的地址，再精心构造一个栈为调用这个API的栈，

就可以改变当前栈的内存页的属性，使其从"不可执行"变成"可执

```c
#include <stdio.h>
#include <Windows.h>
int main()
{
	char shellcode[] = "123";
	HANDLE hHep = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE | HEAP_ZERO_MEMORY, 0, 0);
	PVOID Mptr = HeapAlloc(hHep, 0, sizeof(shellcode));
	RtlCopyMemory(Mptr, shellcode, sizeof(shellcode));
	DWORD dwThreadId = 0;
	HANDLE hThread = CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)Mptr, NULL, NULL, &dwThreadId);
	WaitForSingleObject(hThread, INFINITE);
	printf( "Hello World!\n");
}
```

