import ev3dev.ev3 as ev3
import time
import math

from odometry import Odometry


class Motors:

    def __init__(self, odometry: Odometry):
        # Setup Motors
        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")

        # Setup Odometry
        self.odometry = odometry

    def drive_forward(self, speed: float, duration: float):
        # Reset Motors
        self.rm.reset()
        self.lm.reset()

        # Set stop action
        self.rm.stop_action = "brake"
        self.lm.stop_action = "brake"

        # Set given speed
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed

        # Run until stop command
        self.rm.command = "run-forever"
        self.lm.command = "run-forever"

        # Sleep for a given time while motors running
        time.sleep(duration)

        # Stop Motors
        self.rm.stop()
        self.lm.stop()

    # PID Controller (with P and D component)
    def follow_line(self, cs, ticks_previous_l: int, ticks_previous_r: int, previous_brightness: int):
        # Setup multipliers for Controller
        multiplier_p = 0.4  # 0.4
        multiplier_d = 0.2  # 0.15

        # Get brightness
        r, g, b = cs.get_colors()
        brightness = math.sqrt(r**2 + g**2 + b**2)

        # Calculate Error for P and D component
        error_p = brightness - 350
        error_d = brightness - previous_brightness

        # Calculate turn
        turn = multiplier_p*error_p + multiplier_d*error_d  # (change y)/(change x)*error

        # Slow down if driving in very bright of very dark area (changing offset)
        if 150 < brightness <= 450:
            offset = 200
        else:
            offset = 130  # 150

        # Calculate speed
        right_speed = offset + turn
        left_speed = offset - turn

        # Set speed to Motors
        self.rm.speed_sp = right_speed
        self.lm.speed_sp = left_speed

        # Run until stop command
        self.rm.command = "run-forever"
        self.lm.command = "run-forever"

        # Sleep for a given time while motors running
        time.sleep(0.01)  # duration/10

        # Get absolute driven angles for each Motor in this interval
        ticks_l, ticks_r = self.odometry.get_position()

        # Add relative driven angles to Odometry
        self.odometry.add_point(((ticks_l-ticks_previous_l), (ticks_r-ticks_previous_r)))

        # ticks have to be returned because follow_line is multiple times called
        return ticks_l, ticks_r, brightness

    # Stop Robot
    def stop(self):
        # Reset Motors
        self.rm.reset()
        self.lm.reset()

        # Stop Motors
        self.rm.stop()
        self.lm.stop()

    # Turn the Robot to a given angle with a given speed
    def turn_angle(self, speed: float, angle: float):
        # rotate efficient (angle <= 180)
        if angle > 180:
            angle -= 360
        if angle < -180:
            angle += 360

        # 2 Motor rotations = 1 Robot rotation
        self.rm.position_sp = -angle * 2
        self.lm.position_sp = angle * 2

        # Set given speed
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed

        # Run Motors until angle reached
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"

        self.rm.wait_until_not_moving()

    # Turn the robot while it is scanning for edges and return the motor positions where edges are detected.
    def detect_nodes(self, speed: float, cs):
        # Reset Motor positions to 0
        self.odometry.reset_position()

        # 1 Robot rotation
        self.rm.position_sp = 360 * 2.15  # 360 * 2
        self.lm.position_sp = -360 * 2.15  # -360 * 2

        # Set given speed
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed

        # Run Motors until angle reached
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"

        # Get measured angles (relative to Robot) where edges are detected
        nodes = []
        while self.rm.is_running:
            if cs.get_brightness() < 200:
                nodes.append(self.rm.position / 2.15)  # self.rm.position / 2

        return nodes

    # Turn the robot until it detects the next edge
    def turn_until_path_found(self, speed: float, cs):
        # Reset Motor positions to 0
        self.odometry.reset_position()

        # 1 Robot rotation
        self.rm.position_sp = 360 * 2
        self.lm.position_sp = -360 * 2

        # Set given speed
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed

        # Run Motors until angle reached
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"

        # Turn until it detects the next edge
        while self.rm.is_running:
            if cs.get_brightness() < 200:
                self.stop()

    # Reposition the robot after reaching a node so that all possible edges can be detected by the color sensor.
    def drive_in_center_of_node(self, speed: float, duration: float):
        # Stop Motors
        self.stop()

        # Continue Odometry measurement while driving forward with a given speed and duration
        previous_ticks_l, previous_ticks_r = self.odometry.get_position()
        self.drive_forward(speed, duration)
        ticks_l, ticks_r = self.odometry.get_position()
        self.odometry.add_point((ticks_l - previous_ticks_l, ticks_r - previous_ticks_r))

        # Stop Motors
        self.stop()
