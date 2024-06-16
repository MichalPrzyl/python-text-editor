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
    
cursor_x = 0
cursor_y = 0

font_height = font.get_height()

def move_right(cursor_x):
    cursor_x +=1 
    return cursor_x

def move_left(cursor_x):
    cursor_x -= 1
    return cursor_x

def move_down(cursor_y):
    cursor_y += 1
    return cursor_y

def move_up(cursor_y):
    cursor_y -= 1
    return cursor_y

def move_one_word_forward():
    line = text_buffer[cursor_y]
    new_index = cursor_x

    while line[new_index] != ' ':
        if new_index <= len(line) - 2:
            new_index += 1
        else:
            return new_index
    return new_index + 1
    
def move_one_word_back():
    line = text_buffer[cursor_y]
    new_index = cursor_x

    while line[new_index] != ' ':
        if new_index <= len(line) - 2:
            new_index -= 1
        else:
            return new_index
    return new_index - 1
    

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Return key
                text_buffer.insert(cursor_y + 1, text_buffer[cursor_y][cursor_x:])
                text_buffer[cursor_y] = text_buffer[cursor_y][:cursor_x]
                cursor_y = move_down(cursor_y)
                cursor_x = 0
            elif event.key == pygame.K_BACKSPACE:  # Backspace key
                if text_buffer and text_buffer[-1]:
                    text_buffer[cursor_y] = text_buffer[cursor_y][:cursor_x - 1] + text_buffer[cursor_y][cursor_x:]
                    cursor_x = move_left(cursor_x)

                elif text_buffer:
                    text_buffer.pop()
            else:  # Add new chats
                # NORMAL MODE
                if mode == 'normal':
                    if event.unicode == 'l':
                        cursor_x = move_right(cursor_x)
                    elif event.unicode == 'h':
                        cursor_x = move_left(cursor_x)
                    elif event.unicode == 'j':
                        cursor_y = move_down(cursor_y)
                    elif event.unicode == 'k':
                        cursor_y = move_up(cursor_y)
                    elif event.unicode == 'i':
                        mode = 'insert'
                    elif event.unicode == 'w':
                        cursor_x = move_one_word_forward()
                    elif event.unicode == 'b':
                        cursor_x = move_one_word_back()

                    elif event.unicode == 'o':
                        text_buffer.insert(cursor_y + 1, "")
                        cursor_y = move_down(cursor_y)
                        cursor_x = 0
                        mode = "insert"
                    elif event.unicode == '0':
                        cursor_x = 0


                # INSERT MODE
                elif mode == 'insert':
                    if event.key == pygame.K_ESCAPE:
                        mode = 'normal'
                    elif event.key == pygame.K_RSHIFT:
                        pass

                    else:
                        if not text_buffer:
                            text_buffer.append("")
                        text_buffer[cursor_y] = text_buffer[cursor_y][:cursor_x] + event.unicode + text_buffer[cursor_y][cursor_x:]
                        # move_right(cursor_x)
                        cursor_x = move_right(cursor_x)

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

    if True:
        cursor_color = (50, 168, 82)
        # print(f"cursor_x: {cursor_x}")
        # print(f"cursor_y: {cursor_y}")
        # print(f"text_buffer: {text_buffer}")
        cursor_x_to_draw = font.size(text_buffer[cursor_y][:cursor_x])
        cursor_y_to_draw = cursor_y * font_height + 10
        pygame.draw.rect(screen, cursor_color, (cursor_x_to_draw[0] + 10, cursor_y_to_draw, 10, font_height))

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
