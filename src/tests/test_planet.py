#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    @unittest.skip('Example test, should not count in final test results')
    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class TestRoboLabPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        self.planet = Planet()

        self.planet.add_path(((0, 0), Direction.EAST), ((2, 0), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 4)
        self.planet.add_path(((2, 2), Direction.SOUTH), ((2, 0), Direction.NORTH), 2)
        self.planet.add_path(((1, 2), Direction.WEST), ((1, 2), Direction.NORTH), 1)

        """
                planet same:

                                            +--1--+
                (0, 2)---4---(2, 2)         |     |
                   |            |           |     |
                   1            2           +---(3, 2)
                   |            |
                (0, 0)---1---(2, 0)
                   |            |
                   |            |
                   +-----1------+
        """

        self.same = Planet()

        self.same.add_path(((0, 0), Direction.EAST), ((2, 0), Direction.WEST), 1)
        self.same.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.same.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 4)
        self.same.add_path(((2, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 2)
        self.same.add_path(((3, 2), Direction.WEST), ((3, 2), Direction.NORTH), 1)
        self.same.add_path(((0, 0), Direction.SOUTH), ((2, 0), Direction.SOUTH), 1)

        """
            planet blocked:
            X = blocked edge
            
        +----(0, 2)------3------(2, 2)----+
        |       |                  |      |
        |       |       +----2-----+      |
        1       |       |                 1
        |       X-----(1, 1)---X          |
        |               |      |          |
        +----(0, 0)-----X      +--(2, 0)--+
                |                   |
                +---------2---------+
        """
        self.blocked = Planet()

        self.blocked.add_path(((0, 0), Direction.EAST), ((1, 1), Direction.SOUTH), -1)
        self.blocked.add_path(((0, 0), Direction.SOUTH), ((2, 0), Direction.SOUTH), 2)
        self.blocked.add_path(((0, 0), Direction.WEST), ((0, 2), Direction.WEST), 1)
        self.blocked.add_path(((0, 2), Direction.SOUTH), ((1, 1), Direction.WEST), -1)
        self.blocked.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 3)
        self.blocked.add_path(((2, 0), Direction.WEST), ((1, 1), Direction.EAST), -1)
        self.blocked.add_path(((2, 0), Direction.EAST), ((2, 2), Direction.EAST), 1)
        self.blocked.add_path(((2, 2), Direction.SOUTH), ((1, 1), Direction.NORTH), 2)

        """
        planet big:
        X = blocked edge
        
            +-1-+
            |   |
            |   |
        (-1, 3)-+                            (3, 3)-------1---------+
                                                |                   |
                  +-------1--------+            2                   |
                  |                |            |                   |
            +--(0, 2)-----4-----(2, 2)---+   (3, 2)---2----+        |
            |     |                |     |      |          |        |
            |     |                |     |      1          |        |
            1     1                2     +-2-(3, 1)---3--(4, 1)-----+
            |     |                |                       |
            |     |                |                       |
            +--(0, 0)-----1-----(2, 0)---X---(3, 0)        1
                  |                |                       |
                  +-------1--------+                       |
                                                         (4, -1)
        """

        self.big = Planet()

        self.big.add_path(((0, 0), Direction.EAST), ((2, 0), Direction.WEST), 1)
        self.big.add_path(((0, 0), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.big.add_path(((0, 0), Direction.WEST), ((0, 2), Direction.WEST), 1)
        self.big.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 4)
        self.big.add_path(((0, 2), Direction.NORTH), ((2, 2), Direction.NORTH), 1)
        self.big.add_path(((2, 2), Direction.SOUTH), ((2, 0), Direction.NORTH), 2)
        self.big.add_path(((2, 2), Direction.EAST), ((3, 1), Direction.WEST), 2)
        self.big.add_path(((-1, 3), Direction.EAST), ((-1, 3), Direction.NORTH), 1)
        self.big.add_path(((0, 0), Direction.SOUTH), ((2, 0), Direction.SOUTH), 1)
        self.big.add_path(((2, 0), Direction.EAST), ((3, 0), Direction.WEST), -1)
        self.big.add_path(((3, 1), Direction.NORTH), ((3, 2), Direction.SOUTH), 1)
        self.big.add_path(((3, 1), Direction.EAST), ((4, 1), Direction.WEST), 3)
        self.big.add_path(((3, 2), Direction.EAST), ((4, 1), Direction.NORTH), 2)
        self.big.add_path(((3, 2), Direction.NORTH), ((3, 3), Direction.SOUTH), 2)
        self.big.add_path(((3, 3), Direction.EAST), ((4, 1), Direction.EAST), 1)
        self.big.add_path(((4, 1), Direction.SOUTH), ((4, -1), Direction.NORTH), 1)

        self.empty = Planet()

    def test_integrity(self):
        """
        This test should check that the dictionary returned by "planet.get_paths()" matches the expected structure
        """

        b = self.planet.get_paths()
        self.assertEqual({(0, 0): {Direction.EAST: ((2, 0), Direction.WEST, 2),
                                   Direction.NORTH: ((0, 2), Direction.SOUTH, 1)},
                          (1, 2): {Direction.NORTH: ((1, 2), Direction.WEST, 1),
                                   Direction.WEST: ((1, 2), Direction.NORTH, 1)},
                          (2, 0): {Direction.WEST: ((0, 0), Direction.EAST, 2),
                                   Direction.NORTH: ((2, 2), Direction.SOUTH, 2)},
                          (0, 2): {Direction.SOUTH: ((0, 0), Direction.NORTH, 1),
                                   Direction.EAST: ((2, 2), Direction.WEST, 4)},
                          (2, 2): {Direction.WEST: ((0, 2), Direction.EAST, 4),
                                   Direction.SOUTH: ((2, 0), Direction.NORTH, 2)}}, b)

    def test_empty_planet(self):
        """
        This test should check that an empty planet really is empty
        """

        empty_planet = self.empty.planet_dict

        self.assertFalse(empty_planet)

    def test_target(self):
        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Minimum distance is three nodes (two paths in list returned)
        """

        path_1 = self.planet.shortest_path((0, 0), (2, 2))

        self.assertEqual([((0, 0), Direction.EAST), ((2, 0), Direction.NORTH)], path_1)

        path_2 = self.blocked.shortest_path((0, 0), (1, 1))

        self.assertEqual([((0, 0), Direction.SOUTH), ((2, 0), Direction.EAST), ((2, 2), Direction.SOUTH)], path_2)

    def test_target_not_reachable(self):
        """
        This test should check that a target outside the map or at an unexplored node is not reachable
        """
        # (3, 3) is not in the map and is therefore currently unexplored/unreachable.
        c = self.planet.shortest_path((0, 0), (3, 3))

        self.assertIsNone(c)

    def test_same_length(self):
        """
        This test should check that the shortest-path algorithm implemented also can return alternative routes with the
        same cost (weight) to a specific target

        Requirement: Minimum of two paths with same cost exists, only one is returned by the logic implemented
        """

        shortest_same_1 = self.same.shortest_path((0, 0), (2, 2))
        my_list_of_paths_1 = []
        my_list_of_paths_1.append(shortest_same_1)

        self.assertEqual(len(shortest_same_1), 2)
        self.assertEqual(len(my_list_of_paths_1), 1)
        self.assertEqual([((0, 0), Direction.EAST), ((2, 0), Direction.NORTH)], shortest_same_1)

        shortest_same_2 = self.big.shortest_path((0, 0), (4, -1))
        my_list_of_paths_2 = []
        my_list_of_paths_2.append(shortest_same_2)

        self.assertEqual(len(shortest_same_2), 5)
        self.assertEqual(len(my_list_of_paths_2), 1)
        self.assertEqual([((0, 0), Direction.NORTH), ((0, 2), Direction.NORTH),
                          ((2, 2), Direction.EAST), ((3, 1), Direction.EAST), ((4, 1), Direction.SOUTH)], shortest_same_2)

    def test_target_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target nearby

        Result: Target is reachable
        """
        # TODO think more about this unit test
        self.same.shortest_path((0, 0), (2, 2))

    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """

        # (-1, 3) is located in the map but cannot be reached.
        b = self.big.shortest_path((0, 0), (-1, 3))

        # (3, 2) is located in the map but cannot be reached.
        c = self.same.shortest_path((0, 0), (3, 2))

        self.assertIsNone(b)
        self.assertIsNone(c)


if __name__ == "__main__":
    unittest.main()
