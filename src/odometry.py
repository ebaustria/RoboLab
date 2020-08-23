# !/usr/bin/env python3
import math

class Odometry:
    def __init__(self, motor_left, motor_right):
        self.motor_left = motor_left
        self.motor_right = motor_right
        self.tick_list = []

        # YOUR CODE FOLLOWS (remove pass, please!)

    def reset_list(self):
        self.tick_list = []

    def reset_position(self):
        self.motor_left.command = "reset"
        self.motor_right.command = "reset"

    def get_position(self):
        return self.motor_left.position, self.motor_right.position

    def get_distance(self, ticks_l, ticks_r):
        diameter_wheel = 5.5
        distance_l = diameter_wheel*math.pi*ticks_l/360
        distance_r = diameter_wheel*math.pi*ticks_r/360
        return distance_l, distance_r

    def get_angle_alpha(self, ticks_l, ticks_r):
        dl, dr = self.get_distance(ticks_l, ticks_r)
        distance_wheels = 12
        return (dr-dl)/distance_wheels

    def get_path_length(self, ticks_l, ticks_r):#alpha in arc measure
        alpha = self.get_angle_alpha(ticks_l, ticks_r)
        if alpha == 0:
            a, b = self.get_distance(ticks_l, ticks_r) #a = b (round)
            return a
        else:
            dl, dr = self.get_distance(ticks_l, ticks_r)
            return (dr + dl)/alpha*math.sin(alpha/2)

    def get_dif_x(self, gamma_old, ticks_l, ticks_r):#gamma_old in arc measure
        length = self.get_path_length(ticks_l, ticks_r)
        beta = self.get_angle_alpha(ticks_l, ticks_r)/2
        return -math.sin(gamma_old + beta) * length

    def get_dif_y(self, gamma_old, ticks_l, ticks_r):#gamma_old in arc measure
        length = self.get_path_length(ticks_l, ticks_r)
        beta = self.get_angle_alpha(ticks_l, ticks_r) / 2
        return math.cos(gamma_old + beta) * length

    def get_gamma_new(self, gamma_old, ticks_l, ticks_r):#gamma_old, alpha in arc measure
        alpha = self.get_angle_alpha(ticks_l, ticks_r)
        return gamma_old + alpha

    def add_point(self, tupel_ticks):
        self.tick_list.append(tupel_ticks)

    def get_tupel_list(self):
        return self.tick_list

    def calculate_values(self, gamma_old):
        length = 0
        dif_x = 0
        dif_y = 0
        gamma = 0

        for tupel in self.get_tupel_list():
            ticks_l = tupel[0]
            ticks_r = tupel[1]

            dif_x += self.get_dif_x(gamma_old, ticks_l, ticks_r)
            dif_y += self.get_dif_y(gamma_old, ticks_l, ticks_r)
            gamma = self.get_gamma_new(gamma_old, ticks_l, ticks_r)
            length += self.get_path_length(ticks_l, ticks_r)

            gamma_old = gamma

        return dif_x, dif_y, gamma, length #length not necessary

    def get_cardinal_point(self, gamma_in_grad, old_cardinal_point):
        cardinal_points = ["NORTH", "WEST", "SOUTH", "EAST"] #enum in planet.py
        if abs(gamma_in_grad) > 315 or abs(gamma_in_grad) < 45:
            return old_cardinal_point
        elif 45 < abs(gamma_in_grad) < 135:
            if gamma_in_grad < 0:
                return cardinal_points[(cardinal_points.index(old_cardinal_point)-1)%4]
            else:
                return cardinal_points[(cardinal_points.index(old_cardinal_point)+1)%4]
        elif 135 < abs(gamma_in_grad) < 225:
            return cardinal_points[cardinal_points.index(old_cardinal_point)+2]
        elif 225 < abs(gamma_in_grad) < 315:
            if gamma_in_grad < 0:
                return cardinal_points[cardinal_points.index(old_cardinal_point)+1]
            else:
                return cardinal_points[cardinal_points.index(old_cardinal_point)-1]

