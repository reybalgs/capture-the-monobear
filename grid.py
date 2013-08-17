# grid.py
#
# Python source file containing the code for the logic of the grid, as well as
# drawing the grid.

import random, os, sys, pygame
from pygame.locals import *

# CONSTANTS
GRID_COLOR = pygame.Color(0, 0, 0, 0)

class Grid():
    def draw_grid(self):
        """
        Draw the horizontal and vertical lines which comprises the grid.
        """
        screen = pygame.display.get_surface()

        # Horizontal line drawing
        hor_lines = 19

        # Initial x pos of the vertical lines
        x_pos = 16
        # Initial y pos of the horizontal lines
        y_pos = 12
        while hor_lines > 0:
            # Draw the line
            if hor_lines == 19:
                # Top line, move line all the way to the end
                line = pygame.draw.aaline(screen, GRID_COLOR, (x_pos,
                    y_pos), (1016, y_pos))
            elif hor_lines == 10:
                # Middle line, move line all the way to the end
                line = pygame.draw.aaline(screen, GRID_COLOR, (x_pos,
                    y_pos), (1016, y_pos))
            elif hor_lines == 1:
                # Last line, move line all the way to the end
                line = pygame.draw.aaline(screen, GRID_COLOR, (x_pos,
                    y_pos), (1016, y_pos))
            else:
                line = pygame.draw.aaline(screen, GRID_COLOR, (x_pos,
                    y_pos), (784, y_pos))
            # Increment the vertical position
            y_pos += 32
            # Decrement the number of horizontal lines
            hor_lines -= 1

        # Reset the y position
        y_pos = 12
        # Vertical line drawing
        ver_lines = 26
        while ver_lines > 0:
            # Draw the line
            if ver_lines == 1:
                # Last line, draw to the end
                line = pygame.draw.aaline(screen, GRID_COLOR, (1016, y_pos),
                        (1016, y_pos + 576))
            else:
                line = pygame.draw.aaline(screen, GRID_COLOR, (x_pos, y_pos),
                        (x_pos, y_pos + 576))
            # Increment the horizontal position
            x_pos += 32
            # Decrement the number of vertical lines
            ver_lines -= 1

        # DEBUG MESSAGE
        #print('Grid drawn!')
