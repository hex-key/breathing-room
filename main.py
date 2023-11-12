import pygame as pg
import os, sys, json

from typing import Callable

from dialog_box import DialogBox as DBox

CAPTION = "game with story 🦣"
SCREEN_SIZE = (1000, 750)

class App():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.bg_image = None

        self.new_cursor = pg.image.load("./assets/cursor_img.png")
        pg.mouse.set_visible(False)

        self.world = World(self)

    def event_loop(self):
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                for s in self.world.sprites:
                    s.check_click(event.pos)

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.world.sprites.draw(self.screen)
        self.cursor_update(self.screen)
        pg.display.update()

    def main_loop(self):
        self.world.load_menu()
        while not self.done:
            self.event_loop()
            self.world.sprites.update()
            self.render()
            self.clock.tick(self.fps)
    
    def cursor_update(self, screen: pg.surface.Surface):
        position = pg.mouse.get_pos()
        screen.blit(self.new_cursor, position)

class World():
    def __init__(self, app: App):
        with open("./dialogue.json", "r") as f:
            self.dialogue = json.load(f)
        self.intro_dialogue = self.dialogue["intro"]
        self.room_dialogue = self.dialogue["main_room"]
        self.app = app

        self.sprites = pg.sprite.Group()

        # World state options
        #   menu                    Starting menu, prompt to launch intro_sequence
        #   intro_sequence          The intro sequence is playing
        #   idle_main_room          The player is investigating, next state is active_dialogue once they click a sprite
        #   dialogue_main_room      A main roomdialogue box is on screen and currently has focus
        self.state = "menu"

        self.current_checkpoint = 0

    def load_menu(self):
        self.state = "menu"
        self.app.bg_image = pg.image.load("./assets/menu/bg.png")
        self.sprites.add(
            Button(self, "./assets/menu/start.png", (480, 620), lambda: self.load_intro()),
            Button(self, "./assets/menu/skip.png", (900, 650), lambda: self.load_main_room())
                    )

    def load_intro(self):
        self.state = "intro_sequence"
        self.sprites.empty()
        self.app.bg_image = pg.image.load("./assets/intro/bg.png")
        
    def load_main_room(self):
        self.state = "idle_main_room"
        self.sprites.empty()
        self.app.bg_image = pg.image.load("./assets/main_room/bg.png")
        for key, s in self.room_dialogue.items():
            self.sprites.add(Button(self, s["img_path"], s["pos"], None, s["dialogue"], key))
    
    def set_world_state(self, state: str):
        self.state = state
        if state == "idle_main_room":
            for s in self.sprites:
                if isinstance(s, Button):
                    if s.state == "clicked":
                        s.set_state("fading")


class Button(pg.sprite.Sprite):
    def __init__(self, world: World, img_path: str, center: tuple, action: Callable, lines: list[str]=None, label: str=None):    
        pg.sprite.Sprite.__init__(self)
        self.world = world

        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.action = action
        self.lines = lines

        self.label = label
        # Possible button states
        #   visible     Button is regularly displayed
        #   clicked     Button has been clicked, respective dialogue is running
        #   fading      Button is being faded to clear
        self.state = "visible"
        self.alpha = 255
    
    def update(self):
        if self.state == "fading":
            self.alpha -= 0.5
            self.image.fill((255, 255, 255, self.alpha), None, pg.BLEND_RGBA_MULT)
            if self.alpha == 0:
                self.world.sprites.remove(self)

    def check_click(self, p: tuple[int, int]):
        if self.rect.collidepoint(p):
            if self.action is not None:
                self.action()
            else:
                self.state = "clicked"
                self.world.set_world_state("main_room_dialogue")
                self.world.sprites.add(DBox(100, 500, 500, 200, self.lines, self.world))
    
    def set_state(self, state):
        self.state = state


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()