#!/usr/bin/python

# capture-the-monobear/main.py
#
# Main python file. Run this to run the game.

# Important imports
import random, os, sys, pygame
from pygame.locals import *

from grid import *
from player_ui import *
from player import *

#############################################################################
# CONSTANTS AND CRAP
#############################################################################

# Screen resolution
SCREEN_X = 1024
SCREEN_Y = 600

# Game frame rate
FPS = 2

# Node size
NODE_SIZE = 24

# Entities
NONE = 0
NAEGI = 1
KIRIGIRI = 2
WALL = 3
TRAP = 4
MONOKUMA = 5

# Coordinates
X = 0
Y = 1

# Colors
WHITE = (255,255,255)

# Movement cost
MOVE_COST = 10

# Global variables for movement
dpad_up_pressed = False
dpad_down_pressed = False
dpad_right_pressed = False
dpad_left_pressed = False

def main():
    # Main function
    clock = pygame.time.Clock()

    # Get the screen of the game
    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Capture the Monobear!')
    screen = pygame.display.get_surface()

    # Initialize the background of the game
    background = pygame.Surface(screen.get_size())

    # Unnecessary game loop variable
    loop = True

    # Tracks total frames rendered
    frames = 0

    # Initialzie the two players
    naegi = Player('Naegi')
    kirigiri = Player('Kirigiri')

    # Initialize the game grid
    grid = Grid()

    # DEBUG: Test entity drawing
    #grid.node_array[8][4].contents = MONOKUMA
    grid.set_node_entity((4,8), MONOKUMA)
    #grid.set_node_entity((2,2), MONOKUMA)
    # Testing Naegi's location
    naegi.coordinates = (5,3)
    naegi.direction = 'down'
    grid.set_node_entity(naegi.coordinates, NAEGI)
    # Testing Kirigiri's location
    kirigiri.coordinates = (9,15)
    kirigiri.direction = 'up'
    grid.set_node_entity(kirigiri.coordinates, KIRIGIRI)
    # Testing traps
    grid.set_node_entity((10,3), TRAP)
    grid.set_node_entity((8,7), TRAP)
    # Testing walls
    for i in range(3, 15):
        grid.set_node_entity((6, i), WALL)
    for i in range(2, 20):
        grid.set_node_entity((i, 1), WALL)

    # Initialize the handler of player UI elements
    players_ui = UI_Players()

    while loop:
        # Limit the frame rate of the game to 30FPS
        clock.tick(FPS)

        # Display frames rendered
        #frames += 1
        #print(str(frames) + ' were rendered!')

        ####################################################################
        # Game logic
        ####################################################################

        # Testing: Move Kirigiri upwards until she hits something
        if(kirigiri.coordinates[Y] > 0):
            grid.move_player(kirigiri, (kirigiri.coordinates[X],
                kirigiri.coordinates[Y] - 1))

        ####################################################################
        # Event Handling
        ####################################################################
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False

        ####################################################################
        # Display updating
        ####################################################################

        # Clear the screen for new blits
        screen.fill(WHITE)

        # Draw the grid
        grid.draw_grid()
        grid.draw_monokuma()
        grid.draw_walls()
        grid.draw_traps()
        grid.draw_player(naegi)
        grid.draw_player(kirigiri)

        # Display player ui
        players_ui.draw_image()
        players_ui.draw_text()
        players_ui.draw_score(naegi.score, kirigiri.score)

        # Update everything
        pygame.display.flip()

if __name__ == '__main__':
    main()
