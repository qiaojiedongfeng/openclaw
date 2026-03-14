import pygame
import sys
import emoji

# 初始化 Pygame
pygame.init()

# 设置屏幕分辨率
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emoji 库表情符号")

# 加载支持表情符号的字体
try:
    font = pygame.font.Font("msyh.ttc", 64)  # 使用支持表情符号的字体
except FileNotFoundError:
    print("字体文件未找到，请确保路径正确！")
    sys.exit()

# 使用 emoji 库获取表情符号
smile_emoji = emoji.emojize(":smile:")  # 笑的表情
cry_emoji = emoji.emojize(":cry:")      # 哭的表情

# 渲染表情符号
smile_text = font.render(smile_emoji, True, (255, 255, 255))
cry_text = font.render(cry_emoji, True, (255, 255, 255))

# 设置表情符号的位置
smile_rect = smile_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
cry_rect = cry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# 当前显示的表情（默认为笑）
current_emotion = "smile"

# 主循环
running = True
while running:
    # 事件处理（例如按 ESC 退出或按空格切换表情）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # 按 ESC 退出
                running = False
            elif event.key == pygame.K_SPACE:  # 按空格切换表情
                if current_emotion == "smile":
                    current_emotion = "cry"
                else:
                    current_emotion = "smile"

    # 清屏
    screen.fill((0, 0, 0))  # 黑色背景

    # 根据当前表情绘制
    if current_emotion == "smile":
        screen.blit(smile_text, smile_rect)
    else:
        screen.blit(cry_text, cry_rect)

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    pygame.time.delay(20)

# 退出 Pygame
pygame.quit()
sys.exit()