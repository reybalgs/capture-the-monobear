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
WALL_COLOR = pygame.Color(0, 0, 120, 0)
ARRAY_SIZE_X = 24
ARRAY_SIZE_Y = 18
SQUARE_SIZE = 32
INITIAL_POS_X = 16
INITIAL_POS_Y = 12
X = 0
Y = 1
# Color for Naegi's text and icon
NAEGI_COLOR = (120,150,90)
# Color for Kirigiri's text and icon
KIRIGIRI_COLOR = (200,160,200)

# Entities
NONE = 0
NAEGI = 1
KIRIGIRI = 2
WALL = 3
TRAP = 4
MONOKUMA = 5

class OutOfGridRangeException(Exception):
    """
    Exception that is called whenever the provided location is out of the 24x18
    grid range.
    """
    def __init__(self, location):
        self.location = location
    def __str__(self):
        return repr(self.location)

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
                    #print('Entity ' + str(entity) + ' found at ' +
                    #        str(node.coordinates))
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

    def draw_walls(self):
        """
        Draws the wall objects of the board.
        """
        screen = pygame.display.get_surface()

        # Find all the nodes containing walls in the game, then put them in a
        # list.
        nodes = self.find_nodes_containing(WALL)

        # Now let's draw the rects into the game surface.
        for node in nodes:
            # We need to get the X and Y top corner coordinates to draw the
            # rect into, and those locations will depend on the location of the
            # nodes in the array.
            drawing_loc = self.get_drawing_coordinates(node.coordinates)
            wall = pygame.draw.rect(screen, WALL_COLOR,
                    pygame.Rect(drawing_loc, (SQUARE_SIZE, SQUARE_SIZE)))

    def move_player_forward(self, player):
        """
        Moves the location of the given player on the map forward, depending on
        the current direction the player is facing.

        This operates in similar principes as the move_player function.
        """
        # Let's check who the player we got is
        if(player.name.lower() is 'naegi'):
            player_type = NAEGI
            print('Received NAEGI in move_player_forward')
        else:
            player_type = KIRIGIRI
            print('Received KIRIGIRI in move_player_forward')

        # Let's get the proposed new location of the player depending on the
        # direction they are currently facing.
        if(player.direction is 'up'):
            new_location = (player.coordinates[X], player.coordinates[Y] - 1)
        elif(player.direction is 'down'):
            new_location = (player.coordinates[X], player.coordinates[Y] + 1)
        elif(player.direction is 'left'):
            new_location = (player.coordinates[X] - 1, player.coordinates[Y])
        elif(player.direction is 'right'):
            new_location = (player.coordinates[X] + 1, player.coordinates[Y])

        # Check if the location is valid or not
        try:
            if(new_location[X] < 0 or new_location[Y] < 0 or new_location[X] >
                    23 or new_location[Y] > 17):
                raise OutOfGridRangeException(new_location)
        except OutOfGridRangeException:
            print('Exception: Given location ' + str(new_location) + ' is'
                    ' invalid! Exiting')

        # Get the node that we are going to move to
        node = self.get_node_in_location(new_location)
        # Get the old node of the player
        old_node = self.get_node_in_location(player.coordinates)

        # Now that that is out of the way, let's check if the new location is
        # passable for the user.
        if(node.contents is WALL or node.contents is KIRIGIRI or node.contents
                is NAEGI):
            # Impassable node up ahead!
            print('Location ' + str(new_location) + ' contains impassable ' +
                    'object.')
        else:
            # We can move through
            # Set the coordinates of the player to the new location
            player.coordinates = new_location
            # Set the entity of the new location as the player
            self.set_node_entity(new_location, player_type)
            # Set the entity of the old location as empty
            self.set_node_entity(old_node.coordinates, NONE)
        

    def move_player(self, player, new_location):
        """
        Moves the location of the given player on the map.

        It does this by first setting the coordinates carried by the player to
        the provided new_location, then updating the board by setting its
        former location to NONE and setting the new_location to the specified
        player.

        It also checks if the player is allowed to move in the direction
        specified. It will not allow the player to pass if there is a wall or
        another player in the way.
        """
        # Let's check who we got as the parameter, and set a variable
        # reflecting the player's identity
        if(player.name.lower() is 'naegi'):
            player_type = NAEGI
            # Debug message
            print('Received NAEGI in move_player')
        else:
            player_type = KIRIGIRI
            print('Received KIRIGIRI in move_player')
        # First we need to check if the given location is real or not.
        try:
            if(new_location[X] < 0 or new_location[Y] < 0 or new_location[X] >
                    23 or new_location[Y] > 17):
                raise OutOfGridRangeException(new_location)
        except OutOfGridRangeException:
            print('Exception: Given location ' + str(new_location) + ' is'
                    ' invalid! Exiting')

        # Get the node that we are going to move to
        node = self.get_node_in_location(new_location)
        # Get the old node of the player
        old_node = self.get_node_in_location(player.coordinates)

        # Now that that is out of the way, let's check if the new location is
        # passable for the user.
        if(node.contents is WALL or node.contents is KIRIGIRI or node.contents
                is NAEGI):
            # Impassable node up ahead!
            print('Location ' + str(new_location) + ' contains impassable ' +
                    'object.')
        else:
            # We can move through
            # Set the coordinates of the player to the new location
            player.coordinates = new_location
            # Set the entity of the new location as the player
            self.set_node_entity(new_location, player_type)
            # Set the entity of the old location as empty
            self.set_node_entity(old_node.coordinates, NONE)

    def draw_player(self, player):
        """
        Draws the triangle sprite of the player, depending on the player
        passed as an argument. The direction the sprite is pointing is also
        dependent on the direction of the player passed.
        """
        screen = pygame.display.get_surface()

        # Get the rect where the triangle is going to be drawn.
        square_rect = pygame.Rect(self.get_drawing_coordinates(
                    player.coordinates), (SQUARE_SIZE, SQUARE_SIZE))
        # Make the rect a little smaller
        square_rect.x += 4
        square_rect.y += 4
        square_rect.w -= 8
        square_rect.h -= 8
        # DEBUG message: Print rect
        #print square_rect
        # Initialize the list of points for the triangle. The shape will
        # greatly depend on the location the player is going.
        # point1 - first non-center point
        # point2 - second non-center point
        # point3 - center point
        if(player.direction is 'right'):
            # Top left of the rect
            point1 = square_rect.topleft
            # Bottom left of the rect
            point2 = square_rect.bottomleft
            # Center right of the rect
            point3 = (square_rect.right, square_rect.bottom -
                    ((square_rect.bottom - square_rect.top) / 2))
        elif(player.direction is 'down'):
            # Top left of the rect
            point1 = square_rect.topleft
            # Top right of the rect
            point2 = square_rect.topright
            # Bottomcenter of the rect
            point3 = (square_rect.right - ((square_rect.right -
                square_rect.left) / 2), square_rect.bottom)
        elif(player.direction is 'left'):
            # Top right of the rect
            point1 = square_rect.topright
            # Bottom right of the rect
            point2 = square_rect.bottomright
            # Center left of the rect
            point3 = (square_rect.left, square_rect.bottom -
                    ((square_rect.bottom - square_rect.top) / 2))
        elif(player.direction is 'up'):
            # Bottom right of the rect
            point1 = square_rect.bottomright
            # Bottom left of the rect
            point2 = square_rect.bottomleft
            # Center top of the rect
            point3 = (square_rect.right - ((square_rect.right -
                square_rect.left) / 2), square_rect.top)
        # Add the points into the list.
        points = [point1, point2, point3]
        # DEBUG message, print points
        #print points

        # DEBUG print player name
        #print player.name.lower()

        # Draw the triangle of the player.
        if(player.name.lower() == 'naegi'):
            triangle = pygame.draw.polygon(screen, NAEGI_COLOR, points)
        else:
            triangle = pygame.draw.polygon(screen, KIRIGIRI_COLOR, points)

    def draw_traps(self):
        """
        Draws the traps around the board.
        """
        screen = pygame.display.get_surface()
        # Find the nodes containing the bombs
        nodes = self.find_nodes_containing(TRAP)

        # Initialize the image for the traps
        trap = pygame.transform.scale(pygame.image.load(os.path.join("images",
            "bomb.png")), (SQUARE_SIZE, SQUARE_SIZE))
        trap.convert_alpha()

        # Now let's draw the traps in those nodes
        for node in nodes:
            # Get the x and y coordinates to draw the traps in
            drawing_loc = self.get_drawing_coordinates(node.coordinates)
            # Blit the trap in that location
            screen.blit(trap, drawing_loc)

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
        monokuma.convert_alpha()
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
