"""
test_proxy.py - 快速诊断代理和 NVIDIA API 连通性
"""
import requests
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

NVIDIA_API_KEY = "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"
NVIDIA_MODEL   = "qwen/qwen3.5-122b-a10b"

def test(label, proxies):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"🧪 {label}")
    print(f"   代理: {proxies}")

    # Step A: 测试代理本身是否能翻墙
    try:
        r = requests.get("https://api.ipify.org", proxies=proxies, timeout=10)
        print(f"   ✅ 代理可用！出口 IP: {r.text.strip()}")
    except Exception as e:
        print(f"   ❌ 代理不通: {e}")
        return

    # Step B: 测试 NVIDIA API （纯文字，最小请求）
    print("   🤖 测试 NVIDIA API 纯文字接口...")
    try:
        r2 = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Content-Type":  "application/json",
            },
            json={
                "model":      NVIDIA_MODEL,
                "messages":   [{"role": "user", "content": "回复两个字：测试通过"}],
                "max_tokens": 20,
                "stream":     False,
            },
            proxies=proxies,
            timeout=30,
        )
        print(f"   HTTP 状态: {r2.status_code}")
        print(f"   响应: {r2.text[:300]}")
    except Exception as e:
        print(f"   ❌ NVIDIA API 失败: {e}")

# ── 依次测试几种代理格式 ──────────────────────────────────────────────────
proxies_to_try = [
    ("HTTP 代理 7890",     {"http": "http://127.0.0.1:7890",    "https": "http://127.0.0.1:7890"}),
    ("SOCKS5 代理 7890",   {"http": "socks5://127.0.0.1:7890",  "https": "socks5://127.0.0.1:7890"}),
    ("SOCKS5 代理 7891",   {"http": "socks5://127.0.0.1:7891",  "https": "socks5://127.0.0.1:7891"}),
    ("HTTP 代理 10809",    {"http": "http://127.0.0.1:10809",   "https": "http://127.0.0.1:10809"}),  # v2rayN 常见端口
]

for label, proxies in proxies_to_try:
    test(label, proxies)

print("\n" + "=" * 60)
print("✅ 诊断完毕！把上方输出结果贴给我。")
print("   特别关注「出口 IP」那行，如果能显示 IP 说明该代理配置可用。")
print("=" * 60)
