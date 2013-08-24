#!/usr/bin/python

# capture-the-monobear/main.py
#
# Main python file. Run this to run the game.

# Important imports
import random, os, sys, pygame, pdb
from pygame.locals import *

from grid import *
from player_ui import *
from player import *
from pathfinder import *

#############################################################################
# CONSTANTS AND CRAP
#############################################################################

# Screen resolution
SCREEN_X = 1024
SCREEN_Y = 600

# Game frame rate
FPS = 2

# Node size
NODE_SIZE = 32

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
OPEN_LIST_COLOR = pygame.Color(0,200,0,150)
CLOSED_LIST_COLOR = pygame.Color(200,0,0,150)
PATH_LIST_COLOR = pygame.Color(200,200,0,150)

# Movement cost
MOVE_COST = 10

# How long (frames) the players smile when scoring
PLAYER_SMILE_FRAMES = 6
# How long (frames) the players react on traps
PLAYER_TRAP_FRAMES = 10
# How long (frames) explosions occur
EXPLOSION_FRAMES = 4

# The score required to win
WINNING_SCORE = 30

# Global variables for movement
dpad_up_pressed = False
dpad_down_pressed = False
dpad_right_pressed = False
dpad_left_pressed = False

# Global images used
# The tiling background image we will use for the game
tile_img = pygame.image.load(os.path.join(".", "images", "bg.png"))

