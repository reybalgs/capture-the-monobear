#!/usr/bin/python

# capture-the-monobear/main.py
#
# Main python file. Run this to run the game.

# Important imports
import random, os, sys, pygame
from pygame.locals import *

from grid import *
from player_ui import *

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

    # Fill the color of the background
    screen.fill(WHITE)

    # Unnecessary game loop variable
    loop = True

    # Tracks total frames rendered
    frames = 0

    while loop:
        # Limit the frame rate of the game to 30FPS
        clock.tick(30)

        # Display frames rendered
        #frames += 1
        #print(str(frames) + ' were rendered!')

        ####################################################################
        # Game logic
        ####################################################################

        grid = Grid()
        grid.draw_grid()

        ####################################################################
        # Event Handling
        ####################################################################
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False

        ####################################################################
        # Display updating
        ####################################################################

        # Display player ui
        players_ui = UI_Players()
        players_ui.draw_image()

        # Update everything
        pygame.display.flip()

if __name__ == '__main__':
    main()
