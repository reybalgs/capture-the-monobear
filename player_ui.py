# player_ui.py
#
# Contains code for the displaying of the UI elements of the players.

import random, os, sys, pygame
from pygame.locals import *

pygame.font.init()

# CONSTANTS
# Screen resolution
SCREEN_X = 1024
SCREEN_Y = 600
# Color for Naegi's text and icon
NAEGI_COLOR = (120,150,90)
# Color for Kirigiri's text and icon
KIRIGIRI_COLOR = (200,160,200)

# The font for the player text.
text_font = pygame.font.Font(os.path.join(".", "orange_juice.ttf"), 48)
winner_font = pygame.font.Font(os.path.join(".", "orange_juice.ttf"), 140)

class UI_Players():
    def draw_score(self, naegi_score = 0, kirigiri_score = 0):
        """
        Draws the text for the two player's scores. Receives the said scores as
        function arguments. Both are defaulted to 0 for testing cases.
        """
        screen = pygame.display.get_surface()

        # Render Naegi's score text
        naegi_text = text_font.render(str(naegi_score), 1, NAEGI_COLOR)
        # Render Kirigiri's score text
        kirigiri_text = text_font.render(str(kirigiri_score), 1,
            KIRIGIRI_COLOR)

        # Blit the two text
        screen.blit(naegi_text, (960, 24))
        screen.blit(kirigiri_text, (960, 308))

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

    def draw_win_text(self, winner):
        """
        Draws winning text on the center of the screen, depending on who the
        winner is.
        """
        screen = pygame.display.get_surface()

        if winner is 'naegi':
            text = winner_font.render("Naegi won!", 1, NAEGI_COLOR)
        else:
            text = winner_font.render("Kirigiri won!", 1, KIRIGIRI_COLOR)
        screen.blit(text, ((SCREEN_X / 2) - (text.get_rect().width / 2),
            (SCREEN_Y / 2) - (text.get_rect().height / 2)))

    def draw_image(self, naegi_scored=False, kirigiri_scored=False,
            naegi_trapped=False, kirigiri_trapped=False):
        """
        Draws the images of the two players on screen.

        If <player>_scored is True, display the image of the player being happy
        """
        screen = pygame.display.get_surface()

        # Initialize Naegi's image
        if(naegi_scored):
            naegi = pygame.image.load(os.path.join("images",
                "naegi_happy.png"))
        elif(naegi_trapped):
            naegi = pygame.image.load(os.path.join("images",
                "naegi_frustrated.png"))
        else:
            naegi = pygame.image.load(os.path.join("images", "naegi_full.png"))
        # Initialize Kirigiri's image
        if(kirigiri_scored):
            kirigiri = pygame.image.load(os.path.join("images",
                "kirigiri_happy.png"))
        elif(kirigiri_trapped):
            kirigiri = pygame.image.load(os.path.join("images",
                "kirigiri_frustrated.png"))
        else:
            kirigiri = pygame.image.load(os.path.join("images", 
                "kirigiri_full.png"))

        # Get per pixel alpha transparency of the images
        naegi.convert_alpha()
        kirigiri.convert_alpha()

        # Blit the images onto the screen
        screen.blit(naegi, (800,20))
        screen.blit(kirigiri, (778,310))
