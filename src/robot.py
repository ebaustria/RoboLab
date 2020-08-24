from planet import Planet, Direction
from communication import Communication
from odometry import Odometry
from motors import Motors
from sensors import ColorSensor, Ultrasonic
import ev3dev.ev3 as ev3
import math


class Robot:

    def __init__(self, mqtt_client, logger):
        self.planet = Planet()
        self.planet_name = None

        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        self.odometry = Odometry(self.lm, self.rm)
        self.communication = Communication(mqtt_client, logger, self)
        self.motors = Motors()

        self.last_packet = 0

        # TODO think about whether or not we want to pass the robot to the sensors as a parameter
        self.cs = ColorSensor(self.motors)
        self.us = Ultrasonic()
        self.start_location = None
        self.end_location = None
        self.running = True
        self.explore_mode = True

    def run(self):
        counter = 0
        bottle_detected = False


        self.cs.calibrate_colors()

        print("Press Button to start")
        self.cs.button_pressed()


        while self.running:
            # TODO begin following line until first node is reached, send and receive data
            if self.us.get_distance() < 10:
                self.cs.rotate_to_path(180)  # turn until next path
                print("Bottle detected")
                bottle_detected = True
                continue

            if (self.cs.get_node() == "blue" or self.cs.get_node() == "red") and counter == 0:
                counter += 1

                self.motors.drive_in_center_of_node(50, 3)  # speed = 50, time = 3 -> change for efficiency

                if self.planet_name == None:
                    self.communication.send_ready()
                    while self.planet_name == None:
                        pass
                    self.odometry.reset_list()
                    print("Start location: " + str(self.start_location))
                    old_dir = self.start_location[1]
                    dirs = self.cs.analyze(old_dir)
                    print("Dirs: " + str(dirs))
                    # communication and path selection
                    dir = self.choose_dir(old_dir, dirs)
                    print("Old dir: " + str(old_dir))
                    print("New dir: " + str(dir))
                    self.start_location = ((self.start_location[0][0], self.start_location[0][1]), dir)
                    print("End location: " + str(self.start_location))
                    self.cs.select_new_path(old_dir,dir)

                else:
                    x, y, old_dir = self.odometry.calculate_path(
                        self.start_location[1], bottle_detected, self.start_location[0][0], self.start_location[0][1])
                    #not analyze if node known
                    print("Start location: " + str(self.start_location))
                    #communication (path-message)

                    send_dir = (old_dir + 180) % 360
                    self.communication.send_path(self.start_location, ((x,y),send_dir), bottle_detected)

                    print("Old: " +  str(((x, y), old_dir)))

                    while self.end_location == None:
                        pass
                    x = self.end_location[0][0]
                    y = self.end_location[0][1]
                    old_dir = (self.end_location[1] + 180) % 360
                    self.end_location = None

                    dirs = self.cs.analyze(old_dir)
                    print("Dirs: " + str(dirs))
                    # communication and path selection
                    dir = self.choose_dir(old_dir, dirs)
                    print("Old dir: " + str(old_dir))
                    print("New dir: " + str(dir))
                    self.start_location = ((x, y), dir)
                    print("End location: " + str(self.start_location))
                    self.cs.select_new_path(old_dir, dir)

                bottle_detected = False
            else:
                self.motors.follow_line(0.5, self.cs, self.odometry)
                counter = 0
            continue

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
    #TODO
    def choose_dir(self, old_dir, dirs):
        print("Choose dir: ")

        if len(dirs) == 2:
            if dirs[0] == (old_dir + 180) % 360:
                return dirs[1]
            else:
                return dirs[0]

        next_direction = input()

        #test
        if next_direction == "EAST":
            return Direction.EAST
        if next_direction == "SOUTH":
            return Direction.SOUTH
        if next_direction == "WEST":
            return Direction.WEST
        return Direction.NORTH

