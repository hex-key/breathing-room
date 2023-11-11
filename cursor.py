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

screen = pygame.display.set_mode([1000, 750])

running = True

while running:
    screen.fill((255, 253, 208))
    pygame.mouse.set_visible(False)
    background = pygame.image.load("./assets/bg.png")
    new_cursor = pygame.image.load("./assets/cursor_img.png")
    background_rect = pygame.Rect(0, 0, 1000, 750)
    position = pygame.mouse.get_pos()
    screen.blit(background, background_rect)
    screen.blit(new_cursor, position)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()

pygame.quit()