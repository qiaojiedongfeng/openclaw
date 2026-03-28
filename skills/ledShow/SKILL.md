---
name: ledShow
description: LED展示，使用 Pygame 在屏幕上全屏显示LED滚动文字、动态笑脸以及Emoji表情。
metadata:
  {
    "openclaw":
      {
        "emoji": "📺",
        "os": ["win32", "darwin", "linux"],
        "requires": { "bins": ["python"] },
        "install": ["pip install pygame emoji"],
      },
  }
---

# ledShow

通过 Pygame 在屏幕上（全屏或窗口）显示LED风格的滚动文字、绘制的动态笑脸以及交互式 Emoji 表情。

## 何时使用

✅ **使用此 skill 当：**

- 用户想在屏幕上全屏显示一段滚动文字（如提示板、LED屏幕效果）
- 需要在屏幕上展示简单的动画图形（如动态笑脸）
- 想要展示 Emoji 表情并进行简单的键盘交互

## 何时不使用

❌ **不要使用此 skill 当：**

- 没有图形界面的纯终端环境（如只有 SSH 连接的服务器端），因为 Pygame 需要显示器支持
- 需要长时间运行且不能打断主程序的静默任务（此操作会唤起全屏及弹窗独占焦点）

## 需求

- 支持图形界面的操作系统 (Windows, macOS 或带有 GUI 的 Linux)
- 已安装 Python 环境
- 依赖库：`pygame`, `emoji`

## 包含的脚本与功能

* **滚动文字 (`scripts/ledShowText.py`)**
  包含的方法 `led_show_text(led_text)` 可以全屏黑色背景下，通过白色大字体循环从右向左滚动显示传入的文本。可以按 `ESC` 退出。

* **动态笑脸 (`scripts/直接绘制.py`)**
  纯通过 Pygame 绘制动态黄色笑脸图案，包含嘴巴的尺寸变化以及间歇性眨眼的循环动画。全屏显示，按 `ESC` 退出。

* **Emoji 表情 (`scripts/emoji表情.py`)**
  展示 Emoji，按空格键可以切换表情（笑脸和哭脸），按 `ESC` 退出。

## 安全规则

1. **退出机制**：所有全屏显示的脚本均已内置检测键盘按键，必须确保可通过按下 `ESC` 键安全退出。
2. **依赖检查**：运行前需确认 `pygame` 库已正确安装。

## 使用示例

### 全屏滚动文字

```bash
cd D:\MyProjects\NodeProjects\openclaw\skills\ledShow\scripts
python ledShowText.py "你好，OpenClaw！"
```

### 动态笑脸

```bash
cd D:\MyProjects\NodeProjects\openclaw\skills\ledShow\scripts
python 直接绘制.py
```

### Emoji 表情

```bash
cd D:\MyProjects\NodeProjects\openclaw\skills\ledShow\scripts
python emoji表情.py
```
