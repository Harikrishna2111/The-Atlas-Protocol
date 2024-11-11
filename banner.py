import pygame
import subprocess

pygame.init()

# Set the display mode to full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("The Atlas Protocol")

# Load and scale the background image
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, screen.get_size())

# Load the foreground image (play button)
foreground = pygame.image.load("assets/play.png")
foreground = pygame.transform.scale(foreground, (400, 200))

# Load the logo image
logo = pygame.image.load("assets/logo.png")
logo = pygame.transform.scale(logo, (400, 500)) 

# Get the size of the screen and the foreground image
screen_width, screen_height = screen.get_size()
fg_width, fg_height = foreground.get_rect().size

# Calculate position for the logo (centered horizontally, near the top vertically)
logo_width, logo_height = logo.get_rect().size
logo_x = (screen_width - logo_width) // 2
logo_y = 50  # You can adjust this value to position the logo higher or lower

# Calculate position to center the foreground image (play button)
fg_x = logo_x
fg_y = logo_y+550

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the play button is clicked
            mouse_pos = pygame.mouse.get_pos()
            if fg_x <= mouse_pos[0] <= fg_x + fg_width and fg_y <= mouse_pos[1] <= fg_y + fg_height:
                # Run the home.py file
                pygame.quit()
                subprocess.run(["python", "home.py"])
                running = False

    # Draw the background
    screen.blit(background, (0, 0))
    
    # Draw the logo
    screen.blit(logo, (logo_x, logo_y))
    
    # Draw the foreground image (play button)
    screen.blit(foreground, (fg_x, fg_y))

    pygame.display.update()

pygame.quit()
