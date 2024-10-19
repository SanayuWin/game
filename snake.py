import pygame
import time
import random

# เริ่มต้น PyGame
pygame.init()

# กำหนดสีที่ใช้ในเกม
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# ขนาดของหน้าจอเกม
width = 800
height = 600

# สร้างหน้าต่างเกม
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# กำหนดเวลา (Clock) ของเกม
clock = pygame.time.Clock()

# ขนาดบล็อกของงูและความเร็วเริ่มต้น
snake_block = 10
snake_speed = 15

# กำหนดฟอนต์
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# ฟังก์ชันแสดงคะแนน
def show_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    dis.blit(value, [0, 0])

# ฟังก์ชันแสดงข้อความ
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])

# ฟังก์ชันวาดงู
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# ฟังก์ชันหลักของเกม
def gameLoop():
    game_over = False
    game_close = False

    # ตั้งค่าตำแหน่งเริ่มต้นของงู
    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    # ตั้งค่าความยาวเริ่มต้นของงู
    snake_list = []
    length_of_snake = 1

    # สุ่มตำแหน่งของอาหาร
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Continue or Q-Quit", red)
            show_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # ตรวจสอบว่าชนขอบจอหรือไม่
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # วาดอาหาร
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # เพิ่มขนาดของงู
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # ตรวจสอบว่าชนตัวเองหรือไม่
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        show_score(length_of_snake - 1)
        pygame.display.update()

        # ตรวจสอบว่ากินอาหารหรือไม่
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# เรียกใช้เกม
gameLoop()
