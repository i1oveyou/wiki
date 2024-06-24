---
title: wiki-Reverse-Android-apk文件生成-tmp
---




读取apk结构内容的代码

```java
private void verifyLibs() {
    this.crc = new HashMap();
    this.crc.put("armeabi-v7a", Long.valueOf(Long.parseLong(getResources().getString(owasp.mstg.uncrackable3.R.string.armeabi_v7a))));
    this.crc.put("arm64-v8a", Long.valueOf(Long.parseLong(getResources().getString(owasp.mstg.uncrackable3.R.string.arm64_v8a))));
    this.crc.put("x86", Long.valueOf(Long.parseLong(getResources().getString(owasp.mstg.uncrackable3.R.string.x86))));
    this.crc.put("x86_64", Long.valueOf(Long.parseLong(getResources().getString(owasp.mstg.uncrackable3.R.string.x86_64))));
    try {
        ZipFile apk_file = new ZipFile(getPackageCodePath());
        for (Map.Entry<String, Long> i_mem_info : this.crc.entrySet()) {
            String apkMem_path = "lib/" + i_mem_info.getKey() + "/libfoo.so";
            ZipEntry apkMem_file = apk_file.getEntry(apkMem_path);
            Log.v(TAG, "CRC[" + apkMem_path + "] = " + apkMem_file.getCrc());
            if (apkMem_file.getCrc() != i_mem_info.getValue().longValue()) {
                tampered = 31337;
                Log.v(TAG, apkMem_path + ": Invalid checksum = " + apkMem_file.getCrc() + ", supposed to be " + i_mem_info.getValue());
            }
        }
        ZipEntry entry = apk_file.getEntry("classes.dex");
        Log.v(TAG, "CRC[classes.dex] = " + entry.getCrc());
        if (entry.getCrc() != baz()) {
            tampered = 31337;
            Log.v(TAG, "classes.dex: crc = " + entry.getCrc() + ", supposed to be " + baz());
        }
    } catch (IOException unused) {
        Log.v(TAG, "Exception");
        System.exit(0);
    }
}

```

