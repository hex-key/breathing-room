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
        self.room_objects_dialogue = self.dialogue["main_room"]["objects"]
        self.room_checkpoints_dialogue = self.dialogue["main_room"]["checkpoints"]
        self.app = app

        self.sprites = pg.sprite.Group()

        # World state options enumerated later
        self.state = "menu"

        self.current_checkpoint = 0

    def load_menu(self):
        self.set_world_state("menu")
        self.app.bg_image = pg.image.load("./assets/menu/bg.png")
        self.sprites.add(
            MenuButton(self, "./assets/menu/start.png", (480, 620), lambda: self.load_intro()),
            MenuButton(self, "./assets/menu/skip.png", (900, 650), lambda: self.load_main_room())
                    )

    def load_intro(self):
        self.set_world_state("fade")
        def f():
            self.set_world_state("intro_sequence")
            self.sprites.empty()
            self.app.bg_image = pg.image.load("./assets/intro/bg.png")
            #self.sprites.add(DBox(100, 600, 800, 150, self.intro_dialogue, self))
        self.sprites.add(Fade(self, f))
        
        
    def load_main_room(self):
        self.set_world_state("fade")
        def f():
            self.set_world_state("idle_main_room")
            self.sprites.empty()
            self.app.bg_image = pg.image.load("./assets/main_room/bg.png")
            for key, s in self.room_objects_dialogue.items():
                self.sprites.add(RoomObject(self, s["img_path"], s["pos"], s["dialogue"]))
        self.sprites.add(Fade(self, f))
    
    # World state options
    #   menu                    Starting menu, prompt to launch intro_sequence
    #   fade                    World is actively fading, halt all input handling
    #   intro_sequence          The intro sequence is playing
    #   idle_main_room          The player is investigating, next state is active_dialogue once they click a sprite
    #   dialogue_main_room      A main room dialogue box is on screen and currently has focus
    #   checkpoint_main_room    Main room checkpoint dialogue is on screen
    def set_world_state(self, state: str):
        match state:
            case "menu" | "fade" | "intro_sequence" | "dialogue_main_room" | "checkpoint_main_room":
                self.state = state
            case "idle_main_room":
                self.state = state
                for s in self.sprites:
                    if isinstance(s, RoomObject):
                        if s.state == "clicked":
                            s.set_state("fading")
            case _:
                raise Exception("Improper world state passed to set_world_state()")
        
class MenuButton(pg.sprite.Sprite):
    def __init__(self, world: World, img_path: str, center: tuple, action: Callable):    
        pg.sprite.Sprite.__init__(self)
        self.world = world
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.action = action

    def update(self):
        pass

    def check_click(self, p: tuple[int, int]):
        if self.rect.collidepoint(p):
            self.action()


class RoomObject(pg.sprite.Sprite):
    def __init__(self, world: World, img_path: str, center: tuple, lines: list[str]):    
        pg.sprite.Sprite.__init__(self)
        self.world = world

        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.lines = lines
        self.state = "visible"
        self.alpha = 255
    
    def update(self):
        if self.state == "fading":
            self.alpha -= 5
            self.image.set_alpha(self.alpha)
            if self.alpha <= 10:
                self.kill()

    def check_click(self, p: tuple[int, int]):
        if self.rect.collidepoint(p) and self.state == "visible" and self.world.state != "dialogue_main_room":
            self.set_state("clicked")
            self.world.set_world_state("dialogue_main_room")
            self.world.sprites.add(DBox(70, 70, 500, 200, self.lines, self.world))
    
    # Possible button states
    #   visible     Button is regularly displayed
    #   clicked     Button has been clicked, respective dialogue is running
    #   fading      Button is being faded to clear
    def set_state(self, state):
        match state:
            case "visible" | "clicked" | "fading":
                self.state = state
            case _:
                raise Exception("Improper state passed (button)")

class Fade(pg.sprite.Sprite):
    def __init__(self, world: World, action: Callable):
        super().__init__()
        self.rect = pg.display.get_surface().get_rect()
        self.image = pg.Surface(self.rect.size, flags=pg.SRCALPHA)
        self.alpha = 0

        self.world = world
        self.action = action

        self.rebound = False

    def update(self):
        self.image.fill((0, 0, 0, self.alpha))
        if not self.rebound:
            self.alpha += 3
            if self.alpha > 245:
                self.action()
                self.world.sprites.add(self)
                self.rebound = True
        else:
            self.alpha -= 3
            if self.alpha < 10:
                self.world.sprites.remove(self)
    
    def check_click(self, p: tuple[int, int]):
        return



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