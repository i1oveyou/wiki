



关闭三个保护机制：Canary栈溢出保护、栈不可执行、PIE溢出保护（对程序的内存布局随机化），生成64位ELF

```
gcc -g vuln.c -o vuln -fno-stack-protector -z execstack -no-pie
```

