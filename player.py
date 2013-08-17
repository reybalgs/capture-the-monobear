# player.py
#
# Python file containing the source for the players of the game.

class Player():
    def __init__(self, name, coordinates = (0,0), direction='right', 
            score = 0):
        self.name = name
        self.coordinates = coordinates
        self.direction = direction
        self.score = score
