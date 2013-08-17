# player_ui.py
#
# Contains code for the displaying of the UI elements of the players.

import random, os, sys, pygame
from pygame.locals import *

pygame.font.init()

# CONSTANTS
# Color for Naegi's text and icon
NAEGI_COLOR = (120,150,90)
# Color for Kirigiri's text and icon
KIRIGIRI_COLOR = (200,160,200)

# The font for the player text.
text_font = pygame.font.Font(os.path.join(".", "orange_juice.ttf"), 48)

class UI_Players():
    def draw_text(self):
        """
        Draws the name text of the two players on screen.
        """
        screen = pygame.display.get_surface()

        # Render Naegi's name text
        naegi_text = text_font.render("Naegi", 1, NAEGI_COLOR)
        # Render Kirigiri's name text
        kirigiri_text = text_font.render("Kirigiri", 1, KIRIGIRI_COLOR)

        # Rotate their text counterclockwise
        naegi_text = pygame.transform.rotate(naegi_text, 90)
        kirigiri_text = pygame.transform.rotate(kirigiri_text, 90)
        
        # Blit the two image
        screen.blit(naegi_text, (792,24))
        screen.blit(kirigiri_text, (792,308))

    def draw_image(self):
        """
        Draws the images of the two players on screen.
        """
        screen = pygame.display.get_surface()

        # Initialize Naegi's image
        naegi = pygame.image.load(os.path.join("images", "naegi_full.png"))
        kirigiri = pygame.image.load(os.path.join("images", 
            "kirigiri_full.png"))

        # Get per pixel alpha transparency of the images
        naegi.convert_alpha()
        kirigiri.convert_alpha()

        # Blit the images onto the screen
        screen.blit(naegi, (800,20))
        screen.blit(kirigiri, (778,310))
