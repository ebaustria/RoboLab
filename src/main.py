#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import logging
import os
import paho.mqtt.client as mqtt
import math
import time

from communication import Communication
from odometry import Odometry
from planet import Direction, Planet
from motors import Motors
from sensors import Ultrasonic, ColorSensor

client = None  # DO NOT EDIT


def run():
    # DO NOT CHANGE THESE VARIABLES
    #
    # The deploy-script uses the variable "client" to stop the mqtt-client after your program stops or crashes.
    # Your script isn't able to close the client after crashing.
    global client

    client_id = 'brick-117'  # Replace YOURGROUPID with your group ID
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

    com = Communication(client, logger)

    # my changes start

    myMotor = Motors()
    myUltrasonic = Ultrasonic()
    myColorSensor = ColorSensor()

    print("Press Button to start")

    myColorSensor.button_pressed()
    lm, rm = myMotor.get_motors()
    myOdometry = Odometry(lm, rm)

    # startkoordinaten
    x_coordinate = 0
    y_coordinate = 0
    #cardinal_points = ["NORTH", "EAST", "SOUTH", "WEST"]
    direction = "WEST"  # start direction
    gamma_old = 0 #for all start directions

    counter = 0  # better solution? -> first drive away from node than scan again
    bottle_detected = 0 #better solution? -> x- and y-Koordinates do not change when driving back to node
    while True:
        while myUltrasonic.get_distance() > 10:
            if myColorSensor.get_node() == "blue" and counter == 0:
                # ev3.Sound.speak("Blue")
                counter += 1
                # gamma_old everywhere 0 -> in function call change
                gamma_old, direction, x_coordinate, y_coordinate = \
                    myColorSensor.explore(myMotor, myOdometry, 0, x_coordinate, y_coordinate, bottle_detected, direction)
                bottle_detected = 0
            elif myColorSensor.get_node() == "red" and counter == 0:
                # ev3.Sound.speak("Red")
                counter += 1
                #gamma_old everywhere 0 -> in function call change
                gamma_old, direction, x_coordinate, y_coordinate = \
                    myColorSensor.explore(myMotor, myOdometry, 0, x_coordinate, y_coordinate, bottle_detected,
                                          direction)
                bottle_detected = 0
            else:
                myMotor.follow_line(0.5, myColorSensor, myOdometry)
                counter = 0
        myColorSensor.turn_to_angle(180, myMotor)  # turn until next path
        gamma_old = math.pi
        gamma_in_grad = gamma_old*360/(2*math.pi)
        direction = myOdometry.get_cardinal_point(gamma_in_grad , direction)
        bottle_detected = 1
    # my changes end

    # print("Hello World!")

    del com

# DO NOT EDIT
if __name__ == '__main__':
    run()
