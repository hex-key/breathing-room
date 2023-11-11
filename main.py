import pygame as pg

def main():
    # initialize the pg module
    pg.init()
    # load and set the logo
    # logo = pg.image.load("logo32x32.png")
    # pg.display.set_icon(logo)
    pg.display.set_caption("game with story 🦣")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode((1000, 750))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.KEYDOWN:
                continue
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False

if __name__ == "__main__":
    main()

# testing comment