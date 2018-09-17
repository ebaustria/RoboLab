#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
from planet import Direction, Planet
from communication import Communication

client = None  # DO NOT EDIT


def run():
    # DO NOT EDIT
    # the deploy script uses this variable to stop the mqtt client after your program stops or crashes.
    # your script isn't able to close the client after crashing.
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER
    print("Hello World!")


# DO NOT EDIT
if __name__ == '__main__':
    run()
