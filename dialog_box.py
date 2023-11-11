import pygame as pg
from pygame import sprite

class DialogBox:
    def __init__(self, x: int, y: int, width: int, height: int, lines):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.lines = lines
        
        self.font = pg.font.Font("./assets/november.ttf", 20)
        self.text_surface = self.font.render(self.lines[0], True, (0, 0, 0))
        
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface):
        pg.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(self.text_surface, (self.x + 5, self.y + 5))
        
    def update(self):
        pass

    def check_click(self, p):
        if self.rect.collidepoint(p):
            print("clicked!")