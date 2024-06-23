

# link

https://yasm.tortall.net/Download.html



```assembly
bits 32
extern _MessageBoxA@16:proc
extern _ExitProcess@4:proc

.data
msg_title db "Demo!", 0
msg_content db "Hello World!", 0

global main

main:
    push 0
    push 0
    push msg_title
    push msg_content
    push 0
    call _MessageBoxA@16
    push 0
    call _ExitProcess@4
```



```
yasm-1.3.0-win32.exe -f win32 demo.asm -o demo32.obj
```



```
link.exe demo.obj /subsystem:console /defaultlib:kernel32.lib /defaultlib:user32.lib /entry:main /out:demo32_masm.exe
```

