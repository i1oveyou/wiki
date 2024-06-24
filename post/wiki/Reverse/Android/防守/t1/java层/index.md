---
title: wiki-Reverse-Android-防守-t1-java层
---
# root检测

1）。

```java
public static boolean a() {
    for (String str : System.getenv("PATH").split(":")) {
        if (new File(str, "su").exists()) {
            return true;
        }
    }
    return false;
}
```

从环境变量中检测有没有 `su`存在,如果存在说明手机可以root



2），

检测` Build.TAGS`

```java
    public static boolean b() {
        String str = Build.TAGS;
        return str != null && str.contains("test-keys");
    }

```



3），

检测下面这些敏感目录或者文件

```java
   public static boolean c() {
        for (String str : new String[]{"/system/app/Superuser.apk", "/system/xbin/daemonsu", "/system/etc/init.d/99SuperSUDaemon", "/system/bin/.ext/.su", "/system/etc/.has_su_daemon", "/system/etc/.installed_su_daemon", "/dev/com.koushikdutta.superuser.daemon/"}) {
            if (new File(str).exists()) {
                return true;
            }
        }
        return false;
    }

```





```
"/system/app/Superuser.apk", 
"/system/xbin/daemonsu",
"/system/etc/init.d/99SuperSUDaemon", 
"/system/bin/.ext/.su", 
"/system/etc/.has_su_daemon", 
"/system/etc/.installed_su_daemon", 
"/dev/com.koushikdutta.superuser.daemon/"
```



# debuging检测

1）， 

```java
public static boolean a(Context context) {
    return (context.getApplicationContext().getApplicationInfo().flags & 2) != 0;
}
//传入参数 getApplicationContext()
```

2） ,

```java
    new AsyncTask<Void, String, String>() { // from class: sg.vantagepoint.uncrackable2.MainActivity.2
        /* JADX INFO: Access modifiers changed from: protected */
        @Override // android.os.AsyncTask
        /* renamed from: a  reason: avoid collision after fix types in other method */
        public String doInBackground(Void... voidArr) {
            while (!Debug.isDebuggerConnected()) {
                SystemClock.sleep(100L);
            }
            return null;
        }

        /* JADX INFO: Access modifiers changed from: protected */
        @Override // android.os.AsyncTask
        /* renamed from: a  reason: avoid collision after fix types in other method */
        public void onPostExecute(String str) {
            MainActivity.this.exit_dialog("Debugger detected!");
        }
    }.execute(null, null, null);
```
