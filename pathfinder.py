# pathfinder.py
#
# Python file containing the source and logic for the pathfinder of the AI
# opponent in the game.
#
# Uses the A* search algorithm with a Manhattan heuristic.

import math, pdb

from grid import *

# Entities
NONE = 0
NAEGI = 1
KIRIGIRI = 2
WALL = 3
TRAP = 4
MONOKUMA = 5

# Coordinates
X = 0
Y = 0

# Movement cost
MOVEMENT_COST = 10

class Pathfinder():
    def print_closed_list(self):
        """
        Prints the entirety of the closed list. Useful for debugging.
        """
        print('Closed list:')
        for node in self.closed_list:
            print(str(node.coordinates))

    def print_open_list(self):
        """
        Prints the entirety of the open list. Useful for debugging.
        """
        print('Open list:')
        for node in self.open_list:
            print(str(node.coordinates))

    def is_monokuma_in_closed_list(self):
        """
        Function that simply checks if monokuma is already in the closed list,
        and returns either True or False depending on the result.
        """
        for node in self.closed_list:
            if node.contents is MONOKUMA:
                print('Monokuma in closed list!')
                return True
        # No monokuma found
        print('Monokuma not yet in closed list')
        return False

    def is_node_in_closed_list(self, node):
        """
        Function that checks if the given node is in the closed list and
        returns a boolean value depending on the result.
        """
        for entry in self.closed_list:
            if entry is node:
                return True
        # Nothing found
        return False

    def find_adjacent_nodes(self, node):
        """
        Finds the four nodes adjacent to the given node and returns them as a
        list.
        """
        adjacent_nodes = []

        # Note: Only add nodes if they are within the scope of the grid, if
        # they are empty or monokuma, and if they are not in the closed list
        # Add the north node
        if((node.getY() - 1) >= 0 and
                (self.grid.get_node_in_location((node.getX(), node.getY() -
                1)).contents is NONE or
                self.grid.get_node_in_location((node.getX(), node.getY() -
                1)).contents is MONOKUMA and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((
                    node.getX(), node.getY() - 1))))):
            print('North node added')
            adjacent_nodes.append(self.grid.get_node_in_location((node.getX(),
                node.getY() - 1)))
        # Add the south node
        if((node.getY() + 1) <= 17 and
                (self.grid.get_node_in_location((node.getX(), node.getY() +
                1)).contents is NONE or
                self.grid.get_node_in_location((node.getX(), node.getY() +
                1)).contents is MONOKUMA)and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((
                    node.getX(), node.getY() + 1)))):
            print('South node added')
            adjacent_nodes.append(self.grid.get_node_in_location((node.getX(),
                (node.getY() + 1))))
        # Add the east node
        if((node.getX() + 1) <= 23 and
                (self.grid.get_node_in_location((node.getX() + 1,
                node.getY())).contents is NONE or
                self.grid.get_node_in_location((node.getX() + 1,
                node.getY())).contents is MONOKUMA) and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((node.getX()
                    + 1, node.getY())))):
            print('East node added')
            adjacent_nodes.append(self.grid.get_node_in_location(((node.getX() +
                1), node.getY())))
        # Add the west node
        if((node.getX() - 1) >= 0 and
                (self.grid.get_node_in_location((node.getX() - 1,
                node.getY())).contents is NONE or
                self.grid.get_node_in_location((node.getX() - 1,
                node.getY())).contents is MONOKUMA) and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((node.getX()
                    - 1, node.getY())))):
            print('West node added')
            adjacent_nodes.append(self.grid.get_node_in_location(((node.getX() -
                1), node.getY())))

        return adjacent_nodes

    def manhattan_heuristic(self, node, end_node):
        """
        Implementation of the Manhattan heuristic, whose value is MOVEMENT_COST
        time how many nodes does it take to directly get from that node to the
        end node.

        Return the value H used in the A* algorithm
        """
        # First let's get the X difference between the node and the finish node
        x_diff = (math.fabs(node.getX() - end_node.getX())) * MOVEMENT_COST
        # Now let's get the Y difference between them
        y_diff = (math.fabs(node.getY() - end_node.getY())) * MOVEMENT_COST

        return x_diff + y_diff

    def get_movement_cost(self, start_node, end_node):
        """
        Finds the movement cost needed to traverse from the start_node to the
        end_node.

        Returns the value G used in the A* algorithm.
        """
        # Find the X difference between the two nodes
        x_diff = (math.fabs(start_node.getX() - end_node.getX())) * MOVEMENT_COST
        # Find the Y difference between the two nodes
        y_diff = (math.fabs(start_node.getY() - end_node.getY())) * MOVEMENT_COST

        return x_diff + y_diff

    def find_path_to_monokuma(self):
        """
        Function that updates the closed list to reflect on the possibly
        shortest path to Monokuma, using the data on the grid at the moment the
        function was called.
        """
        #pdb.set_trace()
        # First, we have to clear the closed and open lists
        self.closed_list = []
        self.open_list = []

        # Now let's get the node containing Monokuma. Only get the first
        # Monokuma in the case of multiple monokumas.
        monokuma_node = self.grid.find_nodes_containing(MONOKUMA).pop(0)

        # Add the current (first) node to the closed list
        self.closed_list.append(self.start_node)

        while not self.is_monokuma_in_closed_list():
            # Keep running the A* algorithm while Monokuma is still not found
            # Add the adjacent nodes from the end of the closed list to the
            # open list
            for node in self.find_adjacent_nodes(
                    self.closed_list[len(self.closed_list) - 1]):
                self.open_list.append(node)
            self.print_closed_list()
            self.print_open_list()
            # Now let's find the best node
            best_node = self.open_list[0]
            for node in self.open_list:
                node_score = (self.get_movement_cost(self.start_node, node) +
                        self.manhattan_heuristic(node, monokuma_node))
                best_score = (self.get_movement_cost(self.start_node,
                    best_node) + self.manhattan_heuristic(best_node,
                    monokuma_node))
                print('Best node is currently at ' + str(best_node.coordinates)
                        + ' with F score of ' + str(best_score))
                print('Current node is at ' + str(node.coordinates) + ' with '
                        + 'F score of ' + str(node_score))
                if node_score < best_score:
                    # We have found a better node
                    print('Node on ' + str(node.coordinates) + ' with score ' +
                            'of ' + str(node_score) + ' is less than best ' +
                            'node on ' + str(best_node.coordinates) + ' with '
                            + 'score of ' + str(best_score))
                    best_node = node
                elif node_score == best_score:
                    # The lastest node is equal, however, let's check their
                    # manhattan heuristic values first. Favor the one with the
                    # lower H value.
                    if(self.manhattan_heuristic(node, monokuma_node) <
                            self.manhattan_heuristic(best_node,
                            monokuma_node)):
                        print('Node on ' + str(node.coordinates) + ' has ' +
                                'equal score with node ' +
                                str(best_node.coordinates) + ' (' +
                                str(node_score) + '), however, node H value ' +
                                str(self.manhattan_heuristic(node,
                                monokuma_node)) + ' is lower than best node ' +
                                ' with ' +
                                str(self.manhattan_heuristic(best_node,
                                monokuma_node)))
                        best_node = node
            # Remove the best node from the open list
            self.open_list.pop(self.open_list.index(best_node))
            # Put the best node in the closed list
            self.closed_list.append(best_node)

        print('Monokuma is found at ' +
                str(self.closed_list[len(self.closed_list) - 1]) + '! Path is: ')
        self.print_closed_list()
        # Return the closed list as the path we will follow
        return self.closed_list

    def __init__(self, grid, start_node):
        # Initialize the closed list of nodes, this is the path we will follow
        self.closed_list = []
        # Initialize the open list of nodes
        self.open_list = []
        # Initialize the grid that the pathfinder will use
        self.grid = grid
        # Initialize the starting node that the pathfinder will use as a
        # reference
        self.start_node = start_node
        print('Pathfinder initialized')
        print('Start node is at ' + str(self.start_node.coordinates))
