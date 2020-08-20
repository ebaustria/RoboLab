from planet import Planet
from communication import Communication
from odometry import Odometry
from barrier import Ultrasound


class Robot:

    def __init__(self, planet: Planet, communication: Communication, odometry: Odometry, ultrasound: Ultrasound):
        self.planet = planet
        self.communication = communication
        self.odometry = odometry
        self.ultrasound = ultrasound
