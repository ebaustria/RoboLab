#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        example planet:

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

        # set your data structure
        self.planet = Planet()

        # add the paths
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    def test_target_not_reachable_with_loop(self):
        # does the shortest path algorithm loop infinitely?
        # there is no shortest path
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class YourFirstTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # set your data structure
        self.planet = Planet()

        # ADD YOUR PATHS HERE:
        # self.planet.add_path(...)

    def test_integrity(self):
        # were all paths added correctly to the planet
        # check if add_path() works by using get_paths()
        self.fail('implement me!')

    def test_empty_planet(self):
        self.fail('implement me!')

    def test_target_not_reachable(self):
        self.fail('implement me!')

    def test_shortest_path(self):
        # at least 2 possible paths
        self.fail('implement me!')

    def test_same_length(self):
        # at least 2 possible paths with the same weight
        self.fail('implement me!')

    def test_shortest_path_with_loop(self):
        # does the shortest path algorithm loop infinitely?
        # there is a shortest path
        self.fail('implement me!')

    def test_target_not_reachable_with_loop(self):
        # there is no shortest path
        self.fail('implement me!')


if __name__ == "__main__":
    unittest.main()
