import sensors
import ev3dev.ev3 as ev3
import math
import time

from planet import Planet
from communication import Communication
from odometry import Odometry
from motors import Motors
from sensors import ColorSensor, Ultrasonic


class Robot:

    def __init__(self, mqtt_client, logger):
        # Create Planet and planet_name variable
        self.planet = Planet()
        self.planet_name = None

        # Setup Sensors, Motors and Odometry
        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        self.odometry = Odometry(self.lm, self.rm)
        self.motors = Motors(self.odometry)
        self.cs = ColorSensor(self.motors)
        self.us = Ultrasonic()

        # Setup Communication
        self.communication = Communication(mqtt_client, logger, self)

        # Create variable to write to from communication
        self.start_location = None
        self.end_location = None
        self.path_choice = None
        self.running = True

    def run(self):
        counter = 0
        bottle_detected = False
        ticks_previous_l, ticks_previous_r = 0, 0

        # Calibrate colors for better color accuracy
        self.cs.calibrate_colors()

        # Wait until we want to start
        print("Press Button to start")
        sensors.button_pressed()

        # Main robot loop
        while self.running:
            # Test if robot detect an obstacle
            if self.us.get_distance() < 15:
                # Rotate robot to drive back, and save that an obstacle was detected
                self.cs.rotate_to_path(180)
                bottle_detected = True
                # TODO Add sound
                continue

            # Test if robot reached node
            if self.cs.get_node() in ["blue", "red"] and counter == 0:
                counter += 1

                # Drive to center of node to better scanning
                self.motors.drive_in_center_of_node(100, 2)

                # Check if robot reached first node
                if self.planet_name is None:
                    # Tell mothership to send planet information (planet_name and start coordinates)
                    self.communication.send_ready()

                    # Wait until message is received
                    while self.planet_name is None:
                        pass

                    # Reset odometry of last path, not used for first path
                    self.odometry.reset_list()

                    # Current robot orientation
                    forward_dir = self.start_location[1]

                    # End-position and direction of incoming path
                    self.end_location = (self.start_location[0], (forward_dir + 180) % 360)

                    # Save path as blocked for better path calculation
                    self.planet.add_path(self.end_location, self.end_location, -1)
                else:
                    # Calculate postion and direction from odometry
                    x, y, forward_dir = self.odometry.calculate_path(
                        self.start_location[1], bottle_detected, self.start_location[0][0], self.start_location[0][1])

                    # Direction facing back, used for path-message
                    send_dir = (forward_dir + 180) % 360

                    # Send path to mothership get real position and direction
                    self.communication.send_path(self.start_location, ((x, y), send_dir), bottle_detected)

                    # Wait until message is received
                    while self.end_location is None:
                        pass

                # Position of current node
                current_pos = self.end_location[0]
                # Direction of robot
                forward_dir = (self.end_location[1] + 180) % 360

                # Test if robot already scanned node
                if current_pos in self.planet.scanned_nodes:
                    # If scanned, wait if mothership sends information like target and pathUnveiled
                    time.sleep(2)
                else:
                    # Scan node for posible directions
                    possible_dirs = self.cs.analyze(forward_dir)

                    # Save direction into unexlored edges if they aren't in the planet dictionary
                    for d in possible_dirs:
                        if current_pos not in self.planet.planet_dict \
                                or d not in self.planet.planet_dict[current_pos].keys():
                            self.planet.add_unexplored_edge(current_pos, d)

                    # Mark node as scanned
                    self.planet.scanned_nodes.append(current_pos)

                # Test if robot reached the target
                if current_pos == self.planet.target:
                    # Send targetReached to mothership
                    self.communication.send_target_reached("Wir sind die da!")

                    # Wait until confirmation
                    while self.running:
                        pass
                    # TODO Add sound
                    continue

                # Calculate next direction based on planet information and posible directions
                next_dir = self.choose_dir()

                # If no direction is found: Exloration complete
                if next_dir == -1:
                    # Send explorationCompleted to mothership
                    self.communication.send_exploration_completed("Wir haben alles entdeckt!")

                    # Wait until confirmation
                    while self.running:
                        pass
                    # TODO Add sound
                    continue

                # Save new starting postion for next path
                self.start_location = (self.end_location[0], next_dir)

                # Rotate to new path
                self.cs.select_new_path(forward_dir, next_dir)

                # Reset variables
                self.end_location = None
                bottle_detected = False
                self.odometry.reset_position()
            else:
                # Follow line and save last data for next tick
                ticks_previous_l, ticks_previous_r = self.motors.follow_line(0.5, self.cs, ticks_previous_l, ticks_previous_r)
                # new (better solution?) -> multiple times calles -> ticks_previous needed
                counter = 0

    def choose_dir(self):
        # Next direction, -1 = no direction found
        choice = -1

        # Test if target is set
        if self.planet.target is not None:
            # Calculate shortest path to target
            shortest = self.planet.shortest_path(self.end_location[0], self.planet.target)

            # Test if target is reachable
            if shortest is not None:
                # Select first direction to get to target
                choice = shortest[0][1]

        # Test if no direction is set (no target or target not reachable)
        if choice == -1:
            # Nodes which need be explored
            incomplete_nodes = []
            # Shortest distance to unexplored node
            distance = math.inf
            # Nearest node
            nearest = None

            # Collect all node, which have open paths
            for node in self.planet.unexplored_edges.keys():
                incomplete_nodes.append(node)

            # Collect all node, which aren't scanned
            for node in self.planet.get_nodes():
                if node not in self.planet.scanned_nodes:
                    incomplete_nodes.append(node)

            # Test if all nodes are explored
            if len(incomplete_nodes) == 0:
                return -1

            # Calculate nearest open node
            for node in incomplete_nodes:
                cur = self.planet.shortest_distance(self.end_location[0], node)
                if cur < distance:
                    distance = cur
                    nearest = node

            # Test if no open node is reachable (explorationCompleted)
            if distance == math.inf:
                return -1
            # Test if open node is reached, choose first open path
            elif distance == 0:
                choice = self.planet.unexplored_edges[nearest][0]
            # Otherwise drive to open node (select first direction to get to open node)
            else:
                choice = self.planet.shortest_next_dir(self.end_location[0], nearest)

        # Send pathSelect to mothership
        self.communication.send_path_select(((self.end_location[0][0], self.end_location[0][1]), choice))

        # Wait until message receive or 3sec (answer optional)
        start_time = time.time()
        while self.path_choice is None and time.time() - start_time < 3.0:
            pass

        # Test if mothership overwrites direction, use forced direction
        if self.path_choice is not None:
            choice = self.path_choice

        # Reset Variable
        self.path_choice = None

        # TODO Add sound

        return choice
