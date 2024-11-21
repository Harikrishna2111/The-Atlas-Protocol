import pygame
import pygame.freetype
import os
import sys
from Atlas_Dialogbox import render_ai_dialog, initialize_dialog_assets, close_dialog, open_dialog
from database import component_selector, component_count_holder, component_weights
from text2speech import speak_text
from Atlas_AI import ComponentManager, interact_with_atlas

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

initialize_dialog_assets()

# Constants
GRID_SIZE = 25  # This will remain 25x25 for grid logic
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
TILE_SIZE = GAME_AREA_WIDTH // GRID_SIZE  # Calculate without scaling
CHARACTER_SCALE = 0.9  # Adjust this value to make the character smaller or larger
CHARACTER_SIZE = int(TILE_SIZE * CHARACTER_SCALE)  # Scale character separately

# Move speed adjustment based on CHARACTER_SCALE
MOVE_SPEED = int(5 * CHARACTER_SCALE)  # Pixels per frame when moving

state = 0

# Joystick constants
ARROW_SIZE = 64  # Size of arrow images
JOYSTICK_MARGIN = 0 # Margin between arrows
JOYSTICK_OFFSET = 250  # Distance from bottom of screen to bottom of joystick

# Create the screen in fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("The Atlas Protocol")
 
# Initialize dialog assets
initialize_dialog_assets()

# Create the grid (25x25, all 0s)
grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0],
     [1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0],
     [1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0],
     [1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0],
     [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
component_map = {
        0: "No Components Found",
        1: "You found a Camera",
        2: "You found a GPS",
        3: "You found a Processor",
        4: "You found a Data Storage",
        5: "You found a NLP component",
        6: "You found a Communication component"    
        }
component = {
        0: "No Components Found",
        1: "Camera",
        2: "GPS",
        3: "ALU",
        4: "Data Storage",
        5: "NLP",
        6: "Communication"    
        }
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
sample_image = pygame.image.load("assets/components/frame.png").convert_alpha()
sample_image = pygame.transform.scale(sample_image, (300, 300))  # Scale it to fit the top half
# Add this near your other image loading code
overlay_image = pygame.image.load("assets/components/" + str(state) + ".png").convert_alpha()  # Replace with your image path
overlay_image = pygame.transform.scale(overlay_image, (150, 150))  # Same size as sample_image

# Load the collect image
collect_image = pygame.image.load("assets/collect.png").convert_alpha()
collect_image = pygame.transform.scale(collect_image, (150, 50))  # Adjust size as needed
COLLECT_IMAGE_X = GAME_AREA_WIDTH + 100  # Horizontal center of game area
COLLECT_IMAGE_Y = GAME_AREA_HEIGHT - 525 # 150 pixels from bottom of game area

# Define overlay position coordinates directly
overlay_x =  1380
overlay_y =  90
overlay_rect = overlay_image.get_rect(topleft=(overlay_x, overlay_y))

FONT_SIZE = 24
TEXT_COLOR = (255, 255, 255)  # White text
TEXT_POSITION = (GAME_AREA_WIDTH + 50, 325)  # Position in right panel
font = pygame.font.Font("C:/Windows/Fonts/Arial.ttf", FONT_SIZE)
# Function to render text
def draw_text(screen, text, position):
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, position)

# Add a boolean control variable
show_overlay = True  # You can toggle this to True when needed

# Initial character position (in grid coordinates)
CHAR_START_X = 19
CHAR_START_Y = 13  

# Chatbot components
len_return_txt = 0
INPUT_BOX_HEIGHT = 40
INPUT_BOX_WIDTH = 300
OUTPUT_BOX_HEIGHT = 150
OUTPUT_BOX_WIDTH = 300
INPUT_BOX_COLOR_INACTIVE = pygame.Color('lightskyblue3')
INPUT_BOX_COLOR_ACTIVE = pygame.Color('dodgerblue2')
TEXT_COLOR = pygame.Color('white')
PLACEHOLDER_COLOR = pygame.Color('gray')

