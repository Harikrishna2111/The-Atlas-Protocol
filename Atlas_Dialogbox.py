import pygame
import os


# AI Dialog Constants
AI_AVATAR_SIZE = (200, 200)
DIALOG_BOX_SIZE = (850, 350)
TEXT_COLOR = (0, 0, 0)
TEXT_SIZE = 20
TEXT_WIDTH = 360

# Screen and positioning constants
SCREEN_WIDTH = 1200  # Adjust as needed
SCREEN_HEIGHT = 800  # Adjust as needed

# Dialog positioning
AI_AVATAR_POS = (15, 740)
DIALOG_BOX_POS = (-30, 600)
TEXT_POS = (210, 720)

# Global variables
ai_avatar = None
dialog_box = None
game_font = None
dialog_visible = False
current_dialog_text = ""

def initialize_dialog_assets():
    global ai_avatar, dialog_box, game_font
    
    try:
        # Load and scale AI-related images
        ai_avatar = pygame.image.load(os.path.join("assets", "ai.png")).convert_alpha()
        ai_avatar = pygame.transform.scale(ai_avatar, AI_AVATAR_SIZE)

        dialog_box = pygame.image.load(os.path.join("assets", "dialog-box.png")).convert_alpha()
        dialog_box = pygame.transform.scale(dialog_box, DIALOG_BOX_SIZE)
    except pygame.error as e:
        print(f"Error loading dialog assets: {e}")
        return False
    
    # Initialize font
    pygame.font.init()
    game_font = pygame.font.Font(None, TEXT_SIZE)
    return True

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        # Handle very long words
        if font.size(word)[0] > max_width:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
            # Split long word
            while word:
                for i in range(len(word), 0, -1):
                    if font.size(word[:i])[0] <= max_width:
                        lines.append(word[:i])
                        word = word[i:]
                        break
        else:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def close_dialog():
    global dialog_visible
    dialog_visible = False

def open_dialog():
    global dialog_visible
    dialog_visible = True

def is_dialog_visible():
    return dialog_visible

def update_dialog_text(new_text):
    global current_dialog_text
    current_dialog_text = new_text

def render_ai_dialog(screen, text):
    if not dialog_visible:
        return
    
    try:
        # Draw AI avatar
        if ai_avatar is not None:
            screen.blit(ai_avatar, AI_AVATAR_POS)
        
        # Draw dialog box
        if dialog_box is not None:
            screen.blit(dialog_box, DIALOG_BOX_POS)
        
        # Wrap and render text
        if game_font is not None:
            wrapped_lines = wrap_text(text, game_font, TEXT_WIDTH)
            for i, line in enumerate(wrapped_lines):
                text_surface = game_font.render(line, True, TEXT_COLOR)
                screen.blit(text_surface, (TEXT_POS[0], TEXT_POS[1] + i * (TEXT_SIZE + 5)))
    except Exception as e:
        print(f"Error rendering dialog: {e}")
