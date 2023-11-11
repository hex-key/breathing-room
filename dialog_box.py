import pygame as pg
from pygame import sprite

class DialogBox:

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.lines = lines
        self.lines_index = 0
        self.lines_count = len(lines)

        self.world = world
        
        self.font = pg.font.Font("./assets/november.ttf", 20)
        self.text_surface = self.font.render(self.lines[self.lines_index], True, (0, 0, 0))
        
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface):
        pg.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(self.text_surface, (self.x + 5, self.y + 5))
        
    def update(self):
        pass

    def check_click(self, p):
        if self.rect.collidepoint(p):
            self.lines_index += 1
            if self.lines_index >= self.lines_count:
                self.world.world_dboxes.remove(self)
                self.world.state = "idle_main_room"
            else:
                self.text_surface = self.font.render(self.lines[self.lines_index], True, (0, 0, 0))
