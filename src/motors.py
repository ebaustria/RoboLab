import ev3dev.ev3 as ev3
import time
import math

from odometry import Odometry
#from sensors import ColorSensor
#import sensors


class Motors:

    def __init__(self, odometry: Odometry):
        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")

        self.odometry = odometry

    def drive_forward(self, speed: float, duration: float):
        self.rm.reset()
        self.lm.reset()

        self.rm.stop_action = "brake"
        self.lm.stop_action = "brake"

        self.rm.speed_sp = speed
        self.lm.speed_sp = speed

        self.rm.command = "run-forever"
        self.lm.command = "run-forever"

        time.sleep(duration)

        self.rm.stop()
        self.lm.stop()

    def drive_backward(self, speed: float, duration: float):
        self.drive_forward(-speed, duration)

    #in progress (PID-Controller)
    def follow_line(self, duration: float, cs, odometry, ticks_previous_l: int, ticks_previous_r: int):
        r, g, b = cs.get_colors()
        previous_brightness = math.sqrt(r**2 + g**2 + b**2) # for D-Controller
        #previous_error_d = 0
        right_speed = 0
        left_speed = 0

        #duration in 10 intervals separated
        for i in range(0, int(duration*10)):
            r, g, b = cs.get_colors()
            brightness = math.sqrt(r**2 + g**2 + b**2)

            multiplicator_p = 0.4
            multiplicator_d = 0.2

            error_p = brightness - 350
            error_d = brightness - previous_brightness
            #error_d = error_d-previous_error_d
            turn = multiplicator_p*error_p + multiplicator_d*error_d#(change y)/(change x)*error

            #maybe I-Controller instead

            if 150 < brightness <= 450:
                offset = 200
            else:
                offset = 150

            right_speed = offset + turn
            left_speed = offset - turn
            self.rm.speed_sp = right_speed
            self.lm.speed_sp = left_speed
            self.rm.command = "run-forever"
            self.lm.command = "run-forever"

            time.sleep(duration/10)

            previous_brightness = brightness
            #previous_error_d = error_d

            ticks_l, ticks_r = odometry.get_position()
            odometry.add_point(((ticks_l-ticks_previous_l),(ticks_r-ticks_previous_r)))
            ticks_previous_l = ticks_l
            ticks_previous_r = ticks_r

        return ticks_previous_l, ticks_previous_r

    def stop(self):
        self.rm.reset()
        self.lm.reset()
        self.rm.stop()
        self.lm.stop()

    def turn_angle(self, speed: float, angle: float):
        self.rm.position_sp = -angle * 2 #2 for speed = 100 (2.2 calculated and tested?)
        self.lm.position_sp = angle * 2 #for one rotation -> wheels 2.2 rotations
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"

        self.rm.wait_until_not_moving()

    def detect_nodes(self, speed: float, cs):
        self.odometry.reset_position()

        self.rm.position_sp = 360 * 2
        self.lm.position_sp = -360 * 2
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"

        nodes = []
        while self.rm.is_running:
            if cs.get_brightness() < 200:
                nodes.append(self.rm.position / 2)

        return nodes

    def turn_until_path_found(self, speed: float, cs):
        self.odometry.reset_position()

        self.rm.position_sp = 360 * 2
        self.lm.position_sp = -360 * 2
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"

        while self.rm.is_running:
            if cs.get_brightness() < 200:
                self.stop()

    def drive_in_center_of_node(self, speed: float, duration: float):
        self.stop()

        previous_ticks_l, previous_ticks_r = self.odometry.get_position()
        self.drive_forward(speed, duration)

        ticks_l, ticks_r = self.odometry.get_position()
        self.odometry.add_point((ticks_l-previous_ticks_l, ticks_r-previous_ticks_r))

        self.stop()
