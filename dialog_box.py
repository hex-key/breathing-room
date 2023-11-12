import pygame as pg
from pygame import sprite

class DialogBox:
    def __init__(self, x: int, y: int, width: int, height: int, lines, world):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.font = pg.font.Font("./assets/november.ttf", 25)
        
        self.lines = lines
        self.lines_index = 0
        self.lines_count = len(lines)

        self.world = world
        
        self.text_surface = self.font.render(self.lines[self.lines_index], True, (0, 0, 0))
        
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface):
        pg.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(self.text_surface, (self.x + 5, (self.y + 5) + (20 * )))
        
    def update(self):
        pass

    def check_click(self, p):
        if self.rect.collidepoint(p):
            self.lines_index += 1
            if self.lines_index >= self.lines_count:
                self.world.world_dboxes.remove(self)
                self.world.state = "idle_main_room"
            else:
                self.text_surface = self.font.render(self.break_lines(self.lines[self.lines_index]), True, (0, 0, 0))

    def break_lines(self, line):
        """
        Breaks a line of text into multiple lines that fit within the width of the box, respecting word boundaries. Returns list[str] of these lines. 
        """
        broken_lines = ""
        current_segment = ""
        working_line = line.split(" ")

        while len(working_line) > 0:
            # see if the current segment still fits if one more word is added to it
            if self.font.render(current_segment + " " + working_line[0], True, (0, 0, 0)).get_width() >= self.width - 10:
                # if not, add a break and reset the current segment
                broken_lines += (current_segment + "\n")
                current_segment = ""
                print("1 - current segment: " + current_segment)
            else:
                # else, add another word
                current_segment += " " + working_line[0]
                working_line = working_line[1:]
                print("2 - current segment: " + current_segment)

        return broken_lines.strip("\n")
