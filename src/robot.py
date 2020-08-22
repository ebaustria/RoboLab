from planet import Planet
from communication import Communication
from odometry import Odometry
from motors import Motors
from sensors import ColorSensor, Ultrasonic
import ev3dev.ev3 as ev3


class Robot:

    def __init__(self, mqtt_client, logger):
        self.planet = Planet()
        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        self.odometry = Odometry(self.lm, self.rm)
        self.communication = Communication(mqtt_client, logger, self)
        self.motors = Motors(self)

        # TODO think about whether or not we want to pass the robot to the sensors as a parameter
        # self.cs = ColorSensor()
        # self.us = Ultrasonic()
        self.current_location = None
        self.running = True
        self.explore_mode = True

    def run(self):

        # TODO how do we save/take the planet name as input so we can send it to the mothership?
        # self.communication.send_planet_name(self.planet.planet_name)

        # TODO begin following line until first node is reached
        # TODO if first node reached, call send_ready()

        while self.running:
            # TODO find place to call on_message, figure out what parameters in function call should be
            #self.communication.on_message(client=self.communication.client, data=?, message=?)
            if self.planet.target is None:
                self.explore_mode = True

            if self.explore_mode:
                # TODO what exactly does the robot need to do in explore mode and in what order?
                # Where do variables (like self.planet.target) need to be changed? Where do we need to add a "pass"after
                # changing variables?

                # This should probably happen at the end of the robot's Aufenthalt at a node.
                if self.planet.target is not None:
                    shortest = self.planet.shortest_path(self.current_location, self.planet.target)

                    if not shortest:
                        # TODO send_target_reached
                        self.planet.target = None
                    elif shortest is not None:
                        self.explore_mode = False
                        # TODO do something with the shortest path
            else:
                shortest = self.planet.shortest_path(self.current_location, self.planet.target)

                if shortest is None:
                    self.explore_mode = True
                elif not shortest:
                    # TODO send_target_reached
                    self.planet.target = None
                else:
                    # TODO do something with the shortest path