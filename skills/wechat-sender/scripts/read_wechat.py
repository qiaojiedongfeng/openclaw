"""
read_wechat.py - 微信聊天截图 → NVIDIA Qwen 多模态 AI → 回复建议
流程：激活微信 → 搜索联系人 → 截图 → 直接发图给 Qwen 视觉模型 → 流式输出建议

用法: python read_wechat.py <联系人名字>
示例: python read_wechat.py 张三

依赖安装:
    pip install pyautogui pyperclip requests pillow
"""

import pyautogui
import pyperclip
import subprocess
import requests
import base64
import time
import sys
import io
import json
from pathlib import Path

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 脚本根目录（skills/wechat-sender/）
current_dir = Path(__file__).parent.parent

# ── NVIDIA AI API 配置 ────────────────────────────────────────────────────
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_API_KEY = "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"
NVIDIA_MODEL   = "qwen/qwen3.5-122b-a10b"
# ──────────────────────────────────────────────────────────────────────────

# ── 代理配置 ──────────────────────────────────────────────────────────────
# 优先读取环境变量 https_proxy/http_proxy，否则使用本地默认端口 7890
import os as _os
_proxy_url = (
    _os.environ.get("https_proxy")
    or _os.environ.get("HTTPS_PROXY")
    or _os.environ.get("http_proxy")
    or _os.environ.get("HTTP_PROXY")
    or "http://127.0.0.1:7890"   # Clash/v2ray 默认端口，按需修改
)
PROXIES = {"http": _proxy_url, "https": _proxy_url}
print(f"🌐 代理配置: {_proxy_url}")
# ──────────────────────────────────────────────────────────────────────────


# ── Step 1: 激活微信窗口 ───────────────────────────────────────────────────

def activate_wechat():
    """用 PowerShell 把微信窗口提到前台"""
    ps_script = r"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
}
"@

$proc = Get-Process -Name "Weixin" -ErrorAction SilentlyContinue
if (-not $proc) { $proc = Get-Process -Name "WeChat" -ErrorAction SilentlyContinue }
if (-not $proc) { Write-Host "未找到微信进程"; exit 1 }

$hWnd = [IntPtr]::Zero
foreach ($p in $proc) {
    if ($p.MainWindowHandle -ne [IntPtr]::Zero) { $hWnd = $p.MainWindowHandle; break }
}
if ($hWnd -eq [IntPtr]::Zero) {
    foreach ($cls in @("WeChatMainWndForPC", "WeChat_PC_Window")) {
        $hWnd = [Win32]::FindWindow($cls, $null)
        if ($hWnd -ne [IntPtr]::Zero) { break }
    }
}
if ($hWnd -eq [IntPtr]::Zero) { Write-Host "无法获取微信窗口句柄"; exit 1 }

[Win32]::ShowWindow($hWnd, 9)
Start-Sleep -Milliseconds 300
[Win32]::SetForegroundWindow($hWnd) | Out-Null
Write-Host "成功激活微信窗口"
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, timeout=5, text=True
        )
        if result.stdout:
            print(f"[PowerShell] {result.stdout.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 激活微信失败: {e}")
        return False


# ── Step 2: 搜索联系人进入聊天 ───────────────────────────────────────────

def navigate_to_contact(linkman):
    """通过图像识别定位搜索框，搜索联系人并进入聊天窗口"""
    images = [
        current_dir / 'picture' / 'searchbutton.png',
        current_dir / 'picture' / 'searchbutton2.png',
        current_dir / 'picture' / 'searchbutton3.png',
        current_dir / 'picture' / 'searchbutton4.png',
    ]
    images = [str(img) for img in images if Path(img).exists()]

    if not images:
        print("⚠️  未找到搜索栏参考图片，将跳过导航直接截图当前界面")
        return False

    wechat_location = None
    for img in images:
        try:
            wechat_location = pyautogui.locateOnScreen(
                img, minSearchTime=0.5, grayscale=True, confidence=0.7
            )
            if wechat_location:
                print("✅ 找到微信搜索框")
                break
        except pyautogui.ImageNotFoundException:
            continue
        except Exception as e:
            print(f"图像识别错误: {e}")

    if not wechat_location:
        print("⚠️  未找到微信搜索框，将跳过导航直接截图当前界面")
        return False

    try:
        pyautogui.click(wechat_location.left + 40, wechat_location.top + 15)
        time.sleep(0.5)
        pyperclip.copy(linkman)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.2)
        pyautogui.press('enter')
        time.sleep(1.5)
        print(f"✅ 已进入与「{linkman}」的聊天窗口")
        return True
    except Exception as e:
        print(f"❌ 导航失败: {e}")
        return False


# ── Step 3: 截图并压缩为 JPEG base64 ─────────────────────────────────────

def take_screenshot_as_b64(quality=70) -> str:
    """截取全屏，压缩为 JPEG，返回 base64 字符串"""
    print("📸 正在截取聊天区域...")
    time.sleep(0.3)

    screenshot = pyautogui.screenshot().convert("RGB")

    # 保存临时文件便于调试
    tmp_path = Path(__file__).parent / "_last_screenshot.jpg"
    screenshot.save(str(tmp_path), format="JPEG", quality=quality)

    # 编码为 base64
    buf = io.BytesIO()
    screenshot.save(buf, format="JPEG", quality=quality)
    img_bytes = buf.getvalue()
    img_b64 = base64.standard_b64encode(img_bytes).decode("utf-8")

    print(f"✅ 截图完成：{len(img_bytes)//1024} KB → 已保存至 {tmp_path.name}")
    return img_b64


# ── Step 4: NVIDIA Qwen 多模态分析（流式） ────────────────────────────────

