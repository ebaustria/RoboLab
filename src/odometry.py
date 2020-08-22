# !/usr/bin/env python3
import math

class Odometry:
    def __init__(self, motor_left, motor_right):
        self.motor_left = motor_left
        self.motor_right = motor_right
        self.tick_list = []

        # YOUR CODE FOLLOWS (remove pass, please!)
        pass

    def reset_position(self):
        self.motor_left.command = "reset"
        self.motor_right.command = "reset"

    def get_position(self):
        return self.motor_left.position, self.motor_right.position

    def get_distance(self, ticks_l, tick_r):
        diameter_wheel = 5.5
        distance_l = diameter_wheel*math.pi*ticks_l/360
        distance_r = diameter_wheel*math.pi*tick_r/360
        return distance_l, distance_r

    def get_angle_alpha(self, dl, dr):
        distance_wheels = 12
        return (dr-dl)/distance_wheels

    def get_path_length(self, dl, dr, alpha):#alpha in arc measure
        return (dr + dl)/alpha*math.sin(alpha/2)

    def get_dif_x(self, gamma_old, beta, length):#gamma_old in arc measure
        return -math.sin(gamma_old + beta) * length

    def get_dif_y(self, gamma_old, beta, length):#gamma_old in arc measure
        return math.cos(gamma_old + beta) * length

    def get_gamma_new(self, gamma_old, alpha):#gamma_old, alpha in arc measure
        return gamma_old + alpha

    def add_point(self, tupel_ticks):
        self.tick_list.append(tupel_ticks)

    def get_tupel_list(self):
        return self.tick_list

    def add_movement(self, angle_left, angle_right):
        pass



    def get_direction(self):
        pass

