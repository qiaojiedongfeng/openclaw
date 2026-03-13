# WeChat Sender Skill

自动化发送微信消息的 skill。

## 安装依赖

```bash
pip install pyautogui pyperclip keyboard PySide6
```

## 使用方法

```bash
python scripts/send_wechat.py "联系人名称" "消息内容"
```

## 示例

```bash
python scripts/send_wechat.py "张三" "你好，现在工资多少呀？"
python scripts/send_wechat.py "胡总" "贾海琳现在没有来，合同还没给"
```

## 工作原理

1. **PowerShell 激活微信窗口** — 比图像识别更快更稳定
2. **PyAutoGUI 搜索联系人** — 通过图像识别找到搜索框
3. **输入消息并发送** — 使用剪贴板避免输入法问题

## 注意事项

- 确保微信桌面客户端已运行
- 需要在 `picture/` 目录下放置微信图标截图（用于定位搜索框）
- 消息内容通过剪贴板传输，避免输入法干扰
- 脚本会自动等待窗口激活和各个操作步骤

## 图片资源

需要在 `picture/` 目录下放置以下微信图标截图：
- `WeChatLogo.png`
- `WeChatLogo2.png`
- `WeChatLogo3.png`
- `WeChatLogo4.png`

这些图片用于定位微信窗口中的搜索框位置。
