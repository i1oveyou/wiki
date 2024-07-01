



https://enovella.github.io/android/reverse/2020/09/03/r2pay-android-crackmes-radare2con.html

res:

https://www.youtube.com/watch?v=M0ETKs6DZn8



- Java root checks
- Java obfuscation
- Obfuscated Whitebox cryptography
- Manual code obfuscation though conditional tricks
- Native root checks
- Native anti-debugging
- Native inline assembly syscalls
- Native code integrity checks
- Native memory checksumming
- Native anti-DBI (Dynamic Binary Instrumentation)
- Native obfuscation
- Runtime Application Self-Protection (RASP)





 Frida 可能存在 UTF-16 编码问题

这可能是由于其中一个函数使用音符 (♫) 作为名称所致



```java
C0282 rb = new C0282(getApplicationContext());
if (rb.m1161() || (rb.m1154() && rb.m1149())) {
    int i = 1337 / 0;
    this.f508 = (byte) (this.f508 | 15);
}
```

去hook getApplicationContext() ,返回其它包名的contex



扫描各个目录以确定是否存在名为“su”的程序。

```java
public boolean m1155(String filename) {
    String[] pathsArray = C0272.m1134();
    boolean result = false;
    for (String path : pathsArray) {
        String completePath = path + filename;
        File f = new File(path, filename);
        boolean fileExists = f.exists();
        //我们可以通过挂接/重载 java 的“exists();”来轻松绕过此检查。并将返回值设置为 false
        if (fileExists) {
            C0288.m1179(completePath + " binary detected!");
            result = true;
        }
    }
    return result;
}
```



当应用程序尝试打开任何 su 文件时，我们还需要覆盖该参数，

方法是在我们从 libc.so 中挂钩“open”时替换它的参数。



```java
    public final String[] m1153() {
        try {
            InputStream inputstream = Runtime.getRuntime().exec("getprop").getInputStream();
            // exec 传递另外一个参数
            if (inputstream == null) {
                return null;
            }
            String propVal = new Scanner(inputstream).useDelimiter("\\A").next();
            return propVal.split("\n");
        } catch (IOException | NoSuchElementException e) {
            C0288.m1182(e);
            return null;
        }
    }

```





```java
   public boolean m1160() {
        String buildTags = Build.TAGS;
        return buildTags != null && buildTags.contains("test-keys");
       // hook String.contains("test-keys")
    }

```

