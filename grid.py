# grid.py
#
# Python source file containing the code for the logic of the grid, as well as
# drawing the grid.

import random, os, sys, pygame
from pygame.locals import *

# Import node class
from node import Node

# CONSTANTS
GRID_COLOR = pygame.Color(0, 0, 0, 0)
ARRAY_SIZE_X = 24
ARRAY_SIZE_Y = 18

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

    def __init__(self):
        """
        Initialization function for the grid.

        Initializes the important variables that it has as an object such as
        the array of nodes.
        """
        # Initialize the "array" we will use for the grid
        # Note that it's just a y list of x lists
        self.node_array = []

        # Debug variable for tracking nodes
        num = 1
        for i in range(0, ARRAY_SIZE_Y):
            row = []
            for j in range(0, ARRAY_SIZE_X):
                # Create the node with its respective coordinates
                node = Node(j, i)
                # Add the node to the row
                row.append(node)
                # DEBUG message
                print('Created node ' + str(num) + ' at coordinates: ' + 
                        str(node.coordinates))
                num += 1
            # Add the row to the array
            self.node_array.append(row)

        # Debug message
        print('Node array initialized!')
