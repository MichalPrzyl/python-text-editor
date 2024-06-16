import pygame
import sys

pygame.init()

# Window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MEDITOR v.1.0.0")

# Colors
background_color = (30, 30, 30)
text_color = (255, 255, 255)

# Font
font = pygame.font.Font(None, 36)

# MODE
mode = 'normal'

# Buffor
text_buffer = ['hejka naklejka co tam ciekawego', "hejk"]

# Status line
status_line_text_color = (31, 31, 31)
status_line_color = (131, 143, 134)
status_line_height = 20

# Tick
last_blink_time = pygame.time.get_ticks()
cursor_blink_interval = 500
cursor_visible = True
    
cursor_pos = (0, 0)  # (line, column)
font_height = font.get_height()

def move_right(cursor_pos):
    cursor_pos = (cursor_pos[0] + 1, cursor_pos[1])
    return cursor_pos

def move_left(cursor_pos):
    cursor_pos = (cursor_pos[0] - 1, cursor_pos[1])
    return cursor_pos

def move_down(cursor_pos):
    cursor_pos = (cursor_pos[0], cursor_pos[1] + 1)
    return cursor_pos

def move_up(cursor_pos):
    cursor_pos = (cursor_pos[0], cursor_pos[1] - 1)
    return cursor_pos


# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Return key
                text_buffer.append("")
            elif event.key == pygame.K_BACKSPACE:  # Backspace key
                if text_buffer and text_buffer[-1]:
                    text_buffer[-1] = text_buffer[-1][:-1]
                elif text_buffer:
                    text_buffer.pop()
            else:  # Add new chats
                # NORMAL MODE
                if mode == 'normal':
                    if event.unicode == 'l':
                        cursor_pos = move_right(cursor_pos)
                    elif event.unicode == 'h':
                        cursor_pos = move_left(cursor_pos)
                    elif event.unicode == 'j':
                        cursor_pos = move_down(cursor_pos)
                    elif event.unicode == 'k':
                        cursor_pos = move_up(cursor_pos)
                    elif event.unicode == 'i':
                        mode = 'insert'


                # INSERT MODE
                elif mode == 'insert':
                    if event.key == pygame.K_ESCAPE:
                        mode = 'normal'

                    if not text_buffer:
                        text_buffer.append("")
                    text_buffer[-1] += event.unicode

    # Background fill
    screen.fill(background_color)

    # Render text
    y_offset = 0
    for line in text_buffer:
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (10, 10 + y_offset))
        y_offset += font_height

    # Render cursor rectangle
    current_time = pygame.time.get_ticks()
    if current_time - last_blink_time > cursor_blink_interval:
        cursor_visible = not cursor_visible
        last_blink_time = pygame.time.get_ticks()
        print(f"cursor_pos: {cursor_pos}")

    if True:
        cursor_color = (50, 168, 82)

        cursor_pos_lol = font.size(text_buffer[cursor_pos[1]][:cursor_pos[0]])
        cursor_x = cursor_pos[0] + 10
        cursor_y = cursor_pos[1] * font_height + 10
        print(f"cursor_y: {cursor_y}")
        pygame.draw.rect(screen, cursor_color, (cursor_pos_lol[0] + 10, cursor_y, 10, font_height))

    # draw status line
    pygame.draw.rect(screen, status_line_color, (0, screen_height - status_line_height,
                                                 screen_width, status_line_height))
    
    status_line_font =  pygame.font.Font(None, 20)
    status_line_text_surface = status_line_font.render(f'mode: {mode}', True, status_line_text_color)
    screen.blit(
        status_line_text_surface, 
        (0 + 10, screen_height - status_line_height + status_line_height/5))


    # Update screen
    pygame.display.flip()

# Close
pygame.quit()
sys.exit()
