import pygame

pygame.init()

# Grid settings
grid_size = 50
cell_size = 16
char_size = 32
screen_width = grid_size * cell_size
screen_height = grid_size * cell_size

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid-based Character Movement")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a custom grid
grid = [
    ['*']*grid_size,
    ['*'] + ['o']*(grid_size-2) + ['*'],
    ['*'] + ['o']*(grid_size-2) + ['*'],
    ['*'] + ['o']*(grid_size-2) + ['*'],
    ['*'] + ['o']*(grid_size-2) + ['*'],
    ['*'] + ['o']*10 + ['*']*5 + ['o']*(grid_size-17) + ['*'],
    ['*'] + ['o']*10 + ['*']*5 + ['o']*(grid_size-17) + ['*'],
    ['*'] + ['o']*10 + ['*']*5 + ['o']*(grid_size-17) + ['*'],
    ['*'] + ['o']*10 + ['*']*5 + ['o']*(grid_size-17) + ['*'],
    ['*'] + ['o']*10 + ['*']*5 + ['o']*(grid_size-17) + ['*'],
]
# Fill the rest of the grid with a pattern
for i in range(10, grid_size-1):
    row = ['*'] + ['o']*15 + ['*']*3 + ['o']*15 + ['*']*3 + ['o']*12 + ['*']
    grid.append(row)
grid.append(['*']*grid_size)  # Bottom wall

# Ensure starting position is empty
start_x, start_y = 1, 1

# Load and resize character image
char_img = pygame.image.load("Hero_move/run2.png")

# Character position (in grid coordinates)
char_x, char_y = start_x, start_y

clock = pygame.time.Clock()

def draw_grid():
    for y in range(grid_size):
        for x in range(grid_size):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if grid[y][x] == 'o':
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)

