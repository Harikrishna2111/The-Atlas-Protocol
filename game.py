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