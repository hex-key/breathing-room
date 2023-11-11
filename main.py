import pygame as pg
import os, sys
import json

from dialog_box import DialogBox as DBox

CAPTION = "game with story 🦣"
SCREEN_SIZE = (1000, 750)

# 
class RoomButton(object):
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

class MenuStartButton(object):
    def __init__(self, w):
        self.image = pg.image.load("./assets/menu/start.png")
        self.rect = self.image.get_rect()
        self.rect.center = (480, 620)

        self.world = w

    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_click(self, p):
        if self.rect.collidepoint(p):
            self.world.load_intro()

class MenuSkipButton(object):
    def __init__(self, w):
        self.image = pg.image.load("./assets/menu/skip_button.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (900, 650)

        self.world = w

    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_click(self, p):
        if self.rect.collidepoint(p):
            print('help')
            self.world.load_main_room()

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
        #   menu                Starting menu, prompt to launch intro_sequence
        #   intro_sequence      The intro sequence is playing
        #   active_dialogue     A dialogue box is on screen and currently has focus
        #   idle_main_room      The player is investigating, next state is active_dialogue once they click a sprite
        self.state = "menu"

        self.current_checkpoint = 1

    def load_menu(self):
        self.app.bg_image = pg.image.load("./assets/menu/menu_bg.png")
        self.world_buttons.append(MenuStartButton(self))
        self.world_buttons.append(MenuSkipButton(self))

    def load_intro(self):
        self.clear_screen()
        self.app.bg_image = pg.image.load("./assets/intro/intro_bg.png")
        
    def load_main_room(self):
        self.clear_screen()
        self.app.bg_image = pg.image.load("./assets/main_room/bg.png")
        for button in self.dialogue["main_room"].values():
            self.world_buttons.append(RoomButton(button["pos"], self, button["dialogue"]))

    def clear_screen(self):
        for arr in self.screen_object_arrays:
            arr.clear()


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
        self.bg_image = None

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
                if (self.world.state == "menu"):
                    for o in self.world.world_buttons:
                        o.check_click(event.pos)
                elif (self.world.state == "intro_sequence"):
                    for o in self.world.world_dboxes:
                        o.check_click(event.pos)
                elif (self.world.state == "idle_main_room"):
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
        self.screen.blit(self.bg_image, (0, 0))
        
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
        self.world.load_menu()
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