import pygame as pg
from pygame import sprite

#need to adapt this to work for the initial screen prompts and the checkpoint prompts

class DialogBox(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, dialogue: list[str], world):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.world = world
        
        self.dialogue = dialogue

        self.lines_index = 0
        self.total_lines = len(self.dialogue["initial"]) + 1

        self.font = pg.font.Font("./assets/november.ttf", 25)

        self.image = pg.Surface((self.width, self.height))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        # options: initial, prompt, response
        self.state = "initial"
    
    def draw_lines(self, line_segments: list[str]):
        self.image.fill((255, 255, 255))
        height_index = 0
        for segment in line_segments:
            text = self.font.render(segment, True, (0, 0, 0))
            self.image.blit(text, (5, 5 + ((self.font.get_height()+2)*height_index)))
            height_index += 1
        

    def update(self):
        # TODO: state updates

        if self.state == "initial":
            # display initial dialogue text as user clicks through
            line_segments = break_line(self, self.dialogue["initial"][self.lines_index])
            self.draw_lines(line_segments)

        elif self.state == "prompt":
            text_prompt_1 = self.font.render(self.dialogue["prompt_1"], True, (0, 0, 0))
            text_prompt_2 = self.font.render(self.dialogue["prompt_2"], True, (0, 0, 0))

            # TODO generalize these, and ffs draw a box around them
            self.image.blit(text_prompt_1, (5, self.rect.height - 55))
            self.image.blit(text_prompt_2, (5, self.rect.height - 25))

        else: # response
            # display response text as user clicks through
            line_segments = break_line(self, self.dialogue[self.chosen_response][self.lines_index])
            self.draw_lines(line_segments)
            
            
    def advance_text(self):
        if self.lines_index >= self.total_lines:
            self.world.sprites.remove(self)
            self.world.set_world_state("idle_main_room")
        else:
            self.text_surface = self.font.render(self.dialogue["initial"][self.lines_index], True, (0, 0, 0))
            
    def check_click(self, p: tuple[int, int]):
        if self.rect.collidepoint(p):
            if self.state == "initial":
                # advance text
                self.lines_index += 1
                self.advance_text()                
                # advance state if done with initial dialogue
                if self.lines_index == len(self.dialogue["initial"]) - 1:
                    self.state = "prompt"

            elif self.state == "prompt":
                # if statement that sets chosen_response based on where it was clicked
                self.chosen_response = "response_1"

                self.total_lines += len(self.dialogue[self.chosen_response])
                self.state = "response"

            else: # response
                self.lines_index += 1
                self.advance_text()


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


