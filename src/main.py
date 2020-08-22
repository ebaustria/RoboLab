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


    del com


    #my changes start


    myMotor = Motors()
    myUltrasonic = Ultrasonic()
    myColorSensor = ColorSensor()
    print("Press Button to start")
    myColorSensor.button_pressed()



    rm = ev3.LargeMotor("outB")
    lm = ev3.LargeMotor("outC")
    myOdometry = Odometry(lm, rm)
    myOdometry.reset_position()
    pos_l, pos_r = myOdometry.get_position()
    print("Position 1 rechts: " + str(pos_r))
    print("Position 1 links: " + str(pos_l))
    myMotor.follow_line(1, myColorSensor, myOdometry)
    #myMotor.drive_forward(100,2)
    #myMotor.turn_angle(100, 10, 5)
    #myMotor.drive_forward(100,2) #problem because alpha in that case = 0 -> division zero
    for tupel in myOdometry.get_tupel_list():
        a = tupel[0]
        b = tupel[1]
        print("A: " + str(a) + "    B: " + str(b))
    '''pos_l, pos_r = myOdometry.get_position()
    print("Position 1 rechts: " + str(pos_r))
    print("Position 1 links: " + str(pos_l))
    dl, dr = myOdometry.get_distance(pos_l,pos_r)
    print("Distanz rechts: " + str(dr))
    print("Distanz links; " + str(dl))
    alpha = myOdometry.get_angle_alpha(dl,dr)
    print("Winkel: " + str(alpha*360/(2*math.pi)))
    length = myOdometry.get_path_length(dl, dr, alpha)
    print("Länge: " + str(length))'''


    '''

    counter = 0 #better solution? -> first drive away from node than scan again
    while True:
        while myUltrasonic.get_distance() > 20:
            if myColorSensor.get_node() == "blue" and counter == 0:
                # ev3.Sound.speak("Blue")
                counter += 1
                myMotor.stop()
                myMotor.drive_forward(50, 3)
                myMotor.stop()

                angles = myColorSensor.get_neighbour_nodes()

                i = 0
                for angle in angles:

                    i += 1
                    print(str(i) + ". Knoten am Winkel: " + str(angle))
                    if angle != 10: #only test -> decision for angle later
                        print("Winkel ungleich 10")
                        myMotor.turn_angle(100, angle, 4)
                        time.sleep(1) #necessary?
                        break
                time.sleep(2) #necessary?

            elif myColorSensor.get_node() == "red" and counter == 0:
                #ev3.Sound.speak("Red")
                counter += 1
                myMotor.stop()
                myMotor.drive_forward(50, 3)
                myMotor.stop()

                angles = myColorSensor.get_neighbour_nodes()

                i = 0
                for angle in angles:
                    i += 1
                    print(str(i) + ". Knoten am Winkel: " + str(angle))
                    if angle != 10:
                        print("Winkel ungleich 10")
                        myMotor.turn_angle(100,angle,4)
                        time.sleep(1) #necessary?
                        break
                time.sleep(2)#necessary?

            else:
                myMotor.follow_line(0.5, myColorSensor)
                counter = 0
        myMotor.turn_angle(100,170,4)

    '''
    #my changes end


    #print("Hello World!")


# DO NOT EDIT
if __name__ == '__main__':
    run()
