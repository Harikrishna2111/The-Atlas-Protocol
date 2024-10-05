import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Multiple Images Example")

# Load the background image
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (width, height))

# Load the second image
# Replace 'second_image.png' with the path to your second image
second_image = pygame.image.load('play.png')

# Resize the second image
# Change these values to your desired width and height
new_width, new_height = 150,100
second_image = pygame.transform.scale(second_image, (new_width, new_height))

# Get the rect of the second image
second_image_rect = second_image.get_rect()

# Position the second image (for example, center it)
second_image_rect.center = (width // 2, height*3 // 4)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the second image
    screen.blit(second_image, second_image_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
