---
title: wiki-Reverse-winRe-PE-应用篇-脱PE壳-3.小结篇
---
一般而言，脱壳的基本步骤如下：

1：寻找OEP（注意：OEP指的是程序原始入口点，不是壳的入口点，英文全称是（original entry point)

2：转储，也就是dump

3:  修复IAT 

4：检查目标程序是否存在AntiDump等阻止程序被转储的保护措施，并修复