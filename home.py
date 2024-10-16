import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 25
FPS = 60
MOVE_SPEED = 2  # Pixels per frame when moving

# Get the screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
GAME_AREA_SIZE = min(SCREEN_HEIGHT, SCREEN_WIDTH)  # Leave 200 pixels on the right

# Calculate the game area size and position
TILE_SIZE = GAME_AREA_SIZE // GRID_SIZE
GAME_AREA_LEFT = 0
GAME_AREA_TOP = (SCREEN_HEIGHT - GAME_AREA_SIZE) // 2

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("The Atlas Protocol")

# Create the grid (all 0s)
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# Load background image
background_image = pygame.image.load(os.path.join("assets", "map1.png")).convert()
background_image = pygame.transform.scale(background_image, (GAME_AREA_SIZE, GAME_AREA_SIZE))

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.grid_x = GRID_SIZE // 2
        self.grid_y = GRID_SIZE // 2
        self.pixel_x = self.grid_x * TILE_SIZE + GAME_AREA_LEFT
        self.pixel_y = self.grid_y * TILE_SIZE + GAME_AREA_TOP
        self.direction = "down"
        self.frame = 0
        self.animation_speed = 0.2
        self.moving = False
        self.load_images()
        self.image = self.standing_image
        self.rect = self.image.get_rect()
        self.rect.x = self.pixel_x
        self.rect.y = self.pixel_y
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y

    def load_images(self):
        self.images = {
            "up": [], "down": [], "left": [], "right": []
        }
        self.standing_image = pygame.image.load(os.path.join("character", "character_standing.png")).convert_alpha()
        
        for direction in self.images.keys():
            for i in range(9):
                img = pygame.image.load(os.path.join("character", f"character_{direction}_{i}.png")).convert_alpha()
                self.images[direction].append(img)

    def move(self, dx, dy):
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        if 0 <= new_grid_x < GRID_SIZE and 0 <= new_grid_y < GRID_SIZE and grid[new_grid_y][new_grid_x] == 0:
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.target_x = self.grid_x * TILE_SIZE + GAME_AREA_LEFT
            self.target_y = self.grid_y * TILE_SIZE + GAME_AREA_TOP
            self.moving = True

            if dx < 0:
                self.direction = "left"
            elif dx > 0:
                self.direction = "right"
            elif dy < 0:
                self.direction = "down"
            elif dy > 0:
                self.direction = "up"

    def update(self):
        if self.moving:
            if self.pixel_x < self.target_x:
                self.pixel_x = min(self.pixel_x + MOVE_SPEED, self.target_x)
            elif self.pixel_x > self.target_x:
                self.pixel_x = max(self.pixel_x - MOVE_SPEED, self.target_x)
            
            if self.pixel_y < self.target_y:
                self.pixel_y = min(self.pixel_y + MOVE_SPEED, self.target_y)
            elif self.pixel_y > self.target_y:
                self.pixel_y = max(self.pixel_y - MOVE_SPEED, self.target_y)

            self.rect.x = self.pixel_x
            self.rect.y = self.pixel_y

            if (self.pixel_x, self.pixel_y) == (self.target_x, self.target_y):
                self.moving = False

            self.frame += self.animation_speed
            if self.frame >= len(self.images[self.direction]):
                self.frame = 0
            self.image = self.images[self.direction][int(self.frame)]
        else:
            self.image = self.standing_image

# Create character
character = Character()
all_sprites = pygame.sprite.Group(character)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif not character.moving:
                if event.key == pygame.K_UP:
                    character.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    character.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    character.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    character.move(1, 0)

    all_sprites.update()

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(background_image, (GAME_AREA_LEFT, GAME_AREA_TOP))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
