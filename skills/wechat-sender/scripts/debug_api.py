"""
debug_api.py - 专门用来诊断截图 + MiniMax API 调用是否正常
步骤：
  1. 截取全屏并保存到本地 debug_screenshot.png（方便肉眼确认截图内容）
  2. 用纯文本消息测试 API 是否通（排除网络/key 问题）
  3. 用截图 base64 测试多模态接口（找出图片未传到的根因）
"""

import pyautogui
import requests
import base64
import sys
import io
import json
from pathlib import Path

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

MINIMAX_API_BASE = "https://api.minimaxi.com/anthropic"
MINIMAX_API_KEY  = "sk-cp-FYiNElCk7hWXawTD51nTlv74Yq2jzXbhMqccn-ixHC4Q3nCLqW0tuI4OZOXQXR0bbk5fZkFl1cKMXKWzTDYcbKkD6nkQPjhEWijvW8K8iUhJ8278i0VI6Xk"
MINIMAX_MODEL    = "MiniMax-M2.5"

HEADERS = {
    "x-api-key":         MINIMAX_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type":      "application/json",
}

SAVE_PATH = Path(__file__).parent / "debug_screenshot.png"


def do_request(body: dict, label: str):
    """发请求，打印完整响应"""
    print(f"\n{'─'*60}")
    print(f"📤 [{label}] 发送请求...")
    try:
        r = requests.post(
            f"{MINIMAX_API_BASE}/v1/messages",
            headers=HEADERS,
            json=body,
            timeout=60,
        )
        print(f"   HTTP 状态码: {r.status_code}")
        try:
            resp_json = r.json()
            # 屏蔽 base64 data 字段，只打印结构
            print(f"   响应 JSON (结构预览):")
            print(json.dumps(resp_json, ensure_ascii=False, indent=2)[:2000])
        except Exception:
            print(f"   原始响应文本: {r.text[:500]}")
        return r
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None


# ── 测试 1：纯文字消息 ──────────────────────────────────────────────────────
def test_text_only():
    print("\n" + "="*60)
    print("🧪 测试 1：纯文字消息（验证 API Key 和网络是否通）")
    body = {
        "model": MINIMAX_MODEL,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": "请回复：API连通性测试通过"}],
    }
    return do_request(body, "纯文字")


# ── 测试 2：base64 图片（Anthropic 标准格式）────────────────────────────────
def test_image_base64(img_b64: str):
    print("\n" + "="*60)
    print("🧪 测试 2：Anthropic 标准格式 base64 图片")
    body = {
        "model": MINIMAX_MODEL,
        "max_tokens": 128,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type":       "base64",
                            "media_type": "image/png",
                            "data":       img_b64,
                        },
                    },
                    {"type": "text", "text": "这张截图里有什么内容？请用一句话描述。"},
                ],
            }
        ],
    }
    return do_request(body, "base64图片-Anthropic格式")


# ── 测试 3：OpenAI 兼容格式尝试（image_url + data URI）──────────────────────
def test_image_openai_format(img_b64: str):
    print("\n" + "="*60)
    print("🧪 测试 3：OpenAI 兼容格式 image_url（data URI）")
    # 有些 Anthropic-compat API 实际底层是 OpenAI 格式，这里都试一下
    body = {
        "model": MINIMAX_MODEL,
        "max_tokens": 128,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        },
                    },
                    {"type": "text", "text": "这张截图里有什么内容？请用一句话描述。"},
                ],
            }
        ],
    }
    return do_request(body, "base64图片-OpenAI格式")


def compress_to_jpeg(pil_image, quality=60) -> str:
    """把 PIL 截图压缩成 JPEG base64，减少传输体积"""
    buf = io.BytesIO()
    # 先确保是 RGB（截图可能是 RGBA）
    pil_image = pil_image.convert("RGB")
    pil_image.save(buf, format='JPEG', quality=quality)
    data = buf.getvalue()
    b64 = base64.standard_b64encode(data).decode('utf-8')
    print(f"   JPEG 压缩后大小: {len(data)//1024} KB，base64 长度: {len(b64)} 字符")
    return b64


# ── 测试 4：MiniMax 原生 OpenAI 兼容接口 ────────────────────────────────────
def test_minimax_native_openai(img_b64_jpeg: str):
    print("\n" + "="*60)
    print("🧪 测试 4：MiniMax 原生 OpenAI 兼容接口（api.minimaxi.chat）+ JPEG")
    headers_oa = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "content-type":  "application/json",
    }
    body = {
        "model":      MINIMAX_MODEL,
        "max_tokens": 256,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type":      "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64_jpeg}"},
                    },
                    {"type": "text", "text": "这张截图里有什么内容？请用一句话描述。"},
                ],
            }
        ],
    }
    print(f"\n{'─'*60}")
    print(f"📤 [MiniMax原生-OpenAI格式] 发送请求...")
    try:
        r = requests.post(
            "https://api.minimaxi.chat/v1/chat/completions",
            headers=headers_oa,
            json=body,
            timeout=60,
        )
        print(f"   HTTP 状态码: {r.status_code}")
        try:
            resp_json = r.json()
            print(f"   响应 JSON:")
            print(json.dumps(resp_json, ensure_ascii=False, indent=2)[:2000])
        except Exception:
            print(f"   原始响应: {r.text[:500]}")
        return r
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        return None


def main():
    from PIL import Image
    import time

    # ── 截图并保存到本地 ──
    print("📸 截取当前屏幕...")
    time.sleep(1)
    shot = pyautogui.screenshot()
    shot.save(str(SAVE_PATH))
    print(f"✅ PNG 截图已保存到: {SAVE_PATH}")
    print(f"   （请手动打开这个文件，确认截图内容是否正确）")

    buf = io.BytesIO()
    shot.save(buf, format='PNG')
    img_b64_png = base64.standard_b64encode(buf.getvalue()).decode('utf-8')
    print(f"   PNG base64 长度: {len(img_b64_png)} 字符")

    # 压缩成 JPEG，给测试 4 用
    print("🗜️  正在压缩为 JPEG...")
    img_b64_jpeg = compress_to_jpeg(shot, quality=60)

    # ── 依次测试 ──
    test_text_only()
    test_image_base64(img_b64_png)
    test_image_openai_format(img_b64_png)
    test_minimax_native_openai(img_b64_jpeg)   # ← 新增：原生接口

    print("\n" + "="*60)
    print("✅ 诊断完毕，请把上面的输出贴给我，我来判断哪种格式能用。")
    print("="*60)


if __name__ == '__main__':
    main()
