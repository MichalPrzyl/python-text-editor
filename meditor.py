import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Prosta Gra z Pygame")

# Kolory
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_index = 0

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zmiana koloru tła
    screen.fill(colors[color_index])
    color_index = (color_index + 1) % len(colors)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Opóźnienie, aby zmiana koloru była widoczna
    pygame.time.delay(500)

# Zamykanie Pygame
pygame.quit()
sys.exit()