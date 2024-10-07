import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 32
MAP_WIDTH = 40
MAP_HEIGHT = 30
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Walking Game")

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = "down"
        self.frame = 0
        self.animation_speed = 0.2
        self.moving = False
        self.load_images()
        self.image = self.standing_image
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.target_x = self.rect.x
        self.target_y = self.rect.y

    def load_images(self):
        self.images = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }
        self.standing_image = pygame.image.load(os.path.join("images", "character_standing.png")).convert_alpha()
        
        for direction in self.images.keys():
            for i in range(4):
                img = pygame.image.load(os.path.join("images", f"character_{direction}_{i}.png")).convert_alpha()
                self.images[direction].append(img)

    def move(self, dx, dy):
        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        elif dy < 0:
            self.direction = "up"
        elif dy > 0:
            self.direction = "down"

        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            self.x = new_x
            self.y = new_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

    def update(self):
        if self.moving:
            self.frame += self.animation_speed
            if self.frame >= 4:
                self.frame = 0

            if self.rect.x < self.target_x:
                self.rect.x += 2
            elif self.rect.x > self.target_x:
                self.rect.x -= 2

            if self.rect.y < self.target_y:
                self.rect.y += 2
            elif self.rect.y > self.target_y:
                self.rect.y -= 2

            if self.rect.x == self.target_x and self.rect.y == self.target_y:
                self.moving = False

            self.image = self.images[self.direction][int(self.frame)]
        else:
            self.image = self.standing_image

# Create character
character = Character(MAP_WIDTH // 2, MAP_HEIGHT // 2)
all_sprites = pygame.sprite.Group(character)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character.move(0, -1)
            elif event.key == pygame.K_DOWN:
                character.move(0, 1)
            elif event.key == pygame.K_LEFT:
                character.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                character.move(1, 0)

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
