import pygame

pygame.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

screen = pygame.display.set_mode([500, 500])

running = True

while running:
    new_cursor = pygame.image.load("cursor_img.png")
    screen.fill((255, 253, 208))
    pygame.mouse.set_visible(False)
    position = pygame.mouse.get_pos()
    screen.blit(new_cursor, position)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()

pygame.quit()