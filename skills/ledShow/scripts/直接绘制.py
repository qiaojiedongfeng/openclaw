import pygame
import sys
import math

# 初始化 Pygame
pygame.init()

# 获取屏幕分辨率
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# 设置全屏
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("动态笑脸")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # 新增黄色作为脸部颜色

# 动画参数
mouth_height = 50  # 嘴巴初始高度
blink_counter = 0  # 眨眼计数器

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # 清屏
    screen.fill(BLACK)

    # 动态计算参数
    time = pygame.time.get_ticks() / 200  # 时间参数
    angle = math.sin(time) * 0.5  # 嘴巴弧度变化
    current_mouth_height = 50 + int(20 * math.sin(time * 2))  # 嘴巴高度变化

    # 绘制笑脸
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2, HEIGHT // 2), 300)  # 黄色脸

    # 动态眨眼（每120帧眨一次）
    blink_counter = (blink_counter + 1) % 120
    if blink_counter > 110:  # 最后10帧保持闭眼
        eye_height = 15
    else:
        eye_height = 60

    # 绘制眼睛
    pygame.draw.ellipse(screen, BLACK, (WIDTH // 2 - 100, HEIGHT // 2 - 50, 40, eye_height))  # 左眼
    pygame.draw.ellipse(screen, BLACK, (WIDTH // 2 + 50, HEIGHT // 2 - 50, 40, eye_height))  # 右眼

    # 绘制动态嘴巴
    mouth_rect = (WIDTH // 2 - 75, HEIGHT // 2 + 70, 150, current_mouth_height)
    pygame.draw.arc(screen, BLACK, mouth_rect, math.pi + angle, 2 * math.pi - angle, 10)

    # 刷新屏幕
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()
