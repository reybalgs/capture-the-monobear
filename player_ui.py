# player_ui.py
#
# Contains code for the displaying of the UI elements of the players.

import random, os, sys, pygame
from pygame.locals import *

class UI_Players():
    def draw_image(self):
        """
        Draws the images of the two players on screen.
        """
        screen = pygame.display.get_surface()

        # Initialize Naegi's image
        naegi = pygame.image.load(os.path.join("images", "naegi_full.png"))
        kirigiri = pygame.image.load(os.path.join("images", 
            "kirigiri_full.png"))

        # Blit the images onto the screen
        screen.blit(naegi, (580,20))
        screen.blit(kirigiri, (550,310))
