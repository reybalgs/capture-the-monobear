#!/usr/bin/python

# capture-the-monobear/main.py
#
# Main python file. Run this to run the game.

# Important imports
import random, os, sys, pygame
from pygame.locals import *

from grid import *
from player_ui import *


#############################################################################
# CONSTANTS AND CRAP
#############################################################################

# Screen resolution
SCREEN_X = 1024
SCREEN_Y = 600

# Game frame rate
FPS = 30

# Node size
NODE_SIZE = 24

# Entities
NONE = 0
NAEGI = 1
KIRIGIRI = 2
WALL = 3
TRAP = 4
MONOKUMA = 5

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

    # The scores of the players
    naegi_score = 0
    kirigiri_score = 0

    # Initialize the game grid
    grid = Grid()

    # DEBUG: Test entity drawing
    #grid.node_array[8][4].contents = MONOKUMA
    grid.set_node_entity((4,8), MONOKUMA)
    #grid.set_node_entity((2,2), MONOKUMA)

    for i in range(3, 15):
        grid.set_node_entity((6, i), WALL)
    for i in range(2, 20):
        grid.set_node_entity((i, 1), WALL)

    # Initialize the handler of player UI elements
    players_ui = UI_Players()

    while loop:
        # Limit the frame rate of the game to 30FPS
        clock.tick(30)

        # Display frames rendered
        #frames += 1
        #print(str(frames) + ' were rendered!')

        ####################################################################
        # Game logic
        ####################################################################


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

        # Display player ui
        players_ui.draw_image()
        players_ui.draw_text()
        players_ui.draw_score(naegi_score, kirigiri_score)

        # Update everything
        pygame.display.flip()

if __name__ == '__main__':
    main()
