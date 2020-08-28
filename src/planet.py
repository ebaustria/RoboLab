#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import math
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
        self.scanned_nodes = []
        self.unexplored_edges = {}

    # If the start point of the path to add is not in the planet dictionary, an entry is created for it. The same is
    # done for the end point of the path to add. Afterwards, a key-value pair is added to the inner dictionaries of the
    # start and end points. If the inner dictionaries of either the start point or the end point contain 4 key-value
    # pairs and the respective point is not in the list of fully scanned nodes, then it is added to that list.
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

        path_to_add = Path(start[0], target[0], weight, start[1], target[1])

        if path_to_add.start not in self.planet_dict and path_to_add.start is not None:
            self.planet_dict[path_to_add.start] = {}

        if path_to_add.target not in self.planet_dict and path_to_add.target is not None:
            self.planet_dict[path_to_add.target] = {}

        self.planet_dict[path_to_add.start][path_to_add.start_dir] = (path_to_add.target, path_to_add.end_dir,
                                                                      path_to_add.weight)

        self.planet_dict[path_to_add.target][path_to_add.end_dir] = (path_to_add.start, path_to_add.start_dir,
                                                                     path_to_add.weight)

        if len(self.planet_dict[path_to_add.start]) == 4 and path_to_add.start not in self.scanned_nodes:
            self.scanned_nodes.append(path_to_add.start)

        if len(self.planet_dict[path_to_add.target]) == 4 and path_to_add.target not in self.scanned_nodes:
            self.scanned_nodes.append(path_to_add.target)

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

        return self.planet_dict

    # Returns a list of all the nodes in the planet dictionary.
    def get_nodes(self) -> List[Tuple[int, int]]:
        nodes = []

        for node in self.planet_dict.keys():
            nodes.append(node)

        return nodes

    # Returns the next direction to take in the shortest path (the second element in the first tuple in the shortest
    # path).
    def shortest_next_dir(self, start: Tuple[int, int], target: Tuple[int, int]) -> Direction:
        shortest_path = self.shortest_path(start, target)

        return shortest_path[0][1]

    # Maps an unexplored edge to a node in the dictionary of unexplored edges (used when scanning for edges at a node).
    def add_unexplored_edge(self, node: Tuple[int, int], direction: Direction) -> None:
        if node not in self.unexplored_edges:
            self.unexplored_edges[node] = []

        self.unexplored_edges[node].append(direction)

    # Removes an unexplored edge from the list of unexplored edges that is mapped to a node in the dictionary of
    # unexplored edges. Afterwards, if an empty list of unexplored edges is mapped to the node, the key-value pair is
    # removed from the dictionary.
    def remove_unexplored_edge(self, start: Tuple[Tuple[int, int], Direction], end: Tuple[Tuple[int, int], Direction])\
            -> None:
        start_dir = start[1]
        end_dir = end[1]
        start_point = start[0]
        end_point = end[0]

        if start_point in self.unexplored_edges and start_dir in self.unexplored_edges[start_point]:
            self.unexplored_edges[start_point].remove(start_dir)

            if len(self.unexplored_edges[start_point]) == 0:
                del self.unexplored_edges[start_point]

        if end_point in self.unexplored_edges and end_dir in self.unexplored_edges[end_point]:
            self.unexplored_edges[end_point].remove(end_dir)

            if len(self.unexplored_edges[end_point]) == 0:
                del self.unexplored_edges[end_point]

    # Implementation of Dijkstra's algorithm.
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[None, List[Tuple[Tuple[int, int],
                                                                                                       Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: 2-Tuple[List, Direction]
        """

        unvisited = {}
        current_node = start
        precursor_compass_dict = {}
        shortest_path = []

        if start == target:
            return shortest_path

        # If the target node is not in the planet dictionary, then it cannot be found/reached. Return None.
        if target not in self.planet_dict.keys():
            return None

        # If no path exists between the start node and the target, return None.
        if not self.path_exists(start, target):
            return None

        # All nodes are marked unvisited. The start node is given the tentative distance of 0, and the other nodes are
        # given the tentative distance of infinity.
        for node in self.planet_dict.keys():
            if node == start:
                unvisited[node] = 0
            else:
                unvisited[node] = math.inf

        # Until the target has been marked as visited: check the neighbors of the current node, reassign neighbors'
        # tentative distances, and map tentative precursor nodes to neighbors, if necessary.
        while target in unvisited:
            current_neighbors = self.planet_dict[current_node].items()
            for (start_dir, path) in current_neighbors:
                if path[0] in unvisited.keys() and path[2] != -1:
                    neighbor = path[0]
                    neighbor_weight = path[2]
                    tentative_dist = unvisited[neighbor]
                    if unvisited[current_node] + neighbor_weight < tentative_dist:
                        tentative_dist = unvisited[current_node] + neighbor_weight
                        unvisited[neighbor] = tentative_dist
                        precursor_compass_dict[neighbor] = (current_node, start_dir)

            # Mark the current node as visited after checking its neighbors.
            unvisited.pop(current_node)

            # Find the unvisited node with the lowest tentative distance and set it as the new current node.
            for (node, distance) in unvisited.items():
                if distance == min(unvisited.values()):
                    current_node = node

        # Exit the while loop when the target has been marked as visited and initialize the shortest path.
        if target in precursor_compass_dict.keys():
            shortest_path.append(precursor_compass_dict[target])
        else:
            return None

        # Iterate over the shortest path until the start node is reached. On every iteration, add the respective node's
        # precursor to the shortest path. When the iteration is finished, reverse the shortest path and return it as the
        # result.
        for (coord, direc) in shortest_path:
            if coord != start:
                shortest_path.append(precursor_compass_dict[coord])

        shortest_path.reverse()

        return shortest_path

    # Helper function for determining whether a given target node can be reached from a given start node. Intended to
    # prevent shortest_path from attempting to create a shortest path to a node that is located in the planet dictionary
    # but cannot be reached.
    def path_exists(self, start: Tuple[int, int], target: Tuple[int, int]) -> bool:
        to_check = []
        checked = []

        to_check.append(start)

        while len(to_check) != 0:
            removed = to_check[0]
            checked.append(removed)
            to_check.remove(removed)
            neighbors = self.planet_dict[removed].items()

            for (start_dir, path) in neighbors:
                if path[0] == target and path[2] == -1:
                    pass
                elif path[0] == target:
                    return True
                if path[0] not in checked and path[2] != -1:
                    to_check.append(path[0])

        return False

    # Calculates the distance of the shortest path between a start point and a target point.
    def shortest_distance(self, start: Tuple[int, int], target: Tuple[int, int]) -> Union[int, float]:
        shortest = self.shortest_path(start, target)

        if shortest is None:
            return math.inf

        weight = 0
        for (pos, direction) in shortest:
            weight += self.planet_dict[pos][direction][2]

        return weight
