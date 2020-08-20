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

    client_id = 'brick-YOURGROUPID'  # Replace YOURGROUPID with your group ID
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



    #my changes start
    '''cs = ev3.ColorSensor()
    cs.mode = 'RGB-RAW'
    r, g, b = cs.bin_data("hhh")
    brightness = math.sqrt(r ** 2 + g ** 2 + b ** 2)
    # brightness = (r + g + b) / 3
    # print("Brightness: " + str(brightness))
    print("red: " + str(r) + " green: " + str(g) + " blue: " + str(b))'''

    myMotor = Motors()
    myUltrasonic = Ultrasonic()
    myColorSensor = ColorSensor()
    print(myColorSensor.get_node())
    #r, g, b = myColorSensor.get_colors()
    #print("red: " + str(r) + " green: " + str(g) + " blue: " + str(b))
    count = 0 #better solution?
    while myUltrasonic.get_distance() > 25:
        #print(myColorSensor.get_node())
        if myColorSensor.get_node() == "red" and counter == 0:
            counter += 1
            myMotor.stop()
            myMotor.drive_forward(50, 2)
            myMotor.stop()
            #ev3.Sound.speak("Red")
            myMotor.turn_left(20, 6)
            time.sleep(2)

        elif myColorSensor.get_node() == "blue" and counter == 0:
            counter += 1
            myMotor.stop()
            myMotor.drive_forward(50, 2)
            myMotor.stop()
            #ev3.Sound.speak("Blue")
            myMotor.turn_left(20, 6)
            time.sleep(2)

        else:
            myMotor.follow_line(200,1)
            counter = 0

    myMotor.drive_backward(200,5)

    
    #def dif(color, ref_color1, ref_color2): #eventuell lieber Spektren zur Ermittlung von Knoten aufnehmen
    '''    dif_color = 0
        if (color - ref_color1 < 0):
            dif_color += ref_color1 - color
        else:
            dif_color += color - ref_color1
        if (color - ref_color2< 0):
            dif_color += ref_color2 - color
        else:
            dif_color += color - ref_color2
        return dif_color

    cs = ev3.ColorSensor()
    cs.mode = 'RGB-RAW'
    r, g, b = cs.bin_data("hhh")
    print("red: " + str(r) + " green: " + str(g) + " blue: " + str(b))
    dif_red = 0
    dif_blue = dif(b, r , r)
    print(str(dif_blue))

    while dif_red < 200 :
        myMotor.follow_line(200,1)
        r, g, b = cs.bin_data("hhh")
        print("red: " + str(r) + " green: " + str(g) + " blue: " + str(b))
        dif_red = dif(r,g,b)
        print(str(dif_red))
    while dif_blue < 100:
        myMotor.follow_line(200, 1)
        r, g, b = cs.bin_data("hhh")
        print("red: " + str(r) + " green: " + str(g) + " blue: " + str(b))
        dif_blue = dif(b, r, r)
        print(str(dif_blue))
    myMotor.turn_left(200,5)'''
 #red = 168, 178
 #blue




        
    #my changes end


    #print("Hello World!")


# DO NOT EDIT
if __name__ == '__main__':
    run()
