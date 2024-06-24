---
title: wiki-pwn-winPwn-内存保护机制-写在前面
---
# 内存保护机制

links

```cpp
https://tearorca.github.io/Linux%E5%92%8CWindows%E4%BF%9D%E6%8A%A4%E6%9C%BA%E5%88%B6/
https://introspelliam.github.io/categories/%E5%AE%89%E5%85%A8%E6%8A%80%E6%9C%AF/
```

 

当入门winPwn的时候,就发现

```
$ check .\d1.exe
Warn: undersized load config, probably missing fields
Results for: .\d1.exe
Dynamic Base    : "Present"
ASLR            : "Present"
High Entropy VA : "NotPresent"
Force Integrity : "NotPresent"
Isolation       : "Present"
NX              : "Present"
SEH             : "Present"
CFG             : "NotPresent"
RFG             : "NotPresent"
SafeSEH         : "NotPresent"
GS              : "Present"
Authenticode    : "NotPresent"
.NET            : "NotPresent"
```

其实有这么多的保护