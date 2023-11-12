import pygame as pg
from pygame import sprite


class DialogBox(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, dialogue: list[str], world):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.world = world
        
        self.dialogue = dialogue

        self.lines = self.dialogue["initial"]
        self.lines_index = 0
        self.lines_count = len(self.lines)
        
        self.font = pg.font.Font("./assets/november.ttf", 25)

        self.image = pg.Surface((self.width, self.height))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        line_segments = break_line(self, self.lines[self.lines_index])
        self.image.fill((255, 255, 255))
        height_index = 0
        for segment in line_segments:
            text = self.font.render(segment, True, (0, 0, 0))
            self.image.blit(text, (5, 5 + ((self.font.get_height()+2)*height_index)))
            # self.image.blit(text, (5, 5))
            height_index += 1
            
    def check_click(self, p: tuple[int, int]):
        if self.rect.collidepoint(p):
            self.lines_index += 1
            if self.lines_index >= self.lines_count:
                self.world.sprites.remove(self)
                self.world.set_world_state("idle_main_room")
            else:
                self.text_surface = self.font.render(self.lines[self.lines_index], True, (0, 0, 0))

def break_line(self, line):
        """
        Breaks a line of text into multiple lines that fit within the width of the box, respecting word boundaries. Returns list[str] of these lines. 
        """
        broken_lines = []
        current_segment = ""
        working_line = line.split(" ")

        while len(working_line) > 0:
            # see if the current segment still fits if one more word is added to it
            if self.font.render(current_segment + " " + working_line[0], True, (0, 0, 0)).get_width() >= self.width - 10:
                # if not, add a break and reset the current segment
                broken_lines.append(current_segment + " ")
                current_segment = ""

            else:
                # else, add another word
                current_segment += " " + working_line[0]
                working_line = working_line[1:]
        broken_lines.append(current_segment)

        return broken_lines