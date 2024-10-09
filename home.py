import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 32
FPS = 60

# Create the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("The Atlas Protocol")

# Update screen dimensions and map size
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Load background image
background_image = pygame.image.load(os.path.join("assets", "map1.png")).convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = MAP_WIDTH // 2
        self.y = MAP_HEIGHT // 2
        self.direction = "down"
        self.frame = 0
        self.animation_speed = 0.2
        self.moving = False
        self.load_images()
        self.image = self.standing_image
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.target_x = self.rect.x
        self.target_y = self.rect.y

    def load_images(self):
        self.images = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }
        self.standing_image = pygame.image.load(os.path.join("character", "character_standing.png")).convert_alpha()
        
        for direction in self.images.keys():
            for i in range(9):
                img = pygame.image.load(os.path.join("character", f"character_{direction}_{i}.png")).convert_alpha()
                self.images[direction].append(img)

    def move(self, dx, dy):
        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        elif dy < 0:
            self.direction = "down"
        elif dy > 0:
            self.direction = "up"

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
            if self.frame >= 9:
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
character = Character(0, 0)  # The actual position is set in the __init__ method now
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
            elif event.key == pygame.K_UP:
                character.move(0, -1)
            elif event.key == pygame.K_DOWN:
                character.move(0, 1)
            elif event.key == pygame.K_LEFT:
                character.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                character.move(1, 0)

    all_sprites.update()

    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
