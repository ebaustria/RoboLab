from planet import Planet
from communication import Communication
from odometry import Odometry


class Robot:

    def __init__(self, planet: Planet, communication: Communication, odometry: Odometry):
        self.planet = planet
        self.communication = communication
        self.odometry = odometry
