# grid.py
#
# Python source file containing the code for the logic of the grid, as well as
# drawing the grid.

import random, os, sys, pygame, pdb
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

    def highlight_path(self, path, color=(200,0,0,100)):
        """
        Highlights a list of nodes provided as an argument. Useful for tracing
        the pathfinding of the AI.
        """
        screen = pygame.display.get_surface()
        for node in path:
            # Draw a translucent rectangle over the node. Color depends on the
            # argument provided
            rect = pygame.draw.rect(screen, color,
                    pygame.Rect(self.get_drawing_coordinates(
                    node.get_coordinates()), (SQUARE_SIZE, SQUARE_SIZE)))

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
        except:
            return

        print('New location is ' + str(new_location))
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
                    'object: ' + str(node.contents))
        else:
            # Let's check if we grabbed Monokuma
            if(node.contents is MONOKUMA):
                # Get the previous score of the player
                previous_score = player.score
                # Increment the score of the player
                player.score += 1
                # Set the flag that the player has scored, this will help with
                # the graphics
                player.scored = True
                # Change the music appropriately
                if previous_score < 10 and player.score >= 10:
                    pygame.mixer.music.load(os.path.join("sounds",
                        "medium.ogg"))
                    pygame.mixer.music.play()
                elif previous_score < 20 and player.score >= 20:
                    pygame.mixer.music.load(os.path.join("sounds", "fast.ogg"))
                    pygame.mixer.music.play()
                elif previous_score >= 10 and player.score < 10:
                    pygame.mixer.music.load(os.path.join("sounds", "slow.ogg"))
                    pygame.mixer.music.play()
                # Play a score sound
                score_sound = pygame.mixer.Sound(os.path.join("sounds",
                    "score.ogg"))
                score_sound.play()
            # Now let's check if the player stepped on a trap
            elif(node.contents is TRAP):
                # Get the previous score of the player
                previous_score = player.score
                # Decrement the score of the player by two, but don't let it go
                # to negative
                if(player.score < 2):
                    player.score = 0
                else:
                    player.score -= 2
                # Set the flag that the player has been trapped, this will help
                # with the graphics (and the movement)
                player.trapped = True
                # Change the music appropriately
                if previous_score < 10 and player.score >= 10:
                    pygame.mixer.music.load(os.path.join("sounds",
                        "medium.ogg"))
                    pygame.mixer.music.play()
                elif previous_score < 20 and player.score >= 20:
                    pygame.mixer.music.load(os.path.join("sounds", "fast.ogg"))
                    pygame.mixer.music.play()
                elif previous_score >= 10 and player.score < 10:
                    pygame.mixer.music.load(os.path.join("sounds", "slow.ogg"))
                    pygame.mixer.music.play()
                # Play an explosion sound
                explosion_sound = pygame.mixer.Sound(os.path.join("sounds",
                    "explosion.wav"))
                explosion_sound.play()
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

    def spawn_walls(self, pattern='quad'):
        """
        Draws a predefined pattern of walls, also depending on the argument
        given.
        """
        if pattern is 'quad':
            # Create a quad pattern of walls
            # The top  and bottom horizontal walls
            for i in range(5, 18):
                self.set_node_entity((i, 4), WALL)
                self.set_node_entity((i, 12), WALL)
            # The left and right vertical walls
            for i in range(5, 11):
                self.set_node_entity((3, i), WALL)
                self.set_node_entity((19, i), WALL)
        elif pattern is 'bottleneck':
            # Create a bottle where there is only one path in and out
            # Necks
            for i in range(8, 14):
                self.set_node_entity((10, i), WALL)
                self.set_node_entity((12, i), WALL)
            # Bottle top horizontal
            for i in range(6, 11):
                self.set_node_entity((i, 14), WALL)
            for i in range(12, 17):
                self.set_node_entity((i, 14), WALL)
            # Bottle verticals
            for i in range(15, 18):
                self.set_node_entity((6, i), WALL)
                self.set_node_entity((16, i), WALL)
        elif pattern is 'face':
            for i in range(4, 8):
                self.set_node_entity((5, i), WALL)
            for i in range(4, 8):
                self.set_node_entity((17, i), WALL)
            for i in range(5,18):
                self.set_node_entity((i, 14), WALL)
        elif pattern is 'arrows':
            # Arrows that extend from the corners
            # Topleft arrow
            for i in range(1, 8):
                self.set_node_entity((i,i), WALL)
            for i in range(3, 8):
                self.set_node_entity((i,7), WALL)
                self.set_node_entity((7,i), WALL)
            # Topright arrow
            self.set_node_entity((16,7), WALL)
            self.set_node_entity((17,6), WALL)
            self.set_node_entity((18,5), WALL)
            self.set_node_entity((19,4), WALL)
            self.set_node_entity((20,3), WALL)
            self.set_node_entity((21,2), WALL)
            self.set_node_entity((22,1), WALL)
            for i in range(16, 21):
                self.set_node_entity((i, 7), WALL)
            for i in range(3, 7):
                self.set_node_entity((16, i), WALL)
            # Bottomright arrow
            for i in range(16, 9, -1):
                self.set_node_entity((i + 6,i), WALL)
            for i in range(16, 21):
                self.set_node_entity((i,10), WALL)
            for i in range(10, 15):
                self.set_node_entity((16, i), WALL)
            # Bottomright arrow
            for i in range(1, 8):
                self.set_node_entity((i, 17 - i), WALL)
            for i in range(10, 15):
                self.set_node_entity((7, i), WALL)
            for i in range(3, 8): 
                self.set_node_entity((i, 10), WALL)
            # Middle walls
            for i in range(0, 3):
                self.set_node_entity((11, i), WALL)
                self.set_node_entity((12, i), WALL)
                self.set_node_entity((11, i + 5), WALL)
                self.set_node_entity((12, i + 5), WALL)
                self.set_node_entity((11, i + 10), WALL)
                self.set_node_entity((12, i + 10), WALL)
                self.set_node_entity((11, i + 15), WALL)
                self.set_node_entity((12, i + 15), WALL)

    def draw_player(self, player):
        """
        Draws the triangle sprite of the player, depending on the player
        passed as an argument. The direction the sprite is pointing is also
        dependent on the direction of the player passed.
        """
        screen = pygame.display.get_surface()

        print('Coordinates are ' + str(player.coordinates))
        print('Direction is ' + str(player.direction))

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

    def spawn_traps(self):
        """
        Spawns a random number of traps around the grid, while also removing
        the traps prior to creation.
        """
        # Find the nodes where traps are currently in.
        nodes = self.find_nodes_containing(TRAP)

        # Remove the traps on those nodes.
        for node in nodes:
            node.contents = NONE

        # Generate a random number of traps
        num_traps = random.randint(1,8)

        # Put these traps around the board
        for i in range(0, num_traps):
            # Generate a random location
            random_location = (random.randint(0,23), random.randint(0,17))
            while(self.get_node_in_location(random_location).contents is not
                    NONE):
                # Keep generating while we have conflicts
                random_location = (random.randint(0,23), random.randint(0,17))
            # Put the trap in that location
            self.get_node_in_location(random_location).contents = TRAP

    def get_random_empty_location(self):
        """
        Returns a randomly chosen empty location somewhere in the grid. Perfect
        for initial spawning of the players.
        """
        # Let's get a list of blank nodes.
        nodes = self.find_nodes_containing(NONE)

        # Return a random node's location from that list
        return random.choice(nodes).coordinates

    def spawn_monokuma(self):
        """
        Spawns a random Monokuma somewhere in the grid, while also removing the
        last existing one.
        """
        # First, let's get a list of nodes where Monokuma is in.
        nodes = self.find_nodes_containing(MONOKUMA)

        # Remove Monokuma on those nodes.
        for node in nodes:
            node.contents = NONE

        random_location = (random.randint(0,23), random.randint(0,17))
        # Generate a random location in the board.
        while(self.get_node_in_location(random_location).contents is not NONE):
            random_location = (random.randint(0,23), random.randint(0,17))

        # Now let's put Monokuma on the random location.
        self.get_node_in_location(random_location).contents = MONOKUMA

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

    def draw_explosions(self, location, frame):
        """
        Draws an expanding explosion sprite in the given location on the map.
        The size depends on the current frame of the explosion.
        """
        screen = pygame.display.get_surface()
        # Get the rect pertaining to the location
        drawing_rect = pygame.Rect((self.get_drawing_coordinates(location)),
                (SQUARE_SIZE, SQUARE_SIZE))
        # Load the explosion image
        explosion = pygame.image.load(os.path.join(
            "images", "pow.png"))
        # Scale the image according to the current frame
        # Debug message
        print('Frame multiplier is ' + str(frame / 10.0))
        explosion = pygame.transform.scale(explosion,
                (int(explosion.get_rect().width * (frame / 10.0)),
                int(explosion.get_rect().height * (frame / 10.0))))
        # Set the drawing location to the middle of the rect
        #drawing_rect.topleft = (drawing_rect.centerx, drawing_rect.centery)
        # Blit the explosion
        screen.blit(explosion, drawing_rect)

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
