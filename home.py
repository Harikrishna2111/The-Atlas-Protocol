import pygame
import os
import sys

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 25
FPS = 60

# Get the screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Variable to control the width of the game map (0.0 to 1.0)
vary_width = 0.8  # Change this value to reduce the width of the game map

# Calculate game area dimensions
GAME_AREA_WIDTH = int(SCREEN_WIDTH * vary_width)
GAME_AREA_HEIGHT = SCREEN_HEIGHT

# Calculate the tile size based on the game area dimensions
TILE_SIZE = GAME_AREA_WIDTH // GRID_SIZE

# New: Add character scale factor
CHARACTER_SCALE = 0.6  # Adjust this value to make the character smaller or larger
TILE_SIZE = int(TILE_SIZE * CHARACTER_SCALE)

# New: Adjust MOVE_SPEED based on CHARACTER_SCALE
MOVE_SPEED = int(5 * CHARACTER_SCALE)  # Pixels per frame when moving

# Joystick constants
ARROW_SIZE = 64  # Size of arrow images
JOYSTICK_MARGIN = 20  # Margin between arrows
JOYSTICK_OFFSET = 200  # Distance from bottom of screen to bottom of joystick

# Create the screen in fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("The Atlas Protocol")

# Create the grid (25x25, all 0s)
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Load background image
background_image = pygame.image.load(os.path.join("assets", "map1.png")).convert()
background_image = pygame.transform.scale(background_image, (GAME_AREA_WIDTH, GAME_AREA_HEIGHT))

# Load arrow images
arrow_up = pygame.image.load(os.path.join("arrows", "arrow_up.png")).convert_alpha()
arrow_down = pygame.image.load(os.path.join("arrows", "arrow_down.png")).convert_alpha()
arrow_left = pygame.image.load(os.path.join("arrows", "arrow_left.png")).convert_alpha()
arrow_right = pygame.image.load(os.path.join("arrows", "arrow_right.png")).convert_alpha()

# Scale arrow images
arrow_up = pygame.transform.scale(arrow_up, (ARROW_SIZE, ARROW_SIZE))
arrow_down = pygame.transform.scale(arrow_down, (ARROW_SIZE, ARROW_SIZE))
arrow_left = pygame.transform.scale(arrow_left, (ARROW_SIZE, ARROW_SIZE))
arrow_right = pygame.transform.scale(arrow_right, (ARROW_SIZE, ARROW_SIZE))

# Create joystick group
joystick_group = pygame.Surface((ARROW_SIZE * 3 + JOYSTICK_MARGIN * 2, ARROW_SIZE * 3 + JOYSTICK_MARGIN * 2), pygame.SRCALPHA)

# Position arrows within the joystick group
arrow_up_rect = arrow_up.get_rect(midtop=(ARROW_SIZE * 1.5 + JOYSTICK_MARGIN, 0))
arrow_down_rect = arrow_down.get_rect(midbottom=(ARROW_SIZE * 1.5 + JOYSTICK_MARGIN, ARROW_SIZE * 3 + JOYSTICK_MARGIN * 2))
arrow_left_rect = arrow_left.get_rect(midleft=(0, ARROW_SIZE * 1.5 + JOYSTICK_MARGIN))
arrow_right_rect = arrow_right.get_rect(midright=(ARROW_SIZE * 3 + JOYSTICK_MARGIN * 2, ARROW_SIZE * 1.5 + JOYSTICK_MARGIN))

# Draw arrows on the joystick group
joystick_group.blit(arrow_up, arrow_up_rect)
joystick_group.blit(arrow_down, arrow_down_rect)
joystick_group.blit(arrow_left, arrow_left_rect)
joystick_group.blit(arrow_right, arrow_right_rect)

# Position the joystick group on the screen
joystick_x = GAME_AREA_WIDTH + (SCREEN_WIDTH - GAME_AREA_WIDTH - joystick_group.get_width()) // 2
joystick_y = SCREEN_HEIGHT - joystick_group.get_height() - JOYSTICK_OFFSET  # Adjusted to move down
joystick_rect = joystick_group.get_rect(topleft=(joystick_x, joystick_y))

# Load the sample image (uploaded image)
sample_image = pygame.image.load("assets/map1.png").convert()
sample_image = pygame.transform.scale(sample_image, (joystick_group.get_width(), joystick_group.get_height()))  # Scale it to fit the top half

# Define the area for the sample image (top half of the right column)
sample_image_rect = sample_image.get_rect(topleft=(joystick_x, joystick_y - joystick_group.get_height() - JOYSTICK_MARGIN))

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.grid_x = 0
        self.grid_y = 0
        self.pixel_x = self.grid_x * TILE_SIZE
        self.pixel_y = self.grid_y * TILE_SIZE
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
        self.standing_image = pygame.transform.scale(self.standing_image, (TILE_SIZE, TILE_SIZE))
        
        for direction in self.images.keys():
            for i in range(9):
                img = pygame.image.load(os.path.join("character", f"character_{direction}_{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.images[direction].append(img)

    def move(self, dx, dy):
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        if 0 <= new_grid_x < GRID_SIZE and 0 <= new_grid_y < GRID_SIZE and grid[new_grid_y][new_grid_x] == 0:
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.target_x = self.grid_x * TILE_SIZE
            self.target_y = self.grid_y * TILE_SIZE
            self.moving = True

            if dx < 0:
                self.direction = "left"
            elif dx > 0:
                self.direction = "right"
            elif dy < 0:
                self.direction = "up"
            elif dy > 0:
                self.direction = "down"

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()

                # Check if the mouse is inside the joystick group area
                if joystick_rect.collidepoint(mouse_pos):
                    # Calculate the relative position of the mouse within the joystick group
                    relative_pos = (mouse_pos[0] - joystick_rect.x, mouse_pos[1] - joystick_rect.y)

                    # Check which arrow button was clicked
                    if arrow_up_rect.collidepoint(relative_pos) and not character.moving:
                        character.move(0, -1)
                    elif arrow_down_rect.collidepoint(relative_pos) and not character.moving:
                        character.move(0, 1)
                    elif arrow_left_rect.collidepoint(relative_pos) and not character.moving:
                        character.move(-1, 0)
                    elif arrow_right_rect.collidepoint(relative_pos) and not character.moving:
                        character.move(1, 0)

    # Update all sprites
    all_sprites.update()

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(background_image, (0, 0))  # Draw the background
    all_sprites.draw(screen)  # Draw character
    screen.blit(sample_image, sample_image_rect.topleft)  # Draw the sample image in the top half
    screen.blit(joystick_group, joystick_rect.topleft)  # Draw joystick in the bottom half

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
