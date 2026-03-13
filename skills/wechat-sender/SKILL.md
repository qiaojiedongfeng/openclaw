---
name: wechat-sender
description: 通过微信桌面客户端发送消息给联系人
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "os": ["win32"],
        "requires": { "bins": ["python"] },
        "install": [],
      },
  }
---

# wechat-sender

在 Windows 上通过微信桌面客户端自动发送消息。

## 何时使用

✅ **使用此 skill 当：**

- 用户想给某人发送微信消息
- 需要发送特定内容给某个联系人
- 自动化微信消息发送

## 何时不使用

❌ **不要使用此 skill 当：**

- 微信桌面客户端未运行
- 联系人名称不明确或未找到
- 批量发送消息（需要用户明确确认）

## 需求

- Windows 操作系统
- 微信桌面客户端已安装并运行

## 常用命令

### 发送消息

```bash
python send_wechat.py "联系人名称" "消息内容"
```

## 安全规则

1. **发送前必须确认** 收件人和消息内容
2. **验证联系人** 在微信中存在
3. **检查消息内容** 准确无误
4. **确保微信已运行** 再尝试发送

## 使用示例

用户："给张三发消息说'你好，现在怎么样？'"



```bash
cd D:\MyProjects\NodeProjects\openclaw\skills\wechat-sender\scripts
python send_wechat.py "张三" "你好，现在怎么样？"
```
