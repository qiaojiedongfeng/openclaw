import pygame
import sys
import argparse
from pathlib import Path

# 这个是图片的路径，虽然内容一样，但格式不一样
current_dir = Path(__file__).parent




def led_show_text(led_text):
    print('Displaying:', led_text)
    # 初始化 Pygame
    pygame.init()

    # 获取屏幕的实际分辨率
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h

    # 设置 Pygame 窗口为全屏
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("滚动文字")

    # 隐藏鼠标箭头
    pygame.mouse.set_visible(False)

    # 加载字体文件（确保字体文件路径正确）
    try:
        font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 128)  # 使用支持中文的字体文件
    except FileNotFoundError:
        print("字体文件未找到，请确保路径正确！")
        sys.exit()
    # 渲染文字
    text = font.render(led_text, True, (255, 255, 255))  # 白色文字
    text_rect = text.get_rect()

    # 初始位置（从屏幕右侧开始）
    text_rect.x = WIDTH
    text_rect.y = HEIGHT // 2 - text_rect.height // 2  # 垂直居中

    # 滚动速度（像素/帧）
    scroll_speed = 2

    # 主循环
    running = True
    while running:
        # 事件处理（例如按 ESC 退出）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 更新文字位置
        text_rect.x -= scroll_speed
        if text_rect.right < 0:  # 如果文字完全滚出屏幕，重置到右侧
            text_rect.x = WIDTH

        # 清屏并绘制文字
        screen.fill((0, 0, 0))  # 黑色背景
        screen.blit(text, text_rect)

        # 刷新屏幕
        pygame.display.flip()

        # 控制帧率
        pygame.time.delay(20)

    # 退出 Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="全屏LED滚动文字展示")
    parser.add_argument("text", help="要滚动显示的文字内容")
    args = parser.parse_args()
    led_show_text(args.text)
