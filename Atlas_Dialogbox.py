import pygame
import os

# AI Dialog Constants
AI_AVATAR_SIZE = (200, 200)
DIALOG_BOX_SIZE = (800, 300)
TEXT_COLOR = (0, 0, 0)
TEXT_SIZE = 20
TEXT_WIDTH = 360

# Global variables
ai_avatar = None
dialog_box = None
game_font = None
AI_AVATAR_POS = None
DIALOG_BOX_POS = None
TEXT_POS = None

# Add this with your other constants
dialog_visible = False  # Track if dialog should be shown

def initialize_dialog_assets():
    """Initialize all dialog-related assets"""
    global ai_avatar, dialog_box, game_font, AI_AVATAR_POS, DIALOG_BOX_POS, TEXT_POS
    
    # Load and scale AI-related images
    ai_avatar = pygame.image.load(os.path.join("assets", "ai.png")).convert_alpha()
    ai_avatar = pygame.transform.scale(ai_avatar, AI_AVATAR_SIZE)

    dialog_box = pygame.image.load(os.path.join("assets", "dialog-box.png")).convert_alpha()
    dialog_box = pygame.transform.scale(dialog_box, DIALOG_BOX_SIZE)
    
    # Calculate positions based on screen size
    AI_AVATAR_POS = (0, 700)
    DIALOG_BOX_POS = (-75, 550)
    TEXT_POS = (150, 660)

    # Initialize font
    pygame.font.init()
    game_font = pygame.font.Font(None, TEXT_SIZE)

def wrap_text(text, font, max_width):
    """Wrap text to fit within a certain width"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        width = font.size(test_line)[0]
        
        if width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            
    lines.append(' '.join(current_line))
    return lines

def toggle_dialog():
    """Toggle the dialog visibility"""
    global dialog_visible
    dialog_visible = not dialog_visible

def render_ai_dialog(screen, text):
    """Render AI avatar, dialog box, and text"""
    global current_ai_text
    
    # Only render if dialog is visible
    if not dialog_visible:
        return
        
    if None in (ai_avatar, dialog_box, game_font):
        return  # Don't render if assets aren't initialized

    # Draw AI avatar
    screen.blit(ai_avatar, AI_AVATAR_POS)
    
    # Draw dialog box
    screen.blit(dialog_box, DIALOG_BOX_POS)
    
    # Wrap and render text
    wrapped_lines = wrap_text(text, game_font, TEXT_WIDTH)
    for i, line in enumerate(wrapped_lines):
        text_surface = game_font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (TEXT_POS[0], TEXT_POS[1] + i * (TEXT_SIZE + 5)))