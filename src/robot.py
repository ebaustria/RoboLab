from planet import Planet
from communication import Communication
from odometry import Odometry
from motors import Motors
from sensors import ColorSensor, Ultrasonic
import ev3dev.ev3 as ev3


class Robot:

    def __init__(self, mqtt_client, logger):
        self.planet = Planet()
        self.planet_name = None

        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        self.odometry = Odometry(self.lm, self.rm)
        self.communication = Communication(mqtt_client, logger, self)
        self.motors = Motors(self)

        self.bottle_detected = False
        self.counter = 0
        self.last_packet = 0

        # TODO think about whether or not we want to pass the robot to the sensors as a parameter
        self.cs = ColorSensor()
        self.us = Ultrasonic()
        self.start_location = None
        self.running = True
        self.explore_mode = True

    def run(self):
        # TODO init and start robot

        while self.running:
            # TODO begin following line until first node is reached, send and receive data

            if self.planet.target is None:
                self.explore_mode = True

            # TODO Calc Path, check if target reached, scan, select new path

            if self.explore_mode:
                # TODO what exactly does the robot need to do in explore mode and in what order?
                # Where do variables (like self.planet.target) need to be changed? Where do we need to add a "pass"after
                # changing variables?

                # This should probably happen at the end of the robot's Aufenthalt at a node.
                if self.planet.target is not None:
                    # TODO Change location to end location
                    shortest = self.planet.shortest_path(self.start_location, self.planet.target)

                    if not shortest:
                        # TODO send_target_reached
                        self.planet.target = None
                    elif shortest is not None:
                        self.explore_mode = False
                        # TODO do something with the shortest path
            else:
                # TODO Change location to end location
                shortest = self.planet.shortest_path(self.start_location, self.planet.target)

                if shortest is None:
                    self.explore_mode = True
                elif not shortest:
                    # TODO send_target_reached
                    self.planet.target = None
                else:
                    # TODO do something with the shortest path
                    pass
