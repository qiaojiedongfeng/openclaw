"""
inspect_wechat.py - 微信窗口控件诊断脚本
用途：打印微信窗口的完整控件树，帮助找到聊天记录列表的正确控件名称
运行前请确保：微信已打开并停留在某个联系人的聊天窗口
"""

import uiautomation as auto
import sys
import io
import time

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def print_control_tree(control, depth=0, max_depth=5):
    """递归打印控件树"""
    indent = "  " * depth
    try:
        ctrl_type = control.ControlTypeName
        ctrl_name = repr(control.Name[:60]) if control.Name else '""'
        ctrl_class = control.ClassName or ""
        print(f"{indent}[{ctrl_type}] Name={ctrl_name} Class={ctrl_class!r}")
    except Exception as e:
        print(f"{indent}[ERROR reading control: {e}]")
        return

    if depth >= max_depth:
        return

    try:
        children = control.GetChildren()
        for child in children:
            print_control_tree(child, depth + 1, max_depth)
    except Exception as e:
        print(f"{indent}  [ERROR getting children: {e}]")


def inspect_wechat():
    print("🔍 开始扫描微信窗口控件树...")
    print("📌 请确保微信已打开，并停留在某位联系人的聊天界面\n")

    # 查找微信主窗口（超时 5 秒）
    wechat_win = auto.WindowControl(Name='微信', searchDepth=1)
    if not wechat_win.Exists(5, 1):
        print("❌ 未找到微信主窗口（Name='微信'），尝试不限名称搜索...")
        # 遍历所有顶层窗口，找包含"微信"或"Weixin"的
        all_wins = auto.GetRootControl().GetChildren()
        for w in all_wins:
            try:
                if '微信' in (w.Name or '') or 'Weixin' in (w.ClassName or '') or 'WeChat' in (w.ClassName or ''):
                    print(f"✅ 找到候选窗口: Name={w.Name!r} Class={w.ClassName!r}")
                    wechat_win = w
                    break
            except:
                pass
        else:
            print("❌ 完全找不到微信窗口，请检查微信是否运行。")
            return

    print(f"✅ 找到微信窗口: Name={wechat_win.Name!r} Class={wechat_win.ClassName!r}")
    print("=" * 70)
    print("📋 控件树（最深 4 层）：")
    print("=" * 70)
    time.sleep(0.5)
    print_control_tree(wechat_win, depth=0, max_depth=4)

    print("\n" + "=" * 70)
    print("💡 关注: 找含有聊天内容的 [ListControl] 或 [PaneControl] 等控件")
    print("   重点看 Name= 的值，那就是 read_wechat.py 里要填的控件名称")
    print("=" * 70)


if __name__ == '__main__':
    inspect_wechat()
