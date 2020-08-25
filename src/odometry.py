# !/usr/bin/env python3
import math
from planet import Direction


class Odometry:

    #done
    def __init__(self, motor_left, motor_right):
        self.motor_left = motor_left
        self.motor_right = motor_right
        self.tick_list = []

    #done
    def reset_list(self):
        self.tick_list = []

    #done
    def reset_position(self):
        self.motor_left.command = "reset"
        self.motor_right.command = "reset"

    #done
    def get_position(self):
        return self.motor_left.position, self.motor_right.position

    #done (diameter_wheel right value?)
    def get_distance(self, ticks_l, ticks_r):
        diameter_wheel = 5.5
        distance_l = diameter_wheel*math.pi*ticks_l/360
        distance_r = diameter_wheel*math.pi*ticks_r/360
        return distance_l, distance_r

    #done (distance_wheels right value?)
    def get_angle_alpha(self, ticks_l, ticks_r):
        dl, dr = self.get_distance(ticks_l, ticks_r)
        distance_wheels = 12
        return (dr-dl)/distance_wheels

    #done
    def get_path_length(self, ticks_l, ticks_r):#alpha in arc measure
        alpha = self.get_angle_alpha(ticks_l, ticks_r)
        if alpha == 0:
            a, b = self.get_distance(ticks_l, ticks_r) #a = b (round)
            return a
        else:
            dl, dr = self.get_distance(ticks_l, ticks_r)
            return (dr + dl)/alpha*math.sin(alpha/2)

    #done
    def get_dif_x(self, gamma_old, ticks_l, ticks_r):#gamma_old in arc measure
        length = self.get_path_length(ticks_l, ticks_r)
        beta = self.get_angle_alpha(ticks_l, ticks_r)/2
        return -math.sin(gamma_old + beta) * length

    #done
    def get_dif_y(self, gamma_old, ticks_l, ticks_r):#gamma_old in arc measure
        length = self.get_path_length(ticks_l, ticks_r)
        beta = self.get_angle_alpha(ticks_l, ticks_r) / 2
        return math.cos(gamma_old + beta) * length

    #done (mod 2 pi?)
    def get_gamma_new(self, gamma_old, ticks_l, ticks_r):#gamma_old, alpha in arc measure
        alpha = self.get_angle_alpha(ticks_l, ticks_r)
        return gamma_old + alpha #mod 2 pi?

    #done
    def add_point(self, tupel_ticks):
        self.tick_list.append(tupel_ticks)

    #done
    def get_tupel_list(self):
        return self.tick_list

    #done (return length not necessary)
    def calculate_values(self):
        length = 0
        dif_x = 0
        dif_y = 0
        gamma = 0
        gamma_old = 0

        #test start
        l = self.get_tupel_list()
        for i in range(10, len(l)):
            ticks_l = l[i][0]
            ticks_r = l[i][1]
        #test end

        #for tupel in :
        #    ticks_l = tupel[0]
        #    ticks_r = tupel[1]

            dif_x += self.get_dif_x(gamma_old, ticks_l, ticks_r)
            dif_y += self.get_dif_y(gamma_old, ticks_l, ticks_r)
            gamma = self.get_gamma_new(gamma_old, ticks_l, ticks_r)
            length += self.get_path_length(ticks_l, ticks_r)

            gamma_old = gamma

        return dif_x, dif_y, gamma, length #length not necessary

    #in progress (replace cardinal_points with enum, does modulo work?)
    def get_cardinal_point(self, gamma_in_grad, old_dir):
        cardinal_points = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST] #enum in planet.py
        if abs(gamma_in_grad) > 315 or abs(gamma_in_grad) < 45:
            return old_dir
        elif 45 < abs(gamma_in_grad) < 135:
            if gamma_in_grad < 0:
                return cardinal_points[(cardinal_points.index(old_dir)-1)%4]
            else:
                return cardinal_points[(cardinal_points.index(old_dir)+1)%4]
        elif 135 < abs(gamma_in_grad) < 225:
            return cardinal_points[(cardinal_points.index(old_dir)+2)%4]
        elif 225 < abs(gamma_in_grad) < 315:
            if gamma_in_grad < 0:
                return cardinal_points[(cardinal_points.index(old_dir)+1)%4]
            else:
                return cardinal_points[(cardinal_points.index(old_dir)-1)%4]

    def calculate_path(self, old_dir, bottle_detected, x, y):
        if bottle_detected:
            self.reset_list()
            # print("Bottle on path")
            return x, y, (old_dir+180)%360

        dif_x, dif_y, gamma, length = self.calculate_values()#length not needed
        gamma_in_grad = gamma * 360 / (2 * math.pi)

        # print("Length of List: " + str(len(self.get_tupel_list())))

        # print("New gamma: " + str(gamma_in_grad))  # remove prints
        # print("Path length: " + str(length))
        # print("Moved in x-direction: " + str(dif_x))
        # print("Moved in y-direction: " + str(dif_y))

        self.reset_list()

        dir = self.get_cardinal_point(gamma_in_grad, old_dir)

        unit = 45

        if old_dir == Direction.NORTH:#50 as variable
            x += round(dif_x / unit)  # check
            y += round(dif_y / unit)  # check
        elif old_dir == Direction.SOUTH:
            x -= round(dif_x / unit)  # check
            y -= round(dif_y / unit)  # check
        elif old_dir == Direction.WEST:
            x -= round(dif_y / unit)  # check
            y += round(dif_x / unit)  # check
        elif old_dir == Direction.EAST:
            x += round(dif_y / unit)  # check
            y -= round(dif_x / unit)  # check


        # print("X-Koordinate: " + str(x) + " Y-Koordinate: " + str(y))
        # print("Blickrichtung: " + str(dir))

        return x, y, dir

