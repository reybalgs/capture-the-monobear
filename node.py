#!/usr/bin/python

# node.py
#
# Python class containing code for defining nodes (squares in the game where
# the players move around and Monkuma with his obstacles spawn)

# Import future print function (from Python 3)
from __future__ import print_function

# CONSTANTS
X = 0
Y = 1

class Node():
    """
    The class pertaining to the nodes in the game.
    """
    def getX(self):
        """
        Returns the x coordinate of the Node.
        """
        x = self.coordinates[X]

        return x

    def getY(self):
        """
        Returns the y coordinate of the Node.
        """
        y = self.coordinates[Y]

        return y

    def get_coordinates(self):
        """
        Returns the (x, y) coordinates of the Node.
        """
        return self.coordinates

    def __init__(self, coord_x = 0, coord_y = 0, contents = 0, parent=None):
        # The contents of the node.
        self.contents = contents
        # The coordinates of the node.
        self.coordinates = (coord_x, coord_y)
        # The parent of the node.
        self.parent = parent

def main():
    # Main function for testing
    array_size_x = input('Enter array size (x): ')
    array_size_y = input('Enter array size (y): ')

    array = []
    # Create a list of lists (y list containing x lists)
    for i in range(0, array_size_y):
        x = []
        for j in range(0, array_size_x):
            node = Node(j, i, i + j)
            x.append(node)
        array.append(x)
 
    # Print the array of nodes
    print('Your array:')
    num = 1
    for column in array:
        for node in column:
            print('Node ' + str(num) + ': ' + str(node.coordinates) + ': ' + 
                    str(node.contents))
            num += 1

    print('')
    print('Grid view: ')
    for column in array:
        for node in column:
            print(' ' + str(node.contents), end='')
        print('')

if __name__ == '__main__':
    main()
