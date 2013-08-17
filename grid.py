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
SQUARE_SIZE = 32
INITIAL_POS_X = 16
INITIAL_POS_Y = 12
X = 0
Y = 1

# Entities
NONE = 0
NAEGI = 1
KIRIGIRI = 2
WALL = 3
TRAP = 4
MONOKUMA = 5

class Grid():
    def find_nodes_containing(self, entity):
        """
        Returns a list of Nodes containing the entity provided.
        """
        nodes = []
        for row in self.node_array:
            for node in row:
                if node.contents is entity:
                    # Debug message
                    print('Entity ' + str(entity) + ' found at ' +
                            str(node.coordinates))
                    nodes.append(node)

        return nodes

    def set_node_entity(self, location, entity):
        """
        Sets the entity of the node in the location passed as an argument to
        the entity passed as an argument.

        This convenience function is created because simply doing
        node_array[x][y] will yield wrong results, because the actual array is
        represented as node_array[y][x].
        """
        node = self.get_node_in_location(location)
        node.contents = entity

    def get_node_in_location(self, location):
        """
        Returns a Node object in the specified (x,y) location tuple.
        """
        node = self.node_array[location[Y]][location[X]]
        # Debug message
        print('Returning node in ' + str(node.coordinates) + ' with contents ' +
                str(node.contents))
        return node

    def get_drawing_coordinates(self, location):
        """
        Returns an (x, y) location tuple for PyGame to blit images into,
        depending on the (x, y) location on the array provided as an argument.
        """
        x = INITIAL_POS_X + (32 * location[X])
        y = INITIAL_POS_Y + (32 * location[Y])
        return (x, y)

    def draw_monokuma(self):
        """
        Draws monokuma's sprite depending on his location in the board.
        """
        screen = pygame.display.get_surface()
        # First, we need to find Monokuma's location in the board.
        # I know it's not supposed to happen, but sometimes there can be the
        # case of multiple Monokumas on the board, so we have to use a list of
        # these locations.
        nodes = self.find_nodes_containing(MONOKUMA)
        
        # Then, let's initialize the image for Monokuma.
        monokuma = pygame.transform.scale(pygame.image.load(os.path.join(
            "images", "monokuma_head.png")), (SQUARE_SIZE, SQUARE_SIZE))
        # Now let's draw Monokuma in these nodes
        for node in nodes:
            # We need to get the x and y coordinates (in Surface) to draw
            # Monokuma in, depending on the location in the array
            drawing_loc = self.get_drawing_coordinates(node.coordinates)
            # Blit Monokuma in that location
            screen.blit(monokuma, drawing_loc)

    def draw_grid(self):
        """
        Draw the horizontal and vertical lines which comprises the grid.
        """
        screen = pygame.display.get_surface()

        # Horizontal line drawing
        hor_lines = 19

        # Initial x pos of the vertical lines
        x_pos = INITIAL_POS_X
        # Initial y pos of the horizontal lines
        y_pos = INITIAL_POS_Y
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
        y_pos = INITIAL_POS_Y
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
                        str(node.coordinates) + ' or (' + str(node.getX() + 1)
                        + ', ' + str(node.getY() + 1) + ')')
                num += 1
            # Add the row to the array
            self.node_array.append(row)

        # Debug message
        print('Node array initialized!')
