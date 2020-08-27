#!/usr/bin/env python3
import logging
import os
import paho.mqtt.client as mqtt

from robot import Robot
from uuid import uuid4

client = None  # DO NOT EDIT

#test image
from  ev3dev.ev3 import *
from time import sleep
import ev3dev.fonts as fonts


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

    # Setup robot
    #robot = Robot(client, logger)
    # Start and run robot
    #robot.run()


    lcd = Screen()
    lcd.clear()
    lcd.draw.rectangle((45, 70, 55, 90), fill='black')
    lcd.draw.rectangle((55, 40, 65, 50), fill='black')
    lcd.draw.rectangle((55, 60, 65, 110), fill='black')
    lcd.draw.rectangle((65, 50, 75, 70), fill='black')
    lcd.draw.rectangle((65, 80, 115, 100), fill='black')
    lcd.draw.rectangle((65, 110, 85, 120), fill='black')
    lcd.draw.rectangle((75, 60, 105, 80), fill='black')
    lcd.draw.rectangle((95, 110, 115, 120), fill='black')
    lcd.draw.rectangle((105, 50, 115, 70), fill='black')
    lcd.draw.rectangle((115, 40, 125, 50), fill='black')
    lcd.draw.rectangle((115, 40, 125, 50), fill='black')
    lcd.draw.rectangle((115, 60, 125, 110), fill='black')
    lcd.draw.rectangle((125, 70, 135, 90), fill='black')

    lcd.draw.text((20, 5), 'ROBOLAB 2020', font=fonts.ImageFont.truetype("/home/robot/src/Roboto-Regular.ttf", 20))

    while True:
        lcd.draw.rectangle((35,80,45,110), fill='white')
        lcd.draw.rectangle((135, 80, 145, 110), fill='white')

        lcd.draw.rectangle((35,50,45,80), fill='black')
        lcd.draw.rectangle((135,50,145,80), fill='black')



        lcd.update()
        sleep(1)

        lcd.draw.rectangle((35, 50, 45, 80), fill='white')
        lcd.draw.rectangle((135, 50, 145, 80), fill='white')

        lcd.draw.rectangle((35, 80, 45, 110), fill='black')
        lcd.draw.rectangle((135, 80, 145, 110), fill='black')

        lcd.update()
        sleep(1)


    #logo = Image.open('/home/robot/src/accept.bmp')
    #lcd.image.paste(logo, (0, 0))





# DO NOT EDIT
if __name__ == '__main__':
    run()
