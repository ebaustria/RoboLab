import ev3dev.ev3 as ev3
import math
import time


class Ultrasonic:
    def __init__(self):
        self.us = ev3.UltrasonicSensor()

    #done
    def get_distance(self):
        self.us.mode = 'US-DIST-CM'
        distance = self.us.distance_centimeters
        return distance


class ColorSensor:
    #done
    def __init__(self, motors):
        self.cs = ev3.ColorSensor()
        self.cs.mode = 'RGB-RAW'
        self.red = None
        self.blue = None
        self.motors = motors


    #done
    def get_brightness(self):
        r, g, b = self.cs.bin_data("hhh")
        brightness = math.sqrt(r ** 2 + g ** 2 + b ** 2)
        return brightness

    #done
    def get_node(self):
        interval = 25 #best interval?
        r, g, b = self.cs.bin_data("hhh")
        if abs(r-self.red[0]) < interval and abs(g-self.red[1]) < interval and abs(b-self.red[2]) < interval:
            return "red"
        elif abs(r-self.blue[0]) < interval and abs(g-self.blue[1]) < interval and abs(b-self.blue[2]) < interval:
            return "blue"
        else:
            return "track"

    #done
    def get_colors(self):
        r, g, b = self.cs.bin_data("hhh")
        return r, g, b

    #in progress
    def get_neighbour_nodes(self):
        nodes = []
        angles = [10,10,10,10] #better default values?

        brightness = self.get_brightness()

        angle = 0
        while True:
            if brightness < 200:
                if angle > 315 or angle < 45:
                    if 0 not in angles:
                        angles[0] = 0
                elif angle > 45 and angle < 135:
                    if 90 not in angles:
                        angles[1] = 90
                elif angle > 135 and angle < 225:
                    if 180 not in angles:
                        angles[2] = 180
                elif angle > 225 and angle < 315:
                    if 270 not in angles:
                        angles[3] = 270
                #print("Winkel: " + str(angle))
            if angle >= 370:#360
                break
            brightness = self.get_brightness()
            angle += 5
            self.motors.turn_angle(100, 5, 0.2)#speed = 100, angle = 5, time = 0.2 -> less time?
        return angles

        '''
        for ticks in range(0, 40): #40 ticks (movements)
            brightness = self.get_brightness()
            print("Brightness = " + str(brightness))
            angle = 360*ticks/40
            print("Angle = " + str(angle))
            myMotor.turn_angle(100, (360/40), 0.5) #min value for movement?
            if brightness < 200: #right value?
                nodes.append(angle)


        for node_angle in nodes:
            print(str(node_angle))
            if node_angle > 315 or node_angle < 45:
                if 0 not in angles:
                    angles[0] = 0
            elif node_angle > 45 and node_angle <  135:
                if 90 not in angles:
                    angles[1] = 90
            elif node_angle > 135 and node_angle < 225:
                if 180 not in angles:
                    angles[2] = 180
            elif node_angle > 225 and node_angle < 315:
                if 270 not in angles:
                    angles[3] = 270
        return angles
        '''

    #done
    def initialize_color(self, color):

        print("1. Initialization " +  color)
        self.button_pressed()

        r1,g1,b1 = self.cs.bin_data("hhh")
        print("red: " + str(r1) + " green: " + str(g1) + " blue: " + str(b1))
        return r1, g1, b1

    #done (maybe white and black calibration)
    def calibrate_colors(self):
        self.red = self.initialize_color("RED")
        self.blue = self.initialize_color("BLUE")
        #r3, g3, b3 = self.initialize_color("SCHWARZ")
        #r4, g4, b4 = self.initialize_color("WEIß")

    #done (maybe own class?)
    def button_pressed(self):
        btn = ev3.Button()
        time.sleep(1)
        while not btn.any():
            pass

    #in progress
    def rotate_to_path(self, angle):
        self.motors.turn_angle(100, angle+30, 5)#speed = 100, angle = angle-45, time = 5-> less time?
        brightness = self.get_brightness()

        while brightness > 200:
            self.motors.turn_angle(100, -5, 0.2)#speed = 100, angle = 5, time = 0.2 -> less time?
            brightness = self.get_brightness()

        self.motors.stop()


    def analyze(self, old_dir):
        angles = self.get_neighbour_nodes()
        print("Angles: " + str(angles))
        dirs = []

        for angle in angles:
            if angle != 10:
                dirs.append((angle + old_dir)%360)

        return dirs

        '''for angle in angles:
            print("Winkel: " + str(angle))

        if angles[0] != 10:
            print("g für geradeaus")
        if angles[1] != 10:
            print("l für links")
        if angles[2] != 10:
            print("z für zurück")
        if angles[3] != 10:
            print("r für rechts")'''



    '''def select_new_path(self, gamma_in_grad, old_dir, myOdometry):
        next_direction = input()

        next_angle = 0
        if next_direction is "l":
            next_angle = 90
            gamma_in_grad += 90
        if next_direction is "z":
            next_angle = 180
            gamma_in_grad += 180
        if next_direction is "r":
            next_angle = -90  # 270
            gamma_in_grad -= 90  # +=270

        print("Gamma in grad: " + str(gamma_in_grad))
        dir = myOdometry.get_cardinal_point(gamma_in_grad, old_dir)

        print("Blickrichtung: " + str(dir))

        self.turn_to_angle(next_angle)

        return dir'''

    def select_new_path(self, old_dir, new_dir):
        angle = new_dir - old_dir
        if angle > 180:
            angle -= 360

        print("Angle in select_new_path: " + str(angle))
        self.rotate_to_path(angle)









