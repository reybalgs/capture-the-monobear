# pathfinder.py
#
# Python file containing the source and logic for the pathfinder of the AI
# opponent in the game.
#
# Uses the A* search algorithm with a Manhattan heuristic.

class Pathfinder():
    def __init__(self):
        # Initialize the closed list of nodes
        self.closed_list = []
        # Initialize the open list of nodes
        self.open_list = []
        print('Pathfinder initialized')
