import ev3dev as ev3
import ev3dev.core


class Ultrasound:

    def __init__(self, us):
        self.us = us #ev3.UltrasonicSensor()
        us.mode = 'US-DIST-CM'

    def check_for_barrier(self):
        if self.us.distance_centimeters < 30:
            print(self.us.distance_centimeters)
            ev3dev.core.Sound.speak('Barrier').wait()