class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = INPUT_BOX_COLOR_INACTIVE
        self.text = ''
        self.active = False
        self.font = pygame.font.Font(None, 24)
        self.placeholder = "Type here..."
        self.txt_surface = self.font.render(self.placeholder, True, PLACEHOLDER_COLOR)
        self.max_chars = 100  # Increased character limit
        self.scroll_offset = 0  # Track horizontal scroll position

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = INPUT_BOX_COLOR_ACTIVE
            else:
                self.active = False
                self.color = INPUT_BOX_COLOR_INACTIVE
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN and self.text.strip():
                    response = self.process_input(self.text)
                    self.text = ''
                    self.scroll_offset = 0  # Reset scroll when clearing text
                    self.update_surface()
                    return response
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    # Adjust scroll offset when deleting
                    if self.scroll_offset > 0:
                        self.scroll_offset = max(0, self.scroll_offset - 5)
                    self.update_surface()
                else:
                    # Add character if we're not exceeding the maximum
                    if len(self.text) < self.max_chars:
                        self.text += event.unicode
                        self.update_surface()
                        # Adjust scroll offset if text exceeds box width
                        self.adjust_scroll()
        return None

    def adjust_scroll(self):
        text_width = self.txt_surface.get_width()
        box_width = self.rect.width - 10  # Account for padding
        
        if text_width > box_width:
            # Scroll to show the end of the text
            self.scroll_offset = text_width - box_width
        else:
            self.scroll_offset = 0

    def update_surface(self):
        if self.text:
            self.txt_surface = self.font.render(self.text, True, TEXT_COLOR)
        else:
            self.txt_surface = self.font.render(self.placeholder, True, PLACEHOLDER_COLOR)

    def draw(self, screen):
        # Draw the text box background
        pygame.draw.rect(screen, pygame.Color('black'), self.rect)
        
        # Create a surface for clipping
        clip_rect = pygame.Rect(self.rect.x + 5, self.rect.y, self.rect.width - 10, self.rect.height)
        screen.set_clip(clip_rect)
        
        # Draw the text with scroll offset
        text_pos = (self.rect.x + 5 - self.scroll_offset, self.rect.y + 5)
        screen.blit(self.txt_surface, text_pos)
        
        # Reset clip
        screen.set_clip(None)
        
        # Draw the box border
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def process_input(self, text):
        # Add your chatbot logic here
        return f"Bot: " + interact_with_atlas(text, comp_manager)


class OutputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = INPUT_BOX_COLOR_INACTIVE
        self.text = []  # List to store messages
        self.font = pygame.font.Font(None, 24)
        self.line_height = 35
        self.padding = 10
        self.visible_lines = (h - 2 * self.padding) // self.line_height
        self.text_surface = pygame.Surface((w - 2 * self.padding, h - 2 * self.padding))
        self.max_line_width = w - 2 * self.padding

    def wrap_text(self, text):
        words = text.split()
        lines = []
        current_line = []
        current_width = 0


        for word in words:
            # Render the word to calculate its width
            word_width = self.font.render(word, True, pygame.Color('white')).get_width()

            if current_width + word_width <= self.max_line_width:
                current_line.append(word)
                # Add word width + space width to current line width
                current_width += word_width + self.font.size(' ')[0]
            else:
                # Add the current line to lines and reset for the next line
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        # Add the last line if it exists
        if current_line:
            lines.append(' '.join(current_line))

        return lines


    def add_message(self, message):
        """Add a new message to the chat box"""
        if isinstance(message, str):  # Make sure message is a string
            wrapped_lines = self.wrap_text(message)
            self.text.extend(wrapped_lines)
            
            # Keep only the messages that can be displayed
            while len(self.text) > self.visible_lines:
                self.text.pop(0)  # Remove oldest messages

    def draw(self, screen):
        """Draw the chat box and its contents"""
        # Draw the box background
        pygame.draw.rect(screen, pygame.Color('black'), self.rect)
        
        # Clear the text surface
        self.text_surface.fill(pygame.Color('black'))
        
        # Draw messages from bottom to top
        y_offset = self.text_surface.get_height()
        
        # Iterate through messages in reverse order
        for message in reversed(self.text):
            if isinstance(message, str):  # Ensure message is a string
                txt_surface = self.font.render(message, True, TEXT_COLOR)
                # Position text from bottom
                y_offset -= self.line_height
                if y_offset >= 0:  # Only draw if within bounds
                    self.text_surface.blit(txt_surface, (0, y_offset))
        
        # Draw the text surface onto the screen
        screen.blit(self.text_surface, 
                   (self.rect.x + self.padding, 
                    self.rect.y + self.padding))
        
        # Draw the box border
        pygame.draw.rect(screen, self.color, self.rect, 2)


