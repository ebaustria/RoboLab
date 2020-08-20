import ev3dev.ev3 as ev3
class Ultrasonic:
    def __init__(self):
        self.us = ev3.UltrasonicSensor()

    def get_distance(self):
        self.us.mode = 'US-DIST-CM'
        distance = self.us.distance_centimeters
        #print(distance)
        return distance


class ColorSensor:
    def __init__(self):
        self.cs = ev3.ColorSensor()
        self.cs.mode = 'RGB-RAW'
    def get_brightness(self):
        r, g, b = self.cs.bin_data("hhh")
        brightness = math.sqrt(r ** 2 + g ** 2 + b ** 2)
        return brightness
    def get_node(self):
        r, g, b = self.cs.bin_data("hhh")
        if (r >= 30 and r <= 60) and (g >= 150 and g <= 200) and (b >= 130 and b <= 150):
            return "blue"
        elif (r >= 140 and r <= 170) and (g >= 60 and g <= 80) and (b >= 20 and b <= 40):
            return "red"
        else:
            return "track"
    def get_colors(self):
        r, g, b = self.cs.bin_data("hhh")
        return r, g, b