#!/usr/bin/env python3
import logging
import os
import paho.mqtt.client as mqtt

from robot import Robot
from uuid import uuid4
#only for test (26.8)
#from motors import Motors
#from sensors import ColorSensor
#from odometry import Odometry

client = None  # DO NOT EDIT


def run():
    # DO NOT CHANGE THESE VARIABLES
    #
    # The deploy-script uses the variable "client" to stop the mqtt-client after your program stops or crashes.
    # Your script isn't able to close the client after crashing.
    global client

    client_id = str(uuid4())  # Replace YOURGROUPID with your group ID
    client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                         clean_session=True,  # We want a clean session after disconnect or abort/crash
                         protocol=mqtt.MQTTv311  # Define MQTT protocol version
                         )
    log_file = os.path.realpath(__file__) + '/../../logs/project.log'
    logging.basicConfig(filename=log_file,  # Define log file
                        level=logging.DEBUG,  # Define default mode
                        format='%(asctime)s: %(message)s'  # Define default logging format
                        )
    logger = logging.getLogger('RoboLab')

    # THE EXECUTION OF ALL CODE SHALL BE STARTED FROM WITHIN THIS FUNCTION.
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER.

    #nod needed for PID test
    robot = Robot(client, logger)
    robot.run()

    '''motor = Motors()
    cs = ColorSensor(motor)
    cs.calibrate_colors()
    lm, rm = motor.get_motors()
    od = Odometry(lm, rm)

    print("Press Button to start")
    cs.button_pressed()

    ticks_l = 0
    ticks_r = 0
    while True:
        ticks_l, ticks_r = motor.follow_line(0.5, cs, od, ticks_l, ticks_r)
    '''





# DO NOT EDIT
if __name__ == '__main__':
    run()
