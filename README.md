# ssh-proxy

一个方便本地开发做ssh端口转发的脚本

## 用法:

在HOME目录下编辑proxy.json
```
[
    {
        "user": "user",
        "host": "x.x.x.x",
        "proxys": [
            "3306:dev.rds.aliyuncs.com:3306"
        ]
    },
    {
        "user": "user",
        "host": "x.x.x.x",
        "proxys": [
            "3306:dev.rds.aliyuncs.com:3306"
        ]
    }
]
```
启动脚本便通过x.x.x.x远程主机将开发环境dev.rds.aliyuncs.com的3306端口映射到了本地3306