def analyze_chat_with_ai(img_b64: str, linkman: str) -> str:
    """把截图直接发给 NVIDIA Qwen 多模态模型，流式输出回复建议"""

    prompt = f"""请仔细查看这张微信聊天截图。这是我和「{linkman}」的对话内容。

请站在我的角度，生成 3 条风格不同的回复建议，我会直接选一条粘贴发送：

【简洁版】<一句话，适合忙碌时快速回复>
【温暖版】<有温度和细节，适合亲近的朋友>
【幽默版】<轻松有趣，适合氛围轻松时>

只输出这 3 条回复内容本身，不要额外解释。请用中文。"""

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept":        "text/event-stream",
        "Content-Type":  "application/json",
    }

    payload = {
        "model": NVIDIA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_b64}"
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
        "max_tokens":  2048,
        "temperature": 0.7,
        "top_p":       0.95,
        "stream":      True,
        "chat_template_kwargs": {"enable_thinking": True},
    }

    print("🤖 正在请求 NVIDIA Qwen 多模态 AI 分析（流式输出）...\n")

    try:
        resp = requests.post(
            NVIDIA_API_URL, headers=headers, json=payload,
            stream=True, timeout=120, proxies=PROXIES
        )
        resp.raise_for_status()

        full_reply   = []
        thinking_dot = False  # 是否已打印过"思考中"提示

        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                break

            try:
                chunk   = json.loads(data_str)
                delta   = chunk["choices"][0]["delta"]

                # thinking 内容（模型的推理过程）：折叠显示
                if delta.get("reasoning_content"):
                    if not thinking_dot:
                        print("💭 [Qwen 思考中，请稍候...]", flush=True)
                        thinking_dot = True
                    continue

                # 正式回复内容：流式打印
                content = delta.get("content", "")
                if content:
                    if thinking_dot:
                        print()  # 思考结束，在新行开始输出
                        thinking_dot = False
                    print(content, end="", flush=True)
                    full_reply.append(content)

            except (json.JSONDecodeError, KeyError):
                continue

        print()  # 流结束换行
        return "".join(full_reply)

    except requests.exceptions.HTTPError:
        print(f"\n❌ API 请求失败 (HTTP {resp.status_code})")
        print(f"   响应: {resp.text[:500]}")
        return None
    except Exception as e:
        print(f"\n❌ API 请求异常: {e}")
        return None


# ── Step 5: 粘贴回复建议到微信输入框 ──────────────────────────────────────

def paste_reply_to_input(reply_text: str):
    """将 AI 生成的 3 条回复建议粘贴到微信输入框中，用户删掉不要的再发送"""
    if not reply_text or not reply_text.strip():
        print("⚠️  回复内容为空，跳过粘贴")
        return

    # 通过笑脸图标定位微信输入框（与 send_wechat.py 保持一致）
    smile_images = [
        current_dir / 'picture' / 'smile.png',
        current_dir / 'picture' / 'smile2.png',
    ]
    smile_images = [str(img) for img in smile_images if Path(img).exists()]

    smile_location = None
    for img in smile_images:
        try:
            smile_location = pyautogui.locateOnScreen(
                img, minSearchTime=0.5, grayscale=True, confidence=0.8
            )
            if smile_location:
                print("✓ 找到笑脸图标，定位输入框")
                break
        except pyautogui.ImageNotFoundException:
            continue
        except Exception as e:
            print(f"图像识别错误(笑脸): {e}")

    if not smile_location:
        print("⚠️  未找到笑脸图标，无法定位输入框，请手动粘贴")
        pyperclip.copy(reply_text.strip())  # 至少把内容放到剪贴板
        print("📋 回复建议已复制到剪贴板，请手动 Ctrl+V 粘贴")
        return

    try:
        # 笑脸图标右侧偏下即为输入框
        input_x = smile_location.left + 30
        input_y = smile_location.top + 70
        print(f"点击输入框位置: ({input_x}, {input_y})")
        pyautogui.click(input_x, input_y)
        time.sleep(0.4)

        # 将回复建议写入剪贴板并粘贴
        pyperclip.copy(reply_text.strip())
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        print("✅ 已将回复建议粘贴到微信输入框，请删除多余选项后发送！")
    except Exception as e:
        print(f"❌ 粘贴失败: {e}")


# ── 主流程 ────────────────────────────────────────────────────────────────

def get_reply_suggestions(linkman: str):
    print(f"\n{'='*60}")
    print(f"  🚀  微信聊天 AI 副驾驶（Qwen 多模态直接看图）")
    print(f"  联系人: {linkman}")
    print(f"{'='*60}\n")

    # 1. 激活微信
    if not activate_wechat():
        print("❌ 微信未运行，请先打开微信")
        return
    time.sleep(1)

    # 2. 导航到联系人（找不到搜索框时跳过，截取当前界面）
    navigate_to_contact(linkman)
    time.sleep(0.5)

    # 3. 截图 → base64
    img_b64 = take_screenshot_as_b64(quality=70)

    # 4. AI 直接看图分析
    print("=" * 60)
    print("💡 AI 回复建议：")
    print("=" * 60)
    result = analyze_chat_with_ai(img_b64, linkman)
    print("=" * 60)
    if not result:
        print("❌ 未能获取 AI 回复建议，请查看上面的错误信息")
        return

    # 5. 粘贴回复建议到微信输入框（微信窗口已激活，直接定位粘贴）
    paste_reply_to_input(result)


def main():
    if len(sys.argv) < 2:
        print("用法: python read_wechat.py <联系人名字>")
        print("示例: python read_wechat.py 张三")
        sys.exit(1)

    get_reply_suggestions(sys.argv[1])


if __name__ == '__main__':
    main()
