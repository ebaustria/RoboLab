import ev3dev.ev3 as ev3
import math
import time

from motors import Motors


class Ultrasonic:

    def __init__(self):
        self.us = ev3.UltrasonicSensor()

    def get_distance(self):
        self.us.mode = 'US-DIST-CM'
        distance = self.us.distance_centimeters
        return distance


class ColorSensor:

    def __init__(self, motors: Motors):
        self.cs = ev3.ColorSensor()
        self.cs.mode = 'RGB-RAW'
        self.red = None
        self.blue = None
        self.motors = motors

    def get_brightness(self):
        r, g, b = self.cs.bin_data("hhh")
        brightness = math.sqrt(r ** 2 + g ** 2 + b ** 2)

        return brightness

    def get_node(self):
        interval = 30

        r, g, b = self.cs.bin_data("hhh")
        if abs(r - self.red[0]) < interval and abs(g - self.red[1]) < interval and abs(b - self.red[2]) < interval:
            return "red"
        elif abs(r - self.blue[0]) < interval and abs(g - self.blue[1]) < interval and abs(b - self.blue[2]) < interval:
            return "blue"
        else:
            return "track"

    def get_colors(self):
        return self.cs.bin_data("hhh")

    def get_neighbour_nodes(self):
        nodes = self.motors.detect_nodes(100, self)

        angles = []
        for node in nodes:
            if node >= 315 or node < 45:
                if 0 not in angles:
                    angles.append(0)
            elif 45 <= node < 135:
                if 270 not in angles:
                    angles.append(270)
            elif 135 <= node < 225:
                if 180 not in angles:
                    angles.append(180)
            elif 225 <= node < 315:
                if 90 not in angles:
                    angles.append(90)

        return angles

    def calibrate_colors(self):
        self.red = self.initialize_color("RED")
        self.blue = self.initialize_color("BLUE")

    def initialize_color(self, color: str):
        print("» Press Button to initialize: %s" % color)
        button_pressed()

        r, g, b = self.cs.bin_data("hhh")
        print("Red: {0}, Green: {1}, Blue: {2}".format(r, g, b))

        return r, g, b

    def rotate_to_path(self, angle: int):
        self.motors.turn_angle(100, angle + 40)
        brightness = self.get_brightness()

        while brightness > 200:
            self.motors.turn_until_path_found(100, self)
            brightness = self.get_brightness()

        self.motors.stop()

    def analyze(self, old_dir: int):
        angles = self.get_neighbour_nodes()
        dirs = []

        for angle in angles:
           dirs.append((angle + old_dir) % 360)

        return dirs

    def select_new_path(self, old_dir: int, new_dir: int):
        angle = new_dir - old_dir

        self.rotate_to_path(angle)


def button_pressed():
    btn = ev3.Button()
    time.sleep(1)

    while not btn.any():
        pass
