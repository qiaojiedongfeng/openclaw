import pyautogui
import time
import pyperclip
import subprocess
import os
import sys
import io
from pathlib import Path

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 获取脚本所在目录
current_dir = Path(__file__).parent.parent
print(current_dir)

def activate_wechat():
    """用 PowerShell 激活微信窗口"""
    ps_script = """
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
}
"@

# 新版微信进程名是 Weixin，通过进程主窗口句柄激活（无需猜类名）
$proc = Get-Process -Name "Weixin" -ErrorAction SilentlyContinue
if (-not $proc) {
    # 兼容旧版进程名 WeChat
    $proc = Get-Process -Name "WeChat" -ErrorAction SilentlyContinue
}

if (-not $proc) {
    Write-Host "未找到微信进程（Weixin / WeChat）"
    exit 1
}

# 取第一个有主窗口的进程实例
$hWnd = [IntPtr]::Zero
foreach ($p in $proc) {
    if ($p.MainWindowHandle -ne [IntPtr]::Zero) {
        $hWnd = $p.MainWindowHandle
        Write-Host ("找到微信窗口: PID={0} HWND={1}" -f $p.Id, $hWnd)
        break
    }
}

if ($hWnd -eq [IntPtr]::Zero) {
    Write-Host "微信进程存在但主窗口未找到（可能最小化到托盘）"
    # 尝试用类名兜底（旧版）
    foreach ($cls in @("WeChatMainWndForPC", "WeChat_PC_Window")) {
        $hWnd = [Win32]::FindWindow($cls, $null)
        if ($hWnd -ne [IntPtr]::Zero) {
            Write-Host "兜底找到窗口类: $cls"
            break
        }
    }
}

if ($hWnd -eq [IntPtr]::Zero) {
    Write-Host "无法获取微信窗口句柄"
    exit 1
}

# 还原并激活
[Win32]::ShowWindow($hWnd, 9)  # 9 = SW_RESTORE（从最小化还原）
Start-Sleep -Milliseconds 200
$result = [Win32]::SetForegroundWindow($hWnd)
if ($result) {
    Write-Host "成功激活微信窗口"
    exit 0
} else {
    Write-Host "激活窗口失败（窗口已在前台或权限受限）"
    exit 0
}
    """
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            timeout=5,
            text=True
        )

        if result.stdout:
            print(f"[PowerShell] {result.stdout.strip()}")
        if result.stderr:
            print(f"[PowerShell Error] {result.stderr.strip()}")

        return result.returncode == 0
    except Exception as e:
        print(f"❌ 激活微信失败: {e}")
        return False


def send_message(linkman, message_content):
    """发送微信消息"""

    # 激活微信窗口
    if not activate_wechat():
        print("❌ 微信未运行，请先打开微信")
        return False

    time.sleep(1)  # 等待窗口激活

    # 查找微信窗口中的搜索框或联系人列表
    search_location = None
    images = [
        current_dir / 'picture' / 'searchbutton.png',
        current_dir / 'picture' / 'searchbutton2.png',
        current_dir / 'picture' / 'searchbutton3.png',
        current_dir / 'picture' / 'searchbutton4.png'
    ]
    images = [str(img) for img in images if Path(img).exists()]

    if not images:
        print("❌ 未找到搜索栏图片，请检查 picture 目录")
        return False

    # 尝试找到搜索栏窗口
    wechat_location = None
    for img in images:
        try:
            wechat_location = pyautogui.locateOnScreen(
                img,
                minSearchTime=0.5,
                grayscale=True,
                confidence=0.7
            )
            if wechat_location:
                print(f"✓ 找到微信搜索框")
                break
        except pyautogui.ImageNotFoundException:
            continue
        except Exception as e:
            print(f"图像识别错误: {e}")
            continue

    if not wechat_location:
        print("❌ 未找到微信窗口，请确保微信已打开")
        return False

    # 计算搜索框位置
    search_x = wechat_location.left + 40
    search_y = wechat_location.top + 15

    print(f"屏幕尺寸: {pyautogui.size()}")
    print(f"搜索框位置: ({search_x}, {search_y})")

    try:
        # 点击搜索框
        pyautogui.click(search_x, search_y)
        time.sleep(0.5)

    #     # 清空搜索框
    #     pyautogui.hotkey('ctrl', 'a')
    #     time.sleep(0.2)

        # 输入联系人名称
        pyperclip.copy(linkman)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        # 按下回车选择第一个结果
        pyautogui.press('enter')
        time.sleep(1)

        # 尝试寻找笑脸图标来定位输入框
        smile_images = [
            current_dir / 'picture' / 'smile.png',
            current_dir / 'picture' / 'smile2.png'
        ]
        smile_images = [str(img) for img in smile_images if Path(img).exists()]


        smile_location = None
        if smile_images:
            for img in smile_images:
                try:
                    smile_location = pyautogui.locateOnScreen(
                        img,
                        minSearchTime=0.5,
                        grayscale=True,
                        confidence=0.8
                    )
                    if smile_location:
                        print(f"✓ 找到笑脸图标")
                        break
                except pyautogui.ImageNotFoundException:
                    continue
                except Exception as e:
                    print(f"图像识别错误(笑脸): {e}")
                    continue

        if smile_location:
            # 根据笑脸图标的位置加上偏移量，点击输入框
            input_x = smile_location.left + 30
            input_y = smile_location.top + 70
            print(f"点击输入框位置: ({input_x}, {input_y})")
            pyautogui.click(input_x, input_y)
            time.sleep(0.5)
            # 输入消息内容
            pyperclip.copy(message_content)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.8)

            # 发送消息 (Ctrl+Enter 或 Enter)
            pyautogui.hotkey('enter')
            time.sleep(1)

            print(f"✓ 消息已发送给 {linkman}")
            return True
        else:
            print("⚠️ 未能找到笑脸图标精确定位输入框，尝试直接输入")
            return False


    except Exception as e:
        print(f"❌ 发送消息失败: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python send_wechat.py <联系人> <消息内容>")
        print("示例: python send_wechat.py 张三 'Hello, how are you?'")
        sys.exit(1)

    linkman = sys.argv[1]
    message_content = sys.argv[2]

    print(f"准备发送消息:")
    print(f"  收件人: {linkman}")
    print(f"  内容: {message_content}")
    print()

    success = send_message(linkman, message_content)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
