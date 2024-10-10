import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 32
FPS = 60
MOVE_SPEED = 3  # Smaller step size to make movement smooth

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
        elif dy < 0:  # Fix for "up"
            self.direction = "down"
        elif dy > 0:  # Fix for "down"
            self.direction = "up"

        # Check if movement would cross the boundaries
        if 0 <= self.rect.x + dx * MOVE_SPEED <= SCREEN_WIDTH - self.rect.width:
            self.rect.x += dx * MOVE_SPEED
        if 0 <= self.rect.y + dy * MOVE_SPEED <= SCREEN_HEIGHT - self.rect.height:
            self.rect.y += dy * MOVE_SPEED

        # Set the character as moving if there's movement
        self.moving = (dx != 0 or dy != 0)

    def update(self):
        # Update character animation when moving
        if self.moving:
            self.frame += self.animation_speed
            if self.frame >= len(self.images[self.direction]):
                self.frame = 0
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

    # Handle continuous movement while the keys are held down
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1

    # Call the original move function
    character.move(dx, dy)

    # If no movement keys are pressed, set moving to False
    if dx == 0 and dy == 0:
        character.moving = False

    all_sprites.update()

    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
