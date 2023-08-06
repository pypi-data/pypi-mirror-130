# Quant Friend

## 背景和目的

在量化回测环境，经常需要购置和试用一些临时的计算资源。这个项目的目的是简化在这过程中的重复操作。

## 一键购置模块

TBC

## 汇报模块

这个模块需要被回测应用引入，在相关计算结束后，讲结果汇报给特定关注者，同时通知计算资源供应商，要求停止服务。

### email

可以显式调用

```python
from quant_friend import config_email_sender

config_email_sender('sender@my.com', 'smtp.my.com', 465, True, 'sender', 'password')
```

进行邮箱注册，也可以通过设置环境变量，自动注册。

- smtp_sender
- smtp_host
- smtp_port
- smtp_ssl
- smtp_user
- smtp_password

### 删除主机

可以显式调用

```python
from quant_friend import register_ucloud

register_ucloud(
    region="",
    private_key="",
    public_key="",
)
```

进行注册，也可以通过设置环境变量，自动注册。任意 **uc-** 开头的环境变量都会被自动读取。

```python
from quant_friend import list_and_delete_host

# 删除所有主机
list_and_delete_host('ucloud')
# 按业务组删除主机
list_and_delete_host('ucloud', Tag="你的业务组")
```