import pygame as pg
import os, sys
import json

from dialog_box import DialogBox as DBox

class button:
    text = ""

CAPTION = "game with story 🦣"
SCREEN_SIZE = (1000, 750)

class Button(object):
    def __init__(self, p, w, lines):
        self.size = (50, 50)
        self.rect = pg.Rect((0,0), self.size)
        self.rect.center = p

        self.world = w

        self.dialogue = lines
    
    def draw(self, surface):
        surface.fill(pg.Color("red"), self.rect)

    def check_click(self, p):
        if self.rect.collidepoint(p):
            self.world.world_buttons.remove(self)
            self.world.world_dboxes.append(DBox(100, 500, 500, 200, self.dialogue, self.world))
            self.world.state = "active_dialogue"


class World(object):
    def __init__(self, a):
        with open("./dialogue.json", "r") as f:
            self.dialogue = json.load(f)
        self.app = a

        self.world_buttons = []
        self.world_dboxes = []

        self.screen_object_arrays = []
        self.screen_object_arrays.append(self.world_buttons)
        self.screen_object_arrays.append(self.world_dboxes)

        # World status options
        #   active_dialogue     A dialogue box is on screen and currently has focus
        #   unactive_obstacle   The player is investigating, next state is active_dialogue once they click a sprite
        self.state = "unactive_obstacle"

    def load_stage(self, stage_name):
        print(self.dialogue[stage_name].values())
        for button in self.dialogue[stage_name].values():
            self.world_buttons.append(Button(button["pos"], self, button["dialogue"]))


class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our player (draggable rect).
        """
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()

        self.new_cursor = pg.image.load("./assets/cursor_img.png")
        pg.mouse.set_visible(False)

        self.world = World(self)

    def event_loop(self):
        """
        This is the event loop for the whole program.
        Regardless of the complexity of a program, there should never be a need
        to have more than one event loop.
        """
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.KEYDOWN:
                continue
            if event.type == pg.MOUSEBUTTONDOWN:
                if (self.world.state == "unactive_obstacle"):
                    for o in self.world.world_buttons:
                        o.check_click(event.pos)
                elif (self.world.state == "active_dialogue"):
                    for o in self.world.world_dboxes:
                        o.check_click(event.pos)
            if event.type == pg.QUIT:
                # Change done to True, to exit the main loop
                self.done = True

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(pg.Color("black"))
        for arr in self.world.screen_object_arrays:
            for o in arr:
                o.draw(self.screen)
        
        self.cursor_update(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """
        self.world.load_stage("obstacle_1")
        while not self.done:
            self.event_loop()
            self.render()
            self.clock.tick(self.fps)
    
    def cursor_update(self, screen):
        position = pg.mouse.get_pos()
        screen.blit(self.new_cursor, position)


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()