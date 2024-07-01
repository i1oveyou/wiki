---
title: "env-win10"
---



# vscode



## cmder_shell

配置默认启动终端

准备工作: 

下载了cmder

添加了环境变量 cmder_root

```
        "Cmder": {
            "name": "Cmder",
            "path": [
                "${env:windir}\\Sysnative\\cmd.exe",
                "${env:windir}\\System32\\cmd.exe"
            ],
            "args": ["/k", "${env:cmder_root}\\vendor\\bin\\vscode_init.cmd"],
            "icon": "terminal-cmd",
            "color": "terminal.ansiGreen",
            "startingDirectory": "C:\\mm_dqx\\code"
        },
```



# Terminal



在Windows Terminal中添加cmder

```
            {
                "closeOnExit": "graceful",
                "colorScheme": "Monokai Cmder",
                "commandline": "cmd.exe /k \"%cmder_root%/vendor/init.bat\"",
                "guid": "{00000000-0000-0000-ba54-000000000132}",
                "hidden": false,
                "icon": "%cmder_root%/icons/cmder.ico",
                "startingDirectory": "C:\\mm_dqx\\code",
                "name": "Cmder"
            },
```

相关theme

```
        {
            "background": "#272822",
            "black": "#272822",
            "blue": "#01549E",
            "brightBlack": "#7C7C7C",
            "brightBlue": "#0383F5",
            "brightCyan": "#58C2E5",
            "brightGreen": "#8DD006",
            "brightPurple": "#A87DB8",
            "brightRed": "#F3044B",
            "brightWhite": "#FFFFFF",
            "brightYellow": "#CCCC81",
            "cursorColor": "#FFFFFF",
            "cyan": "#1A83A6",
            "foreground": "#CACACA",
            "green": "#74AA04",
            "name": "Monokai Cmder",
            "purple": "#89569C",
            "red": "#A70334",
            "selectionBackground": "#CCCC81",
            "white": "#CACACA",
            "yellow": "#B6B649"
        },
```



# cmder

## alias

在cmder环境下设置alias

```
cmder_mini\cmder\config\user_aliases.cmd
```

在`user_aliases.cmd`添加对应的alias指令即可

下一次启动cmder就会生效

## lambSymbol

修改显示符号: 最后添加的

```
if not prompt_lambSymbol then
    prompt_lambSymbol = "λ"
end
prompt_lambSymbol = "D0g3>" 
```

