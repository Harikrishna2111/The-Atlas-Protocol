import pygame
import subprocess

pygame.init()

# Set the display mode to full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Images Overlay")

# Load and scale the background image
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, screen.get_size())

# Load the foreground image (play button)
foreground = pygame.image.load("play.png")
 
# Load the logo image
logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (400, 500)) 

# Reduce the size of the foreground image (play button)
new_width = 200
new_height = 100 
foreground = pygame.transform.scale(foreground, (new_width, new_height))

# Get the size of the screen and the foreground image
screen_width, screen_height = screen.get_size()
fg_width, fg_height = foreground.get_rect().size

# Calculate position to center the foreground image (play button)
fg_x = (screen_width - fg_width) // 2
fg_y = 750

# Calculate position for the logo (centered horizontally, near the top vertically)
logo_width, logo_height = logo.get_rect().size
logo_x = (screen_width - logo_width) // 2
logo_y = 50  # You can adjust this value to position the logo higher or lower

# InputBox class
class InputBox:
    def __init__(self, x, y, w, h, text='', placeholder=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.placeholder = placeholder
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text or placeholder, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text or self.placeholder, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        text = self.text or self.placeholder
        color = self.color if self.text else pygame.Color('dodgerblue2')
        self.txt_surface = self.font.render(text, True, color)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create two input boxes
input_box1 = InputBox((screen_width - fg_width) // 2, 650, 140, 32, placeholder='Name')
input_box2 = InputBox((screen_width - fg_width) // 2, 700, 140, 32, placeholder='Password')
input_boxes = [input_box1, input_box2]

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
        for box in input_boxes:
            box.handle_event(event)

    for box in input_boxes:
        box.update()

    # Draw the background
    screen.blit(background, (0, 0))
    
    # Draw the logo
    screen.blit(logo, (logo_x, logo_y))
    
    # Draw the foreground image (play button)
    screen.blit(foreground, (fg_x, fg_y))

    # Draw the input boxes
    for box in input_boxes:
        box.draw(screen)

    pygame.display.update()

pygame.quit()
