import pygame
import random

# กำหนดค่าพื้นฐาน
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# เริ่มต้น Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("โยนขยะลงถังขยะ")
clock = pygame.time.Clock()

# โหลดภาพ
trash_image = pygame.image.load("trash.png")  # ให้ใส่ไฟล์ภาพขยะที่มี
bin_image = pygame.image.load("bin.png")      # ให้ใส่ไฟล์ภาพถังขยะที่มี
bin_rect = bin_image.get_rect(center=(WIDTH // 2, HEIGHT - 50))

# กำหนดตำแหน่งขยะเริ่มต้น
trash_rect = trash_image.get_rect(center=(random.randint(50, WIDTH - 50), 0))

# สร้างตัวแปรสำหรับคะแนน
score = 0
font = pygame.font.SysFont(None, 55)

# ความเร็วในการเคลื่อนที่ของถังขยะ
bin_speed = 10

# กำหนดเวลาในการเล่นเป็น 2 นาที (120 วินาที)
time_limit = 120  # หน่วยเป็นวินาที
start_ticks = pygame.time.get_ticks()  # เก็บเวลาเริ่มต้น

# ลูปหลักของเกม
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ตรวจจับการกดปุ่ม
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bin_rect.left > 0:  # ขยับถังไปทางซ้าย
        bin_rect.x -= bin_speed
    if keys[pygame.K_RIGHT] and bin_rect.right < WIDTH:  # ขยับถังไปทางขวา
        bin_rect.x += bin_speed

    # อัปเดตตำแหน่งขยะ
    trash_rect.y += 10  # ขยับขยะลง

    # เช็คว่าขยะตกลงในถังหรือไม่
    if trash_rect.colliderect(bin_rect):
        score += 1
        trash_rect.center = (random.randint(50, WIDTH - 50), 0)  # รีเซ็ตตำแหน่งขยะใหม่

    # เช็คว่าขยะหลุดหน้าจอหรือไม่
    if trash_rect.y > HEIGHT:
        trash_rect.center = (random.randint(50, WIDTH - 50), 0)  # รีเซ็ตตำแหน่งขยะใหม่

    # ตรวจสอบเวลา
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # แปลงเป็นวินาที
    if elapsed_time > time_limit:
        running = False  # หยุดเกมเมื่อหมดเวลา

    # วาดพื้นหลัง
    screen.fill(WHITE)

    # วาดถังขยะและขยะ
    screen.blit(bin_image, bin_rect)
    screen.blit(trash_image, trash_rect)

    # แสดงคะแนนและเวลาเหลือ
    score_text = font.render(f'Score: {score}', True, BLACK)
    time_remaining = max(0, time_limit - int(elapsed_time))  # เวลาที่เหลือ
    time_text = font.render(f'Time: {time_remaining}', True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (WIDTH - 200, 10))  # แสดงเวลาที่เหลือที่มุมขวา

    # อัปเดตหน้าจอ
    pygame.display.flip()
    clock.tick(FPS)

# แสดงคะแนนสุดท้ายเมื่อเกมจบ
screen.fill(WHITE)
final_score_text = font.render(f'Final Score: {score}', True, BLACK)
screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()

# รอ 3 วินาทีก่อนปิด
pygame.time.delay(3000)
pygame.quit()
