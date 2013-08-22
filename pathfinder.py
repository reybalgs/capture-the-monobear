# pathfinder.py
#
# Python file containing the source and logic for the pathfinder of the AI
# opponent in the game.
#
# Uses the A* search algorithm with a Manhattan heuristic.

import math, pdb

from grid import *
from sets import Set

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

    def print_path(self):
        """
        Prints the entirety of the path list.
        """
        print('Path list:')
        for node in self.path:
            print(str(node.coordinates))

    def clear_node_parents(self):
        """
        Resets the parents of all the nodes in the grid to none.
        """
        for row in self.grid.node_array:
            for node in row:
                node.parent = None

    def remove_list_duplicates(self, list):
        """
        Removes duplicate entries in the given list.
        """
        output = []
        for x in list:
            if x not in output:
                output.append(x)
        return output

    def get_direction_to_next_node_v2(self, current_node):
        """
        Returns the direction that the AI should turn to in order to reach the
        next node in its path list.

        Updated to use the self.path variable, rather than the closed list.
        """

        print('Current node is at ' + str(current_node.coordinates))
        try:
            index = self.path.index(current_node)
        except:
            return 1

        # Get the next node from the current node in the list
        try:
            next_node = self.path[index + 1]
        except:
            return 1
        print('Next node is at ' + str(next_node.coordinates))

        # Return the direction the AI needs to point to, depending on the
        # location of the next node
        if(next_node.getX() > current_node.getX()):
            print('Return right direction')
            return 'right'
        elif(next_node.getX() < current_node.getX()):
            print('Return left direction')
            return 'left'
        elif(next_node.getY() > current_node.getY()):
            print('Return down direction')
            return 'down'
        elif(next_node.getY() < current_node.getY()):
            print('Return up direction')
            return 'up'

    def get_direction_to_next_node(self, current_node):
        """
        Returns the direction that the AI should turn to in order to reach the
        next node in its path list.
        """

        print('Current node is at ' + str(current_node.coordinates))
        # Find the index of the current node in relation to the closed list
        try:
            index = self.closed_list.index(current_node)
        except:
            return 1

        # Get the next node from the current node in the list
        try:
            next_node = self.closed_list[index + 1]
        except:
            return 1
        print('Next node is at ' + str(next_node.coordinates))

        # Return the direction the AI needs to point to, depending on the
        # location of the next node
        if(next_node.getX() > current_node.getX()):
            return 'right'
        elif(next_node.getX() < current_node.getX()):
            return 'left'
        elif(next_node.getY() > current_node.getY()):
            return 'down'
        elif(next_node.getY() < current_node.getY()):
            return 'up'

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

    def is_node_in_open_list(self, node):
        """
        Checks if the given node is in the open list and returns a boolean
        value depending on the result.
        """
        for entry in self.closed_list:
            if entry is node:
                print(str(node.coordinates) + ' is in open list!')
                return True
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
                1)).contents is not WALL and
                self.grid.get_node_in_location((node.getX(), node.getY() -
                1)).contents is not TRAP) and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((
                    node.getX(), node.getY() - 1)))):
            print('North node added')
            adjacent_nodes.append(self.grid.get_node_in_location((node.getX(),
                node.getY() - 1)))
        # Add the south node
        if((node.getY() + 1) <= 17 and
                (self.grid.get_node_in_location((node.getX(), node.getY() +
                1)).contents is not WALL and
                self.grid.get_node_in_location((node.getX(), node.getY() +
                1)).contents is not TRAP) and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((
                    node.getX(), node.getY() + 1)))):
            print('South node added')
            adjacent_nodes.append(self.grid.get_node_in_location((node.getX(),
                (node.getY() + 1))))
        # Add the east node
        if((node.getX() + 1) <= 23 and
                (self.grid.get_node_in_location((node.getX() + 1,
                node.getY())).contents is not WALL and
                self.grid.get_node_in_location((node.getX() + 1,
                node.getY())).contents is not TRAP) and not
                self.is_node_in_closed_list(self.grid.get_node_in_location((node.getX()
                    + 1, node.getY())))):
            print('East node added')
            adjacent_nodes.append(self.grid.get_node_in_location(((node.getX() +
                1), node.getY())))
        # Add the west node
        if((node.getX() - 1) >= 0 and
                (self.grid.get_node_in_location((node.getX() - 1,
                node.getY())).contents is not WALL and
                self.grid.get_node_in_location((node.getX() - 1,
                node.getY())).contents is not TRAP) and not
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

    def get_movement_cost_old(self, node):
        return ((math.fabs(node.getX() - self.start_node.getX()) *
            MOVEMENT_COST) + (math.fabs(node.getY() - self.start_node.getY()) *
                MOVEMENT_COST))

    def get_movement_cost(self, node):
        """
        Finds the movement cost needed to traverse from the start_node to the
        end_node.

        Returns the value G used in the A* algorithm.
        """
        # Find the travel cost as we move through the closed list.
        cost = MOVEMENT_COST * (len(self.closed_list) - 1)

        return cost + MOVEMENT_COST

    def find_lowest_f_in_list(self, list, end_node):
        """
        Returns the node with the lowest F score in the given list.
        """
        best_node = list[0]
        for node in list:
            if((self.get_movement_cost_old(node) +
                    self.manhattan_heuristic(node, end_node)) <
                    self.get_movement_cost_old(best_node) +
                    self.manhattan_heuristic(best_node, end_node)):
                # This node is better, set it as the best node
                best_node = node
        return best_node

    def reconstruct_path(self, end_node):
        """
        Reconstructs a path from the given end_node to the root of the path by
        tracing the parents of the nodes until no further parent is found.
        """
        if end_node.parent:
            # Set the boolean flag for the "do-while" loop
            parent = True
        else:
            return self.path.append(end_node)
        current_node = end_node
        while parent:
            # Add the current node to the path
            self.path.append(current_node)
            print('Adding ' + str(current_node.coordinates) + ' to path')
            # Print the path list
            self.print_path()
            if current_node.parent:
                # The current node has a parent, set the current node to that
                # node
                current_node = current_node.parent
            else:
                # The current node has no parent, we have reached the start
                # Reverse the list first, so that the AI can traverse it
                parent = False
                self.path.reverse()
                print('Path reversed! New path list:')
                self.print_path()
                return self.path
        #if end_node.parent is not None:
        #    current_node = end_node
        #    while current_node.parent is not None:
        #        # Add the current node to the path
        #        self.path.append(current_node)
        #        print('Adding ' + str(current_node.coordinates) + ' to path')
        #        # Print the path list
        #        self.print_path()
        #        current_node = current_node.parent
        #else:
        #    self.path.append(end_node)
        # Reverse the path list
        #self.path.reverse()
        #print('Path reversed! New path list:')
        #self.print_path()
        #return self.path

    def find_path_to_monokuma_v2(self):
        """
        An update to the previous function of finding the path to take to get
        to the monokuma node. Still based on the A* algorithm, however, I'm
        closely basing this code on the pseudocode available on Wikipedia.
        """
        #pdb.set_trace()
        # Clean up the lists used by the pathfinder
        self.closed_list = []
        self.open_list = []
        self.path = []

        # Clear the parents of the nodes
        self.clear_node_parents()
        print('Node parents cleared!')

        # Find the first node containing monokuma.
        # Raise an error if there are no monokumas.
        try:
            monokuma_node = self.grid.find_nodes_containing(MONOKUMA).pop(0)
        except IndexError:
            print('No monokumas found!')

        # Add the starting node to the open list.
        if not self.is_node_in_open_list(self.start_node):
            self.open_list.append(self.start_node)
        # Print open nodes
        self.print_open_list()

        while len(self.open_list):
            # Keep going with the algorithm while we still have something in
            # the open list, or until we have found the monokuma node
            # 
            # Get the node in the open list with the lowest F score value.
            best_node = self.find_lowest_f_in_list(self.open_list,
                    monokuma_node)
            print('Best node is ' + str(best_node.coordinates) + ' with ' +
                    'F score of ' + str(self.get_movement_cost_old(best_node) +
                        self.manhattan_heuristic(best_node, monokuma_node)))
            #for node in self.open_list:
            #    if((self.get_movement_cost_old(node) +
            #            self.manhattan_heuristic(node, monokuma_node)) <
            #            (self.get_movement_cost_old(node) +
            #            self.manhattan_heuristic(node, monokuma_node))):
            #        # Since the F score is better, let's set that as the best
            #        # node
            #        best_node = node
            #        print('Best node is ' + str(best_node.coordinates) + 
            #                ' with ' + 'F score of ' +
            #                str(self.get_movement_cost_old(best_node) +
            #                self.manhattan_heuristic(best_node,
            #                monokuma_node)))
            # Let's check if the current node is the monokuma node
            if best_node == monokuma_node:
                print('We have found the monokuma node! It is at ' +
                        str(best_node.coordinates))
                return self.reconstruct_path(best_node)

            # Remove the current node from the openset
            self.open_list.remove(best_node)
            # Add the current node to the closed set
            if best_node not in self.closed_list:
                self.closed_list.append(best_node)

            adjacent_nodes = self.find_adjacent_nodes(best_node)
            #print('Adjacent nodes:')
            #for node in adjacent_nodes:
            #    print(str(node.coordinates))
            for neighbor_node in adjacent_nodes:
                tentative_g = (self.get_movement_cost_old(best_node) +
                        MOVEMENT_COST)
                print('Tentative G: ' + str(tentative_g))
                print('G of ' + str(best_node.coordinates) + ': ' +
                        str(self.get_movement_cost_old(best_node)))
                if(neighbor_node in self.closed_list and tentative_g
                        >= self.get_movement_cost_old(neighbor_node)):
                    # The neighbor node is already in the closed list and it
                    # doesn't really have an attractive G cost.
                    print('Neighbor node ' + str(neighbor_node.coordinates) + 
                            ' not in closed list and its tentative G score ' +
                            'of ' + str(tentative_g) + ' is greater or equal '
                            + 'to its actual G score')
                #if((not self.is_node_in_closed_list(neighbor_node)) and
                #        tentative_g <
                #        self.get_movement_cost_old(neighbor_node)):
                else:
                #if(neighbor_node not in self.closed_list or (tentative_g <
                #        self.get_movement_cost_old(neighbor_node))):
                    # Set the parent of the current neighbor node to the
                    # current node, to trace the path later
                    neighbor_node.parent = best_node
                    # Add that neighbor to the open set
                    if neighbor_node not in self.open_list:
                        print('Neighbor node ' +
                                str(neighbor_node.coordinates) + ' is not ' +
                                'in open list, appending...')
                        self.open_list.append(neighbor_node)
                        self.print_open_list()
                        self.print_closed_list()
                        #pdb.set_trace()

            # Set the lists so there are no duplicates
            #self.open_list = set(self.open_list)
            #self.closed_list = set(self.closed_list)

            # Print the lists
            self.print_open_list()
            self.print_closed_list()
            self.print_path()

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
            last_closed_node = self.closed_list[len(self.closed_list) - 1]
            adjacent_nodes = self.find_adjacent_nodes(last_closed_node)
            # Keep running the A* algorithm while Monokuma is still not found
            if(len(adjacent_nodes)):
                # Clean up the open list
                print('Adjacent node list has length ' +
                    str(len(adjacent_nodes)) + ' cleaning up open list!')
                self.open_list = []
            # Add the adjacent nodes from the end of the closed list to the
            # open list
            for node in adjacent_nodes:
                print('Node at ' + str(node.coordinates) + ' found as an ' +
                        'adjacent node!')
                self.open_list.append(node)
            self.print_closed_list()
            self.print_open_list()
            # Now let's find the best node
            if(len(self.open_list) == 0):
                print('No open nodes! Returning to game function')
                print('Monokuma node is at ' + str(monokuma_node.coordinates))
                return
            best_node = self.open_list[0]
            for node in self.open_list:
                node_score = (self.get_movement_cost(node) +
                        self.manhattan_heuristic(node, monokuma_node))
                best_score = (self.get_movement_cost(
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
                    # If H values are the same, let's favor the one with the
                    # lower G cost.
                    elif(self.get_movement_cost(node) <
                            self.get_movement_cost(best_node)):
                        print('Node on ' + str(node.coordinates) + ' has ' +
                                'equal F score with node ' +
                                str(best_node.coordinates) + ' (' +
                                str(node_score) + '), however, node G value ' +
                                str(self.get_movement_cost(node)) + ' is ' +
                                'lower than best node with ' +
                                str(self.get_movement_cost(best_node)))
                        best_node = node
                    # If they are really the same, just get the latest one
                    else:
                        print('Both current node ' + str(node.coordinates) + 
                                ' and best node ' + str(best_node.coordinates)
                                + ' has same G and H scores, choosing ' +
                                'current node.')
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
        # Initialize the closed list of nodes
        self.closed_list = []
        # Initialize the open list of nodes
        self.open_list = []
        # Initialize the path that we will actually follow
        self.path = []
        # Initialize the grid that the pathfinder will use
        self.grid = grid
        # Initialize the starting node that the pathfinder will use as a
        # reference
        self.start_node = start_node
        print('Pathfinder initialized')
        print('Start node is at ' + str(self.start_node.coordinates))