comp_manager = ComponentManager()

async def process_message(input_text):
    # # Add both user input and response to output box
    # output_box.add_message(f"You: {input_text}")
    # Add bot response (this is just an example)
    response = f"Bot: " + await interact_with_atlas(input_text, comp_manager)
    output_box.add_message(response)

# Add these lines after creating your screen
input_box_x = GAME_AREA_WIDTH + (SCREEN_WIDTH - GAME_AREA_WIDTH - INPUT_BOX_WIDTH) // 2 
input_box_y = SCREEN_HEIGHT - JOYSTICK_OFFSET // 2 + 80
input_box = InputBox(input_box_x, input_box_y, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)

output_box_x = input_box_x
output_box_y = input_box_y - OUTPUT_BOX_HEIGHT - 10
output_box = OutputBox(output_box_x, output_box_y, OUTPUT_BOX_WIDTH, OUTPUT_BOX_HEIGHT)
output_box.add_message("Welcome to Atlas AI!")


show_collect_image = True
spoke = False
collected = False
current_ai_text = component_map[state] 


# Define the area for the sample image (top half of the right column)
SAMPLE_IMAGE_OFFSET = 210  # Adjust this value to move the image higher or lower
sample_image_rect = sample_image.get_rect(topleft=(joystick_x-35, joystick_y - joystick_group.get_height() - JOYSTICK_MARGIN - SAMPLE_IMAGE_OFFSET - 50))

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.grid_x = CHAR_START_X
        self.grid_y = CHAR_START_Y
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
        self.standing_image = pygame.transform.scale(self.standing_image, (CHARACTER_SIZE, CHARACTER_SIZE))
        
        for direction in self.images.keys():
            for i in range(9):
                img = pygame.image.load(os.path.join("character", f"character_{direction}_{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
                self.images[direction].append(img)

    def move(self, dx, dy):
        # Calculate new grid position
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        # Check boundaries and grid value
        if (0 <= new_grid_x < GRID_SIZE and 0 <= new_grid_y < GRID_SIZE
                and grid[new_grid_y][new_grid_x] == 0):  # Ensure target grid value is 0
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.target_x = self.grid_x * TILE_SIZE
            self.target_y = self.grid_y * TILE_SIZE
            self.moving = True

            # Set direction for animation
            if dx < 0:
                self.direction = "left"
            elif dx > 0:
                self.direction = "right"
            elif dy < 0:
                self.direction = "down"
            elif dy > 0:
                self.direction = "up"
            
            state = component_selector() 


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
    # Check state and display dialog
    if state != 0:
        # Get the appropriate message from component_map
        message = component_map.get(state, "No Components Found")
        # Open the dialog with the message
        open_dialog()
        render_ai_dialog(screen, message)
        
    else:
        close_dialog()

    overlay_image = pygame.image.load("assets/components/" + str(state) + ".png").convert_alpha()  # Replace with your image path
    overlay_image = pygame.transform.scale(overlay_image, (150, 150)) 
    for event in pygame.event.get():
        response = input_box.handle_event(event)
        if response:
            output_box.add_message(response)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                character.move(0, -1)
                state = component_selector()
                collected = False
            elif event.key == pygame.K_DOWN:
                character.move(0, 1)
                state = component_selector()
                collected = False
            elif event.key == pygame.K_LEFT:
                character.move(-1, 0)
                state = component_selector()
                collected = False
            elif event.key == pygame.K_RIGHT:
                character.move(1, 0)
                state = component_selector()
                collected = False
            if event.key == pygame.K_RETURN and input_box.text.strip():
                message = input_box.text
                process_message(message)
                input_box.text = ''  # Clear input box

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                collect_rect = collect_image.get_rect(topleft=(COLLECT_IMAGE_X, COLLECT_IMAGE_Y))
                if collect_rect.collidepoint(mouse_pos):
                    show_collect_image = False
                    collected = True
                    component_count_holder[state - 1] += 1
                    if component_count_holder[state - 1] >= 1:
                        component_weights[state] = 0
                        current_ai_text = (comp_manager.component_found(component[state]))['text']



                # Check if the mouse is inside the joystick group area
                if joystick_rect.collidepoint(mouse_pos):
                    # Calculate the relative position of the mouse within the joystick group
                    relative_pos = (mouse_pos[0] - joystick_rect.x, mouse_pos[1] - joystick_rect.y)
                    # Determine the direction based on relative position
                    if arrow_up_rect.collidepoint(relative_pos):
                        character.move(0, -1)  # Move up
                        state = component_selector()
                        spoke = False  # Reset spoke flag when moving
                        collected = False
                    elif arrow_down_rect.collidepoint(relative_pos):
                        character.move(0, 1)   # Move down
                        state = component_selector()
                        spoke = False  # Reset spoke flag when moving
                        collected = False
                    elif arrow_left_rect.collidepoint(relative_pos):
                        character.move(-1, 0)  # Move left
                        state = component_selector()
                        spoke = False  # Reset spoke flag when moving
                        collected = False
                    elif arrow_right_rect.collidepoint(relative_pos):
                        character.move(1, 0)   # Move right
                        state = component_selector()
                        spoke = False  # Reset spoke flag when moving
                        collected = False




    # Clear screen
    screen.fill((0,0,0))

    # Draw background image in game area
    screen.blit(background_image, (0, 0))
    # Display collect image when state is not 0
    if state != 0:
        collect_image_rect = collect_image.get_rect()
        collect_image_rect.center = (COLLECT_IMAGE_X, COLLECT_IMAGE_Y)
        if not collected:
            screen.blit(collect_image, (COLLECT_IMAGE_X, COLLECT_IMAGE_Y))
    if state != 0:
        open_dialog()  # Make sure the dialog is open
        render_ai_dialog(screen, current_ai_text)
        if not spoke:  # Check if we haven't spoken yet
            current_ai_text = comp_manager.component_found(component[state])['text']

            speak_text(current_ai_text)
            len_return_txt += len(current_ai_text)
            spoke = True  # Set the flag after speaking
            print(len_return_txt)
    else:
        close_dialog()
        spoke = False  # Reset the flag when no component is selected

    # Draw joystick group
    screen.blit(joystick_group, joystick_rect)

    # Draw sample image in top half
    screen.blit(sample_image, sample_image_rect)
    
    if show_overlay:
        screen.blit(overlay_image, overlay_rect)  # Using separate overlay_rect

    # Update character position and animations
    all_sprites.update()
    all_sprites.draw(screen)

    input_box.draw(screen)
    output_box.draw(screen)
    
    
    draw_text(screen, component_map[state], TEXT_POSITION)


    # Update display
    pygame.display.flip()
    clock.tick(FPS)
    

pygame.quit()
sys.exit()

