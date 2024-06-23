





# java

检测当前手机有没有安装一些软件,比如magisk

```java
    public final boolean f11(List<String> packages) {
        boolean result = false;
        PackageManager pm = this.env_ctx.getPackageManager();
        for (String packageName : packages) {
            try {
                pm.getPackageInfo(packageName, 0);//查看有没有安装,没有就抛出异常
                b.a.a.c.a.a(packageName + " ROOT management app detected!");
                result = true;
            }
            catch (PackageManager.NameNotFoundException e) {
                Log.d("dqx","nth");
            }
        }
        return result;
    }

```





在所有环境变量中,检测有没有su

```java
    public boolean f3("su") {
        String[] pathsArray = res_Class.a();
        boolean result = false;
        for (String path : pathsArray) {
            String completePath = path + filename;
            File f = new File(path, filename);
            boolean fileExists = f.exists();
            if (fileExists) {
                b.a.a.c.a.b(completePath + " binary detected!");
                result = true;
            }
        }
        return result;
    }
```





"getprop"环境检测

```
    public boolean f4() {
        Map<String, String> dangerousProps = new HashMap<>();
        dangerousProps.put("ro.debuggable", "1");
        dangerousProps.put("ro.secure", "0");
        boolean result = false;
        String[] lines = m511b();
        if (lines == null) {
            return false;
        }
        for (String line : lines) {
            for (String key : dangerousProps.keySet()) {
                if (line.contains(key)) {
                    String badValue = "[" + dangerousProps.get(key) + "]";
                    if (line.contains(badValue)) {
                        b.a.a.c.a.b(key + " = " + badValue + " detected!");
                        result = true;
                    }
                }
            }
        }
        return result;
    }
```





输出指令,然后检查结果 `which su`

```
    public boolean f7() {
        Process process = null;
        try {
            process = Runtime.getRuntime().exec(new String[]{"which", "su"});
            BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
            boolean z = in.readLine() != null;
            process.destroy();
            return z;
        } catch (Throwable th) {
            if (process != null) {
                process.destroy();
            }
            return false;
        }
    }
```



# so

我怀疑它so的函数也做了混淆