def main():
    # Main function
    clock = pygame.time.Clock()

    # Initialize the mixer
    pygame.mixer.init()

    # Get the screen of the game
    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Capture the Monobear!')
    screen = pygame.display.get_surface()

    # Initialize the background of the game
    background = pygame.Surface(screen.get_size())

    # Loop the game as long as nobody has won
    naegi_won = 0
    kirigiri_won = 0

    # Tracks total frames rendered
    frames = 0

    # Tracks the number of frames Monokuma has stayed untouched
    monokuma_frames = 0

    # Tracks the number of frames for a batch of traps to stay
    trap_frames = 0

    # Tracks the number of frames for Naegi to smile
    naegi_score_frames = 0
    # Tracks the number of frames for Kirigiri to smile
    kirigiri_score_frames = 0
    # Tracks the number of frames for Naegi to react to traps
    naegi_trap_frames = 0
    # Tracks the nubmer of frames for Kirigiri to react to traps
    kirigiri_trap_frames = 0
    # Tracks the number of frames for explosions to occur (also used for their
    # resizing)
    explosion_size_frames = 0

    # Initialzie the two players
    naegi = Player('Naegi')
    kirigiri = Player('Kirigiri')

    # Initialize the game grid
    grid = Grid()

    # DEBUG: Test entity drawing
    #grid.node_array[8][4].contents = MONOKUMA
    #grid.set_node_entity((4,8), MONOKUMA)
    #grid.set_node_entity((9,10), MONOKUMA)
    #grid.set_node_entity((15,4), MONOKUMA)
    #grid.set_node_entity((18,0), MONOKUMA)
    #grid.set_node_entity((3,11), MONOKUMA)
    #grid.set_node_entity((2,2), MONOKUMA)
    # Testing Naegi's location
    #naegi.coordinates = (5,3)
    #naegi.direction = 'down'
    # Testing Kirigiri's location
    #kirigiri.coordinates = (7,5)
    #kirigiri.direction = 'up'
    # Testing traps
    #grid.set_node_entity((12,5), TRAP)
    #grid.set_node_entity((8,7), TRAP)
    #grid.set_node_entity((9,4), TRAP)

    # Initialize the walls
    grid.spawn_walls('arrows')

    # Initialize the handler of player UI elements
    players_ui = UI_Players()

    # Initialize monokuma on the grid
    grid.spawn_monokuma()
    #grid.set_node_entity((10,5), MONOKUMA)

    # Initialize traps on the grid
    grid.spawn_traps()

    # Randomize Naegi's location
    naegi.coordinates = grid.get_random_empty_location()
    grid.set_node_entity(naegi.coordinates, NAEGI)
    # Randomize Kirigiri's location
    kirigiri.coordinates = grid.get_random_empty_location()
    #kirigiri.coordinates = (6,6)
    grid.set_node_entity(kirigiri.coordinates, KIRIGIRI)

    # Initialize the pathfinder for the AI
    pathfinder = Pathfinder(grid,
            grid.get_node_in_location(kirigiri.coordinates))
    # Initialize the first path of the pathfinder
    pathfinder.find_path_to_monokuma_v2()
    # Turn the AI in the direction it's supposed to turn to
    kirigiri.direction = pathfinder.get_direction_to_next_node_v2(
            grid.get_node_in_location(kirigiri.coordinates))

    while not (kirigiri_won or naegi_won):
        # Limit the frame rate of the game
        if((FPS + naegi.score) > 15):
            clock.tick(15)
        else:
            clock.tick(FPS + naegi.score)

        # Display frames rendered
        #frames += 1
        #print(str(frames) + ' were rendered!')

        ####################################################################
        # Game logic
        ####################################################################

        # Update the start node of the pathfinder
        pathfinder.start_node = grid.get_node_in_location(
                kirigiri.coordinates)

        # Randomize monokuma
        monokuma_frames += 1
        if(monokuma_frames > (20 * FPS) or len(grid.find_nodes_containing(MONOKUMA)) is
                0):
            # Spawn monokuma when x frames have passed or there are no
            # monokumas on the map
            grid.spawn_monokuma()
            monokuma_frames = 0
            print('New monokuma spawned at ' +
                    str(grid.find_nodes_containing(MONOKUMA)[0].coordinates))
            #pdb.set_trace()
            # Make the pathfinder find a new path
            pathfinder.find_path_to_monokuma_v2()

        # Randomize traps
        trap_frames += 1
        if(trap_frames > (15 * FPS) or len(grid.find_nodes_containing(TRAP)) is
                0):
            # Spawn traps when x frames have passed or there are no traps on
            # the map
            grid.spawn_traps()
            trap_frames = 0
            # Update the start node of the pathfinder
            if(len(grid.find_nodes_containing(MONOKUMA))):
                pathfinder.start_node = grid.get_node_in_location(
                        kirigiri.coordinates)
                # Make the pathfinder find a new path
                pathfinder.find_path_to_monokuma_v2()
        # Turn the AI in the direction it's supposed to turn to
        if(len(pathfinder.path)):
            kirigiri.direction = pathfinder.get_direction_to_next_node_v2(
                grid.get_node_in_location(kirigiri.coordinates))
        #print('Kirigiri direction is ' + kirigiri.direction)

        # Move the two players in forwards in the direction they are facing
        # However, if they are currently trapped, do not move them.
        if not naegi.trapped:
            grid.move_player_forward(naegi)
        if not kirigiri.trapped:
            grid.move_player_forward(kirigiri)

        # For the player's reaction faces
        # Scoring
        if(naegi.scored):
            naegi_score_frames += 1
        elif(kirigiri.scored):
            kirigiri_score_frames += 1
        # Trapping
        if(naegi.trapped):
            naegi_trap_frames += 1
        if(kirigiri.trapped):
            kirigiri_trap_frames += 1

        # Reset scored player faces when frames have been reached
        if(naegi_score_frames >= PLAYER_SMILE_FRAMES):
            naegi.scored = False
            naegi_score_frames = 0
        if(kirigiri_score_frames >= PLAYER_SMILE_FRAMES):
            kirigiri.scored = False
            kirigiri_score_frames = 0

        # Reset trapped player faces when frames have been reached
        if(naegi_trap_frames >= PLAYER_TRAP_FRAMES):
            naegi.trapped = False
            naegi_trap_frames = 0
        if(kirigiri_trap_frames >= PLAYER_TRAP_FRAMES):
            kirigiri.trapped = False
            kirigiri_score_frames = 0

        # Set the won flags whenever one of them has won or not
        if(naegi.score >= WINNING_SCORE):
            naegi_won = True
        if(kirigiri.score >= WINNING_SCORE):
            kirigiri_won = True

        ####################################################################
        # Event Handling
        ####################################################################
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
            if event.type == KEYDOWN:
                # User pressed a key on the keyboard
                if event.key == K_DOWN:
                    if(naegi.direction != 'up'):
                        # Change the direction of Naegi to down
                        naegi.direction = 'down'
                elif event.key == K_UP:
                    if(naegi.direction != 'down'):
                        # Change the direction of Naegi to up
                        naegi.direction = 'up'
                elif event.key == K_RIGHT:
                    if(naegi.direction != 'left'):
                        # Change the direction of Naegi to right
                        naegi.direction = 'right'
                elif event.key == K_LEFT:
                    if(naegi.direction != 'right'):
                        # Change the direction of Naegi to left
                        naegi.direction = 'left'
                elif event.key == K_ESCAPE:
                    # Quit the game
                    sys.exit(0)

        ####################################################################
        # Display updating
        ####################################################################

        # Clear the screen with white
        screen.fill(WHITE)

        # Render the tile bg
        bg_img_rect = tile_img.get_rect()
        nrows = int(screen.get_height() / bg_img_rect.height) + 1
        ncols = int(screen.get_width() / bg_img_rect.width) + 1

        for y in range(nrows):
            for x in range(ncols):
                bg_img_rect.topleft = (x * bg_img_rect.width, y *
                        bg_img_rect.height)
                screen.blit(tile_img, bg_img_rect)

        # Fill the game area with white
        game_rect = ((16, 12), (32 * 24, 32 * 18))
        pygame.draw.rect(screen, WHITE, game_rect)

        # Fill the player area with white
        player_area_rect = ((16 + (32 * 24), 12), (232, 576))
        pygame.draw.rect(screen, WHITE, player_area_rect)

        # Draw the grid and its elements
        # Highlight the pathfinding of the AI
        #grid.highlight_path(pathfinder.open_list, OPEN_LIST_COLOR)
        #grid.highlight_path(pathfinder.closed_list, CLOSED_LIST_COLOR)
        #grid.highlight_path(pathfinder.path, PATH_LIST_COLOR)
        grid.draw_grid()
        grid.draw_monokuma()
        grid.draw_walls()
        grid.draw_traps()
        players_ui.draw_text()
        players_ui.draw_score(naegi.score, kirigiri.score)
        grid.draw_player(naegi)
        grid.draw_player(kirigiri)

        # Display player ui
        # Naegi scoring
        if(naegi_score_frames > 0 and naegi_score_frames <
                PLAYER_SMILE_FRAMES):
            players_ui.draw_image(True, False)
        # Kirigiri scoring
        elif(kirigiri_score_frames > 0 and kirigiri_score_frames <
                PLAYER_SMILE_FRAMES):
            players_ui.draw_image(False, True)
        # Naegi trapped
        elif(naegi_trap_frames > 0 and naegi_trap_frames < PLAYER_TRAP_FRAMES):
            players_ui.draw_image(False, False, True)
            # Draw the explosion sprite
            #grid.draw_explosions(naegi.coordinates, naegi_trap_frames)
        # Kirigiri trapped
        elif(kirigiri_trap_frames > 0 and kirigiri_trap_frames <
                PLAYER_TRAP_FRAMES):
            players_ui.draw_image(False, False, False, True)
        else:
            players_ui.draw_image()

        # Update everything
        pygame.display.flip()

    # Clear the screen
    screen.fill(WHITE)
    # Check the winner
    if(kirigiri_won):
        print('Kirigiri won!')
    else:
        print('Naegi won!')

if __name__ == '__main__':
    main()
