import pygame as pg

from dialog_box import DialogBox as DBox

class button:
    text = ""

def main():
    # initialize the pg module
    pg.init()
    # load and set the logo
    # logo = pg.image.load("logo32x32.png")
    # pg.display.set_icon(logo)
    pg.display.set_caption("game with story 🦣")
     
    # create a surface on screen
    screen = pg.display.set_mode((1000, 750))
     
    # define a variable to control the main loop
    running = True

    on_screen_objects = []

     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.KEYDOWN:
                print(chr(event.key))
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False

if __name__ == "__main__":
    main()

# testing comment