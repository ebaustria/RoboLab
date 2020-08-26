# !/usr/bin/env python3
import math

from typing import Tuple
from planet import Direction


class Odometry:

    def __init__(self, motor_left, motor_right):
        self.motor_left = motor_left
        self.motor_right = motor_right
        self.tick_list = []

    def reset_list(self):
        self.tick_list = []

    def reset_position(self):
        self.motor_left.command = "reset"
        self.motor_right.command = "reset"

    def get_position(self):
        return self.motor_left.position, self.motor_right.position

    def get_distance(self, ticks_l: float, ticks_r: float):
        diameter_wheel = 5.5

        distance_l = diameter_wheel * math.pi * ticks_l / 360
        distance_r = diameter_wheel * math.pi * ticks_r / 360

        return distance_l, distance_r

    def get_angle_alpha(self, ticks_l: float, ticks_r: float):
        dl, dr = self.get_distance(ticks_l, ticks_r)
        distance_wheels = 12

        return (dr - dl) / distance_wheels

    def get_path_length(self, ticks_l: float, ticks_r: float):  # alpha in arc measure
        alpha = self.get_angle_alpha(ticks_l, ticks_r)
        if alpha == 0:
            a, b = self.get_distance(ticks_l, ticks_r)  # a = b (round)
            return a
        else:
            dl, dr = self.get_distance(ticks_l, ticks_r)
            return (dr + dl) / alpha * math.sin(alpha / 2)

    def get_dif_x(self, gamma_old: float, ticks_l: float, ticks_r: float):  # gamma_old in arc measure
        length = self.get_path_length(ticks_l, ticks_r)
        beta = self.get_angle_alpha(ticks_l, ticks_r) / 2

        return -math.sin(gamma_old + beta) * length

    def get_dif_y(self, gamma_old: float, ticks_l: float, ticks_r: float):  # gamma_old in arc measure
        length = self.get_path_length(ticks_l, ticks_r)
        beta = self.get_angle_alpha(ticks_l, ticks_r) / 2

        return math.cos(gamma_old + beta) * length

    def get_gamma_new(self, gamma_old: float, ticks_l: float, ticks_r: float):  # gamma_old, alpha in arc measure
        alpha = self.get_angle_alpha(ticks_l, ticks_r)

        return gamma_old + alpha  # mod 2 pi?

    def add_point(self, tupel_ticks: Tuple[float, float]):
        self.tick_list.append(tupel_ticks)

    def get_tupel_list(self):
        return self.tick_list

    def calculate_values(self):
        length = 0
        dif_x, dif_y = 0, 0
        gamma, gamma_old = 0, 0

        # test start
        l = self.get_tupel_list()
        for i in range(10, len(l)):
            ticks_l = l[i][0]
            ticks_r = l[i][1]
        # test end

        # for tupel in :
        #    ticks_l = tupel[0]
        #    ticks_r = tupel[1]

            dif_x += self.get_dif_x(gamma_old, ticks_l, ticks_r)
            dif_y += self.get_dif_y(gamma_old, ticks_l, ticks_r)
            gamma = self.get_gamma_new(gamma_old, ticks_l, ticks_r)
            length += self.get_path_length(ticks_l, ticks_r)

            gamma_old = gamma

        return dif_x, dif_y, gamma, length  # length not necessary

    def get_cardinal_point(self, gamma_in_grad: float, old_dir: int):
        cardinal_points = [0, 270, 180, 90]  # NORTH, WEST, SOUTH, EAST

        if abs(gamma_in_grad) > 315 or abs(gamma_in_grad) < 45:
            return old_dir
        elif 45 < abs(gamma_in_grad) < 135:
            if gamma_in_grad < 0:
                return cardinal_points[(cardinal_points.index(old_dir) - 1) % 4]
            else:
                return cardinal_points[(cardinal_points.index(old_dir) + 1) % 4]
        elif 135 < abs(gamma_in_grad) < 225:
            return cardinal_points[(cardinal_points.index(old_dir) + 2) % 4]
        elif 225 < abs(gamma_in_grad) < 315:
            if gamma_in_grad < 0:
                return cardinal_points[(cardinal_points.index(old_dir) + 1) % 4]
            else:
                return cardinal_points[(cardinal_points.index(old_dir) - 1) % 4]

    def calculate_path(self, old_dir: int, bottle_detected: bool, x: int, y: int):
        if bottle_detected:
            self.reset_list()
            return x, y, (old_dir + 180) % 360

        dif_x, dif_y, gamma, length = self.calculate_values()
        gamma_in_grad = gamma * 360 / (2 * math.pi)
        self.reset_list()

        dir = self.get_cardinal_point(gamma_in_grad, old_dir)

        unit = 45
        if old_dir == Direction.NORTH:
            x += round(dif_x / unit)
            y += round(dif_y / unit)
        elif old_dir == Direction.SOUTH:
            x -= round(dif_x / unit)
            y -= round(dif_y / unit)
        elif old_dir == Direction.WEST:
            x -= round(dif_y / unit)
            y += round(dif_x / unit)
        elif old_dir == Direction.EAST:
            x += round(dif_y / unit)
            y -= round(dif_x / unit)

        return x, y, dir
