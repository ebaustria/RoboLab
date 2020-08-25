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
                self.cs.rotate_to_path(180)
                # print("Bottle detected")
                bottle_detected = True
                continue

            if (self.cs.get_node() == "blue" or self.cs.get_node() == "red") and counter == 0:
                counter += 1

                self.motors.drive_in_center_of_node(100, 2, self.odometry)

                if self.planet_name is None:
                    self.communication.send_ready()

                    while self.planet_name is None:
                        pass

                    self.odometry.reset_list()
                    forward_dir = self.start_location[1]
                    self.end_location = (self.start_location[0], (forward_dir + 180) % 360)
                    self.planet.add_path(self.end_location, self.end_location, -1)
                else:
                    x, y, forward_dir = self.odometry.calculate_path(
                        self.start_location[1], bottle_detected, self.start_location[0][0], self.start_location[0][1])

                    send_dir = (forward_dir + 180) % 360
                    self.communication.send_path(self.start_location, ((x, y), send_dir), bottle_detected)

                    while self.end_location is None:
                        pass

                current_pos = self.end_location[0]
                forward_dir = (self.end_location[1] + 180) % 360

                if current_pos in self.planet.scanned_nodes:
                    time.sleep(2)
                else:
                    possible_dirs = self.cs.analyze(forward_dir)
                    for d in possible_dirs:
                        if current_pos not in self.planet.planet_dict or d not in self.planet.planet_dict[current_pos].keys():
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

                self.start_location = (self.end_location[0], next_dir)
                self.cs.select_new_path(forward_dir, next_dir)

                self.end_location = None
                bottle_detected = False
                self.odometry.reset_position()  # new ? necessary
            else:
                ticks_previous_l, ticks_previous_r = self.motors.follow_line(0.5, self.cs, self.odometry, ticks_previous_l, ticks_previous_r)
                # new (better solution?) -> multiple times calles -> ticks_previous needed
                counter = 0

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

            print("Unexplored: " + str(self.planet.unexplored_edges))
            for node in self.planet.unexplored_edges.keys():
                incomplete_nodes.append(node)

            print("Nodes: " + str(self.planet.get_nodes()))
            for node in self.planet.get_nodes():
                if node not in self.planet.scanned_nodes:
                    incomplete_nodes.append(node)

            print("Incomplete: " + str(incomplete_nodes))
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
