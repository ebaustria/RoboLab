#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import List, Tuple, Dict, Union


@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


Weight = int
"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Path:

    def __init__(self, start, target, weight, start_dir, end_dir):
        self.start = start
        self.target = target
        self.weight = weight
        self.start_dir = start_dir
        self.end_dir = end_dir


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate or extend
    it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None
        self.planet_dict = {}

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it

        Example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
        path_to_add = Path(start[0], target[0], weight, start[1], target[1])
        # self.planet_dict[path_to_add.start] = {}

        if path_to_add.start not in self.planet_dict:
            self.planet_dict[path_to_add.start] = {}
            self.planet_dict[path_to_add.start][path_to_add.start_dir] = (path_to_add.target, path_to_add.end_dir,
                                                                          path_to_add.weight)
        else:
            self.planet_dict[path_to_add.start][path_to_add.start_dir] = (path_to_add.target, path_to_add.end_dir,
                                                                          path_to_add.weight)
        if path_to_add.target not in self.planet_dict and path_to_add.target is not None:
            self.planet_dict[path_to_add.target] = {}
            self.planet_dict[path_to_add.target][path_to_add.end_dir] = (path_to_add.start, path_to_add.start_dir,
                                                                         path_to_add.weight)
        else:
            self.planet_dict[path_to_add.target][path_to_add.end_dir] = (path_to_add.start, path_to_add.start_dir,
                                                                         path_to_add.weight)

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths

        Example:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2),
                    Direction.WEST: ((0, 3), Direction.NORTH, 1)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
        return self.planet_dict

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[None, List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: 2-Tuple[List, Direction]
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
        pass
