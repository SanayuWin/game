import pygame
import random

# กำหนดสี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# กำหนดขนาดของบล็อกและตารางเกม
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# ตั้งค่า Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
pygame.display.set_caption("Block Blast")
clock = pygame.time.Clock()

# ฟอนต์สำหรับแสดงคะแนนและเวลา
font = pygame.font.Font(None, 36)

# รูปร่างของบล็อก (Tetriminoes)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[0, 1, 0], [1, 1, 1]],  # T
]

# ฟังก์ชันสำหรับสร้างบล็อก
def create_block():
    shape = random.choice(SHAPES)
    color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW])
    return {"shape": shape, "color": color, "x": GRID_WIDTH // 2 - len(shape[0]) // 2, "y": 0}

# ฟังก์ชันสำหรับการวาดบล็อก
def draw_block(block):
    shape = block["shape"]
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    block["color"],
                    (int((block["x"] + col_idx) * BLOCK_SIZE),
                     int((block["y"] + row_idx) * BLOCK_SIZE),
                     BLOCK_SIZE,
                     BLOCK_SIZE),
                )

# ฟังก์ชันสำหรับวาดตารางเกม
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(
                screen,
                BLACK,
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )

# ฟังก์ชันสำหรับแสดงคะแนนและเวลา
def draw_text(text, x, y):
    render = font.render(text, True, RED)
    screen.blit(render, (x, y))

# ฟังก์ชันตรวจสอบการชน
def check_collision(block, grid):
    shape = block["shape"]
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                x = block["x"] + col_idx
                y = block["y"] + row_idx
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid[y][x]:
                    return True
    return False

# ฟังก์ชันสำหรับวางบล็อกลงในตาราง
def place_block(block, grid):
    shape = block["shape"]
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                grid[block["y"] + row_idx][block["x"] + col_idx] = block["color"]

# ฟังก์ชันสำหรับการลบแถว
def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    rows_cleared = GRID_HEIGHT - len(new_grid)
    new_grid = [[0] * GRID_WIDTH for _ in range(rows_cleared)] + new_grid
    return new_grid, rows_cleared

# ฟังก์ชันเริ่มต้นเกม
def main():
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_block = create_block()
    fall_time = 0
    fall_speed = 30  # ความเร็วในการตกของบล็อก (มิลลิวินาที)
    score = 0
    start_time = pygame.time.get_ticks()  # บันทึกเวลาที่เริ่มเกม

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_block(current_block)

        # คำนวณเวลาที่เล่น (เป็นวินาที)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # แสดงคะแนนและเวลาที่เล่น
        draw_text(f"Score: {score}", 10, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_block["x"] -= 1
                    if check_collision(current_block, grid):
                        current_block["x"] += 1
                elif event.key == pygame.K_RIGHT:
                    current_block["x"] += 1
                    if check_collision(current_block, grid):
                        current_block["x"] -= 1
                elif event.key == pygame.K_DOWN:
                    current_block["y"] += 1
                    if check_collision(current_block, grid):
                        current_block["y"] -= 1
                elif event.key == pygame.K_UP:
                    current_block["shape"] = list(zip(*reversed(current_block["shape"])))
                    if check_collision(current_block, grid):
                        current_block["shape"] = list(zip(*reversed(current_block["shape"])))  # ย้อนกลับ

        fall_time += clock.get_rawtime()
        if fall_time > fall_speed:
            current_block["y"] += 1
            if check_collision(current_block, grid):
                current_block["y"] -= 1
                place_block(current_block, grid)
                grid, rows_cleared = clear_rows(grid)
                score += rows_cleared * 10
                current_block = create_block()
                if check_collision(current_block, grid):
                    running = False  # จบเกมเมื่อบล็อกไม่สามารถตกลงได้
            fall_time = 0

        # วาดตารางที่มีบล็อกอยู่
        for y, row in enumerate(grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print(f"Game Over! Score: {score}, Time: {elapsed_time} seconds")

if __name__ == "__main__":
    main()
