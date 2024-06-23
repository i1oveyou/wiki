



```c
#include    <stdio.h>

void foo() {
        (void) printf("initializing: foo()\n");
}

void bar() {
        (void) printf("finalizing: bar()\n");
}

int main() {
        (void) printf("main()\n");
        return (0);
}
```



```
$ cc -o main -zinitarray=foo -zfiniarray=bar main.c
$ ./main
initializing: foo()
main()
finalizing: bar()
```





直接编译,不需要加编译选项

```c
#include <stdio.h>
 
__attribute((constructor)) void before_main()
{
    printf("%s\n", "I Can Before Main");
}
 
__attribute((destructor)) void after_main()
{
    printf("%s\n", "I Can Aftrer Main");
}
 
int main(int argc, char **argv)
{
    printf("%s\n", "I Am Main");
    return 0;
}
```





```
__int64 __fastcall sub_7FEFAF7CD360(
        __int64 a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8)
{
  __int64 (__fastcall *v8)(void *, void *, __int64 (__fastcall *)(__int64, __int64, __int64, __int64, __int64, __int64, char)); // r12
  void *v9; // rdi
  void *retaddr; // [rsp+0h] [rbp+0h] BYREF

  v8 = (__int64 (__fastcall *)(void *, void *, __int64 (__fastcall *)(__int64, __int64, __int64, __int64, __int64, __int64, char)))sub_7FEFAF7CDF40(&retaddr);
  v9 = rtld_global;
  dl_init(rtld_global, retaddr, &a7, &a8 + (_QWORD)retaddr);
  return v8(v9, retaddr, dl_fini);
}
```





```
ld_linux_x86_64.so.2:00007FEFAF7CD360 sub_7FEFAF7CD360 proc near
ld_linux_x86_64.so.2:00007FEFAF7CD360 mov     rdi, rsp
ld_linux_x86_64.so.2:00007FEFAF7CD363 call    sub_7FEFAF7CDF40
ld_linux_x86_64.so.2:00007FEFAF7CD368 mov     r12, rax
ld_linux_x86_64.so.2:00007FEFAF7CD36B mov     rdx, [rsp+0]
ld_linux_x86_64.so.2:00007FEFAF7CD36F mov     rsi, rdx
ld_linux_x86_64.so.2:00007FEFAF7CD372 mov     r13, rsp
ld_linux_x86_64.so.2:00007FEFAF7CD375 and     rsp, 0FFFFFFFFFFFFFFF0h
ld_linux_x86_64.so.2:00007FEFAF7CD379 mov     rdi, cs:_rtld_global
ld_linux_x86_64.so.2:00007FEFAF7CD380 lea     rcx, [r13+rdx*8+10h]
ld_linux_x86_64.so.2:00007FEFAF7CD385 lea     rdx, [r13+8]
ld_linux_x86_64.so.2:00007FEFAF7CD389 xor     ebp, ebp
ld_linux_x86_64.so.2:00007FEFAF7CD38B call    _dl_init
ld_linux_x86_64.so.2:00007FEFAF7CD390 lea     rdx, _dl_fini
ld_linux_x86_64.so.2:00007FEFAF7CD397 mov     rsp, r13
ld_linux_x86_64.so.2:00007FEFAF7CD39A jmp     r12
ld_linux_x86_64.so.2:00007FEFAF7CD39A sub_7FEFAF7CD360 endp
```