def can_move(x, y):
    for dy in range(char_size // cell_size):
        for dx in range(char_size // cell_size):
            if not (0 <= x + dx < grid_size and 0 <= y + dy < grid_size) or grid[y + dy][x + dx] == '*':
                return False
    return True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            new_x, new_y = char_x, char_y
            if event.key == pygame.K_LEFT:
                new_x -= 1
            elif event.key == pygame.K_RIGHT:
                new_x += 1
            elif event.key == pygame.K_UP:
                new_y -= 1
            elif event.key == pygame.K_DOWN:
                new_y += 1
            
            # Check if the new position is valid
            if can_move(new_x, new_y):
                char_x, char_y = new_x, new_y

    screen.fill(WHITE)
    draw_grid()
    screen.blit(char_img, (char_x * cell_size, char_y * cell_size))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 800
GAME_AREA_WIDTH = int(WIDTH * 0.75)  # 75% of width for game area
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game")

# Colors
GRASS_GREEN = (124, 252, 0)  # Light green color for grass
DARK_GREEN = (0, 100, 0)  # Dark green for obstacles
GRAY = (128, 128, 128)

# Grid setup
GRID_SIZE = 20
cell_size = GAME_AREA_WIDTH // GRID_SIZE

# Character size multiplier
CHAR_SIZE_MULTIPLIER = 0.75

# Create a predefined matrix with a visible layout
matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Ensure start position is empty
start_x, start_y = GRID_SIZE // 2, GRID_SIZE // 2
matrix[start_y][start_x] = 0

# Load character images
char_images = []
for i in range(1, 13):
    img = pygame.image.load(f"Hero_move/run{i}.png")
    img = pygame.transform.scale(img, (int(cell_size * CHAR_SIZE_MULTIPLIER), int(cell_size * CHAR_SIZE_MULTIPLIER)))
    char_images.append(img)

# Load arrow images
arrow_up = pygame.image.load("arrows/yellow-!arrowup.png")
arrow_down = pygame.image.load("arrows/green-!arrowdown.png")
arrow_left = pygame.image.load("arrows/red-!arrowleft.png")
arrow_right = pygame.image.load("arrows/blue-!arrowright.png")

# Scale arrow images
arrow_size = int(WIDTH * 0.05)  # 5% of screen width
arrow_up = pygame.transform.scale(arrow_up, (arrow_size, arrow_size))
arrow_down = pygame.transform.scale(arrow_down, (arrow_size, arrow_size))
arrow_left = pygame.transform.scale(arrow_left, (arrow_size, arrow_size))
arrow_right = pygame.transform.scale(arrow_right, (arrow_size, arrow_size))

# Position arrow images
control_area_width = WIDTH - GAME_AREA_WIDTH
control_area_center = GAME_AREA_WIDTH + control_area_width // 2
arrow_margin = 10
arrow_up_rect = arrow_up.get_rect(midbottom=(control_area_center, HEIGHT - 3*arrow_size - 2*arrow_margin))
arrow_down_rect = arrow_down.get_rect(midtop=(control_area_center, HEIGHT - arrow_size - arrow_margin))
arrow_left_rect = arrow_left.get_rect(midright=(control_area_center - arrow_margin, HEIGHT - 2*arrow_size - arrow_margin))
arrow_right_rect = arrow_right.get_rect(midleft=(control_area_center + arrow_margin, HEIGHT - 2*arrow_size - arrow_margin))

# Animation variables
current_frame = 0
ANIMATION_SPEED = 10  # Frames per second for animation
last_update = time.time()

# Character position (now in pixels)
char_x, char_y = start_x * cell_size + cell_size // 2, start_y * cell_size + cell_size // 2
move_speed = 3  # Pixels per frame

# Clock for controlling game speed
clock = pygame.time.Clock()

# Button states
button_states = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

def draw_matrix():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if matrix[y][x] == 1:
                pygame.draw.rect(screen, DARK_GREEN, rect)
            else:
                pygame.draw.rect(screen, GRASS_GREEN, rect)

def can_move(x, y):
    # Calculate the grid positions for all four corners of the character sprite
    top_left_x = int((x - char_images[0].get_width() / 2) // cell_size)
    top_left_y = int((y - char_images[0].get_height() / 2) // cell_size)
    bottom_right_x = int((x + char_images[0].get_width() / 2 - 1) // cell_size)
    bottom_right_y = int((y + char_images[0].get_height() / 2 - 1) // cell_size)

    # Check if any of these positions are walls
    for check_y in range(top_left_y, bottom_right_y + 1):
        for check_x in range(top_left_x, bottom_right_x + 1):
            if check_x < 0 or check_x >= GRID_SIZE or check_y < 0 or check_y >= GRID_SIZE or matrix[check_y][check_x] == 1:
                return False
    return True

def draw_button(surface, image, rect, pressed):
    if pressed:
        # Draw a slightly smaller version of the button when pressed
        smaller_rect = rect.inflate(-5, -5)
        surface.blit(pygame.transform.scale(image, smaller_rect.size), smaller_rect)
    else:
        surface.blit(image, rect)

running = True
dx, dy = 0, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if arrow_up_rect.collidepoint(mouse_pos):
                    dy = -move_speed
                    button_states['up'] = True
                elif arrow_down_rect.collidepoint(mouse_pos):
                    dy = move_speed
                    button_states['down'] = True
                elif arrow_left_rect.collidepoint(mouse_pos):
                    dx = -move_speed
                    button_states['left'] = True
                elif arrow_right_rect.collidepoint(mouse_pos):
                    dx = move_speed
                    button_states['right'] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dx, dy = 0, 0
                button_states = {key: False for key in button_states}

    # Move character if the new position is valid
    new_x, new_y = char_x + dx, char_y + dy
    if can_move(new_x, new_y):
        char_x, char_y = new_x, new_y
    else:
        # If can't move diagonally, try moving horizontally or vertically
        if dx != 0 and dy != 0:
                char_x += dx
        elif can_move(char_x, char_y + dy):
                char_y += dy

    # Update animation frame
    now = time.time()
    if now - last_update > 1.0 / ANIMATION_SPEED:
        if dx != 0 or dy != 0:
            current_frame = (current_frame + 1) % len(char_images)
        else:
            current_frame = 0  # Reset to first frame when not moving
        last_update = now

    screen.fill(GRASS_GREEN)
    draw_matrix()
    
    # Draw the character
    char_rect = char_images[current_frame].get_rect()
    char_rect.center = (char_x, char_y)
    screen.blit(char_images[current_frame], char_rect)
    
    # Draw arrow buttons with pressed state
    draw_button(screen, arrow_up, arrow_up_rect, button_states['up'])
    draw_button(screen, arrow_down, arrow_down_rect, button_states['down'])
    draw_button(screen, arrow_left, arrow_left_rect, button_states['left'])
    draw_button(screen, arrow_right, arrow_right_rect, button_states['right'])
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
