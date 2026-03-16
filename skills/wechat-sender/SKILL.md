---
name: wechat-sender
description: 通过微信桌面客户端发送消息给联系人，或着 寻求Ai和XX的聊天记录并生成回复建议
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
- 用户想查看微信聊天内容并获取 AI 回复建议
- 需要 AI 帮忙想回复，直接粘贴到输入框由用户确认后发送

## 何时不使用

❌ **不要使用此 skill 当：**

- 微信桌面客户端未运行
- 联系人名称不明确或未找到
- 批量发送消息（需要用户明确确认）
- ⚠️ **后台定时任务或系统自动提醒（如放松眼睛等提示）**：除非用户**明确指示**“通过微信发送”，否则**绝对不要**将系统内部的自动提醒或定时任务重定向到微信。微信消息发送仅限用户显式发起的场景！

## 需求

- Windows 操作系统
- 微信桌面客户端已安装并运行

### AI 回复建议（截图分析 + 自动粘贴）

```bash
python read_wechat.py "联系人或群名称"
```

流程：激活微信 → 搜索联系人 → 截图发给 Qwen 多模态模型 → 流式输出 3 条风格不同的回复建议 → 自动粘贴到微信输入框，由用户删除多余选项后发送。

### 发送消息

```bash
python send_wechat.py "联系人名称" "消息内容"
```

## 安全规则

1. **发送前必须确认** 收件人和消息内容
2. **验证联系人** 在微信中存在
3. **检查消息内容** 准确无误
4. **确保微信已运行** 再尝试发送
5. **AI 回复建议仅供参考**，由用户决定最终发送内容

## 使用示例

用户："帮我看一下微信「云端技术分享群」最新的消息，给我回复建议"

```bash
cd D:\MyProjects\NodeProjects\openclaw\skills\wechat-sender\scripts
python read_wechat.py "云端技术分享群"
```

用户："给张三发消息说'你好，现在怎么样？'"

```bash
cd D:\MyProjects\NodeProjects\openclaw\skills\wechat-sender\scripts
python send_wechat.py "张三" "你好，现在怎么样？"
```
