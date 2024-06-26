---
title: wiki-Reverse-winRe-PE-数据目录表-04.属性证书数据表
---
[04] 属性证书数据表

类似于PE文件的校验或者MD5值

```
addr: 它的值是FA,不会映射到内存
size:
```



exe的数字签名是什么?

数字签名是用于验证软件或文件的身份和完整性的一种安全机制。在Windows操作系统中，可执行文件（.exe）的数字签名通常使用数字证书来实现。

数字签名的过程大致如下：

1. 开发者使用算法对文件计算获取一个hash值
2. 开发者将hash值使用自己的私钥加密，生成数字签名。
3. 开发者将软件、数字签名和开发者公钥打包发布。

在用户下载或运行该软件时，系统会执行以下步骤来验证数字签名：

1. 系统获取软件内的数字签名信息。
2. 系统通过开发者公钥解密数字签名，得到解密后的摘要值。
3. 系统再次对软件进行哈希处理，得到一个当前计算的hash值
4. 系统比较解密后的hash值和当前计算的hash值是否一致。
5. 如果两个摘要值一致，说明该软件是由开发者签名的，且没有被篡改；否则，说明软件可能被篡改，或者并非由该开发者签名。



数字签名可以确保软件的完整性和来源可信性。用户在执行数字签名验证后，可以信任该软件是由特定开发者发布，

并且未被篡改过。这有助于防止恶意软件的传播和保护用户的计算机安全。



exe的数字签名存放在哪里?

具体来说，数字签名信息存放在PE头的"证书表"（Certificate Table）中。

该表位于可执行文件的数据目录中的`IMAGE_DIRECTORY_ENTRY_SECURITY`项处。

证书表中包含了签名算法、证书链、签名时间等与数字签名相关的信息。

这些数字签名信息可以通过一些工具和API来访问和验证，

例如Windows操作系统自带的"属性"对话框、PowerShell命令、SignTool工具以及Cryptographic API函数等。

需要注意的是，数字签名并不会直接影响可执行文件本身的功能和行为，它仅用于验证文件的来源和完整性。

因此，即使可执行文件的数字签名被篡改或删除，文件本身仍然可以正常运行，但可能会导致无法通过数字签名验证。

