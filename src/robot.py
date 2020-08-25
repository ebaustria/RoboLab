from planet import Planet
from communication import Communication
from odometry import Odometry
from motors import Motors
from sensors import ColorSensor, Ultrasonic
import ev3dev.ev3 as ev3
import math
import time


class Robot:

    def __init__(self, mqtt_client, logger):
        self.planet = Planet()
        self.planet_name = None

        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        self.odometry = Odometry(self.lm, self.rm)
        self.communication = Communication(mqtt_client, logger, self)
        self.motors = Motors()

        # TODO think about whether or not we want to pass the robot to the sensors as a parameter
        self.cs = ColorSensor(self.motors)
        self.us = Ultrasonic()
        self.start_location = None
        self.end_location = None
        self.path_choice = None
        self.running = True

    def run(self):
        counter = 0
        bottle_detected = False
        ticks_previous_l = 0
        ticks_previous_r = 0

        self.cs.calibrate_colors()

        print("Press Button to start")
        self.cs.button_pressed()

        while self.running:
            if self.us.get_distance() < 15:
                self.cs.rotate_to_path(180)  # turn until next path
                print("Bottle detected")
                bottle_detected = True
                continue

            if (self.cs.get_node() == "blue" or self.cs.get_node() == "red") and counter == 0:
                counter += 1

                self.motors.drive_in_center_of_node(100, 2, self.odometry)  # speed = 50, time = 3 -> change for efficiency

                if self.planet_name is None:
                    self.communication.send_ready()
                    while self.planet_name is None:
                        pass
                    self.odometry.reset_list()
                    # print("Start location: " + str(self.start_location))
                    old_dir = self.start_location[1]
                    edge_dirs = self.cs.analyze(old_dir)

                    current_pos = (self.start_location[0][0], self.start_location[0][1])

                    for d in edge_dirs:
                        if d not in self.planet.planet_dict[current_pos].keys():
                            self.planet.add_unexplored_edge(current_pos, d)
                    self.planet.scanned_nodes.append(current_pos)

                    # print("Dirs: " + str(edge_dirs))
                    # communication and path selection

                    self.end_location = ((self.start_location[0][0], self.start_location[0][1]), (old_dir + 180) % 360)

                    next_dir = self.choose_dir()

                    # print("Old dir: " + str(old_dir))
                    # print("New dir: " + str(next_dir))
                    self.start_location = ((self.start_location[0][0], self.start_location[0][1]), next_dir)
                    # print("End location: " + str(self.start_location))
                    self.cs.select_new_path(old_dir, next_dir)

                else:
                    x, y, old_dir = self.odometry.calculate_path(
                        self.start_location[1], bottle_detected, self.start_location[0][0], self.start_location[0][1])
                    # print("Start location: " + str(self.start_location))

                    send_dir = (old_dir + 180) % 360
                    self.communication.send_path(self.start_location, ((x, y), send_dir), bottle_detected)

                    # print("Old: " + str(((x, y), old_dir)))

                    while self.end_location is None:
                        pass
                    x = self.end_location[0][0]
                    y = self.end_location[0][1]
                    old_dir = (self.end_location[1] + 180) % 360

                    current_pos = (self.end_location[0][0], self.end_location[0][1])

                    if current_pos in self.planet.scanned_nodes:
                        time.sleep(2)
                    else:
                        unexplored_dirs = self.cs.analyze(old_dir)
                        for d in unexplored_dirs:
                            if d not in self.planet.planet_dict[current_pos].keys():
                                self.planet.add_unexplored_edge(current_pos, d)
                        self.planet.scanned_nodes.append(current_pos)

                    if current_pos == self.planet.target:
                        self.communication.send_target_reached("Wir sind die da!")
                        while self.running:
                            pass
                        continue

                    next_dir = self.choose_dir()
                    if next_dir == -1:
                        self.communication.send_exploration_completed("Wir haben alles entdeckt!")
                        while self.running:
                            pass
                        continue

                    # print("Old dir: " + str(old_dir))
                    # print("New dir: " + str(next_dir))
                    self.start_location = ((x, y), next_dir)
                    # print("End location: " + str(self.start_location))
                    self.cs.select_new_path(old_dir, next_dir)
                # print("-------")

                self.end_location = None
                bottle_detected = False
                self.odometry.reset_position()  # new ? necessary
            else:
                ticks_previous_l, ticks_previous_r = self.motors.follow_line(0.5, self.cs, self.odometry, ticks_previous_l, ticks_previous_r)
                #new (better solution?) -> multiple times calles -> ticks_previous needed
                counter = 0
            continue

    def choose_dir(self):
        choice = -1

        if self.planet.target is not None:
            shortest = self.planet.shortest_path(self.end_location[0], self.planet.target)

            if shortest is not None:
                choice = self.planet.shortest_next_dir(self.end_location[0], self.planet.target)

        if choice == -1:
            incomplete_nodes = []
            distance = math.inf
            nearest = None

            for node in self.planet.unexplored_edges.keys():
                incomplete_nodes.append(node)

            for node in self.planet.get_nodes():
                if node not in self.planet.scanned_nodes:
                    incomplete_nodes.append(node)

            if len(incomplete_nodes) == 0:
                return -1

            for node in incomplete_nodes:
                cur = self.planet.shortest_distance(self.end_location[0], node)
                if cur < distance:
                    distance = cur
                    nearest = node

            if distance == 0:
                choice = self.planet.unexplored_edges[nearest][0]
            else:
                choice = self.planet.shortest_next_dir(self.end_location[0], nearest)

        self.communication.send_path_select(((self.end_location[0][0], self.end_location[0][1]), choice))
        is_communication_cycle_over = False
        start_time = time.time()

        while self.path_choice is None and not is_communication_cycle_over:
            if time.time() - start_time >= 3.0:
                is_communication_cycle_over = True

        if self.path_choice is not None:
            choice = self.path_choice
        self.path_choice = None

        return choice



