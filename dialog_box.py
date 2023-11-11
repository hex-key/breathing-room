import pygame as pg
from pygame import sprite

class DialogBox:
    def __init__(self, screen: sprite, x: int, y: int, width: int, height: int, text: str):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.text = text
        
        self.font = pg.font.Font("./assets/november.ttf", 20)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        pg.draw.rect(self.screen, (255, 255, 255), self.rect)
        self.screen.blit(self.text_surface, (self.x + 5, self.y + 5))
        
    def update(self):
        pass