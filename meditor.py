import pygame
import sys

class Meditor:
    def __init__(self):
        pygame.init()

        # Window
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MEDITOR v.1.0.0")

        # Colors
        self.background_color = (30, 30, 30)
        self.text_color = (255, 255, 255)
        self.status_line_text_color = (31, 31, 31)
        self.status_line_color = (131, 143, 134)

        # Font
        self.font = pygame.font.Font(None, 36)
        self.font_height = self.font.get_height()

        # MODE
        self.mode = 'normal'

        # Buffor
        self.text_buffer = ['hejka naklejka co tam ciekawego', "hejk"]

        # Status line
        self.status_line_height = 20

        # Tick
        self.last_blink_time = pygame.time.get_ticks()
        self.cursor_blink_interval = 500
        self.cursor_visible = True

        self.cursor_x = 0
        self.cursor_y = 0

        self.command_prefix_number = []

    def move_right(self):
        line = self.text_buffer[self.cursor_y]
        if self.cursor_x < len(line):
            self.cursor_x += 1

    def move_left(self):
        if self.cursor_x > 0:
            self.cursor_x -= 1

    def move_down(self):
        # If next line doesn't exist, just return current coords
        if self.cursor_y == len(self.text_buffer) - 1:
            return
        # When line below is shorter, then move cursor_x to its max length.
        if self.cursor_x > len(self.text_buffer[self.cursor_y + 1]):
            max_index = self.get_max_line_index(self.cursor_y + 1)
            self.cursor_x = max_index

        self.cursor_y += 1

    def move_up(self):
        if self.cursor_x > len(self.text_buffer[self.cursor_y - 1]):
            max_index = self.get_max_line_index(self.cursor_y - 1)
            self.cursor_x = max_index
        if self.cursor_y > 0:
            self.cursor_y -= 1

    def move_one_word_forward(self):
        line = self.text_buffer[self.cursor_y]
        new_index = self.cursor_x

        while line[new_index] != ' ':
            if new_index <= len(line) - 2:
                new_index += 1
            else:
                return new_index
        return new_index + 1

    def move_one_word_back(self):
        line = self.text_buffer[self.cursor_y]
        new_index = self.cursor_x

        while line[new_index] != ' ':
            if new_index > 0:
                new_index -= 1
            else:
                return new_index
        return new_index - 1

    def get_max_line_index(self, y_index):
        line = self.text_buffer[y_index]
        return len(line) - 1

    def clear_command_prefix(self):
        self.command_prefix_number = []

    def handle_keydown_event(self, event):
        if event.key == pygame.K_RETURN:  # Return key
            self.text_buffer.insert(self.cursor_y + 1, self.text_buffer[self.cursor_y][self.cursor_x:])
            self.text_buffer[self.cursor_y] = self.text_buffer[self.cursor_y][:self.cursor_x]
            self.move_down()
            self.cursor_x = 0
        elif event.key == pygame.K_BACKSPACE:  # Backspace key
            if self.text_buffer and self.text_buffer[-1]:
                self.text_buffer[self.cursor_y] = self.text_buffer[self.cursor_y][:self.cursor_x - 1] + self.text_buffer[self.cursor_y][self.cursor_x:]
                self.move_left()

            elif self.text_buffer:
                self.text_buffer.pop()
        elif event.key == pygame.K_DELETE:  # Delete key
            self.text_buffer[self.cursor_y] = self.text_buffer[self.cursor_y][:self.cursor_x] + self.text_buffer[self.cursor_y][self.cursor_x + 1:]

        else:  # Add new chars
            # NORMAL MODE
            if self.mode == 'normal':
                # TODO: Refactor prefixes
                if self.command_prefix_number:
                    command_prefix_number_str = [str(el) for el in self.command_prefix_number]
                    prefix = "".join(command_prefix_number_str)
                else:
                    prefix = 1

                if event.unicode == 'l':
                    for _ in range(int(prefix)):
                        self.move_right()
                    self.clear_command_prefix()

                elif event.unicode == 'h':
                    for _ in range(int(prefix)):
                        self.move_left()
                    self.clear_command_prefix()

                elif event.unicode == 'j':
                    for _ in range(int(prefix)):
                        self.move_down()
                    self.clear_command_prefix()

                elif event.unicode == 'k':
                    for _ in range(int(prefix)):
                        self.move_up()
                    self.clear_command_prefix()

                elif event.unicode == 'i':
                    self.mode = 'insert'

                elif event.unicode == 'w':
                    for _ in range(int(prefix)):
                        self.cursor_x = self.move_one_word_forward()
                    self.clear_command_prefix()

                elif event.unicode == 'b':
                    for _ in range(int(prefix)):
                        self.cursor_x = self.move_one_word_back()
                    self.clear_command_prefix()

                elif event.unicode == 'o':
                    self.text_buffer.insert(self.cursor_y + 1, "")
                    self.move_down()
                    self.cursor_x = 0
                    self.mode = "insert"

                elif event.unicode == '0':
                    self.cursor_x = 0

                elif event.unicode == '^':
                    self.cursor_x = 0

                elif event.unicode == '$':
                    self.cursor_x = self.get_max_line_index(self.cursor_y)

                elif pygame.K_0 <= event.key <= pygame.K_9:
                    # Pressed number is just char, for example '3'.
                    pressed_number = event.key - pygame.K_0

                    # If there are already 5 elements in prefix, remove the first one.
                    if len(self.command_prefix_number) == 5:
                        self.command_prefix_number.pop(0)

                    # Add pressed number to prefix
                    self.command_prefix_number.append(pressed_number)

            # INSERT MODE
            elif self.mode == 'insert':
                if event.key == pygame.K_ESCAPE:
                    self.mode = 'normal'
                elif event.key == pygame.K_RSHIFT:
                    pass
                elif event.key == pygame.K_TAB:
                    self.text_buffer[self.cursor_y] = self.text_buffer[self.cursor_y][:self.cursor_x] + '    ' + self.text_buffer[self.cursor_y][self.cursor_x:]
                    self.cursor_x += 4
                else:
                    if not self.text_buffer:
                        self.text_buffer.append("")
                    self.text_buffer[self.cursor_y] = self.text_buffer[self.cursor_y][:self.cursor_x] + event.unicode + self.text_buffer[self.cursor_y][self.cursor_x:]
                    self.cursor_x += 1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown_event(event)

            # Background fill
            self.screen.fill(self.background_color)

            # Render text
            y_offset = 0
            for line in self.text_buffer:
                text_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(text_surface, (10, 10 + y_offset))
                y_offset += self.font_height

            # Render cursor rectangle
            current_time = pygame.time.get_ticks()
            if current_time - self.last_blink_time > self.cursor_blink_interval:
                self.cursor_visible = not self.cursor_visible
                self.last_blink_time = pygame.time.get_ticks()

            if self.cursor_visible:
                try:
                    letter = self.text_buffer[self.cursor_y][self.cursor_x]
                except IndexError:
                    letter = 'o'
                letter_width, _ = self.font.size(letter)
                cursor_color = (50, 168, 82)
                cursor_x_to_draw = self.font.size(self.text_buffer[self.cursor_y][:self.cursor_x])
                cursor_y_to_draw = self.cursor_y * self.font_height + 10
                pygame.draw.rect(self.screen, cursor_color, (cursor_x_to_draw[0] + 10, cursor_y_to_draw, letter_width, self.font_height))

            # Draw status line.
            pygame.draw.rect(self.screen, self.status_line_color, (0, self.screen_height - self.status_line_height,
                                                                    self.screen_width, self.status_line_height))

            status_line_font = pygame.font.Font(None, 20)
            status_line_text_surface = status_line_font.render(f'mode: {self.mode}', True, self.status_line_text_color)
            self.screen.blit(status_line_text_surface, (0 + 10, self.screen_height - self.status_line_height + self.status_line_height // 5))

            # Draw command prefix number.
            command_display_text_surface = status_line_font.render(f'command: {self.command_prefix_number}', True, self.status_line_text_color)
            self.screen.blit(
                command_display_text_surface,
                (self.screen_width - 250, self.screen_height - self.status_line_height + self.status_line_height / 5))

            # Draw line and column position.
            line_column_display_text_surface = status_line_font.render(f'line: {self.cursor_y}, column: {self.cursor_x}', True, self.status_line_text_color)
            self.screen.blit(
                line_column_display_text_surface,
                (self.screen_width - 450, self.screen_height - self.status_line_height + self.status_line_height / 5))

            # Update screen.
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    meditor = Meditor()
    meditor.run()