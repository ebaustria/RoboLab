#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import platform
import ssl
from time import time
from typing import Tuple

from planet import Path, Direction

# Fix: SSL certificate problem on macOS
if all(platform.mac_ver()):
    from OpenSSL import SSL


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    def __init__(self, mqtt_client, logger, robot=None):
        """
        Initializes communication module, connect to server, subscribe, etc.
        :param mqtt_client: paho.mqtt.client.Client
        :param logger: logging.Logger
        """
        # DO NOT CHANGE THE SETUP HERE
        self.client = mqtt_client
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.on_message = self.safe_on_message_handler
        # Add your client setup here

        self.robot = robot

        self.client.username_pw_set('117', password='0QOfuyjhr0')  # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)

        # Main channel
        self.client.subscribe('explorer/117', qos=1)

        self.logger = logger

        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    # DO NOT EDIT THE METHOD SIGNATURE
    def on_message(self, client, data, message):
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))
        self.logger.debug(json.dumps(payload, indent=2))

        # YOUR CODE FOLLOWS

        # Ignore messages from client
        if payload["from"] == "client":
            return

        print("<<< " + message.payload.decode('utf-8'))

        # Get type of payload
        payload_type = payload["type"]

        # debug/error messages e.g. testplanet-Message
        if payload_type in ["notice", "error", "adjust"]:
            """
            Contains some helpful information
            {
                "from": "debug",
                "type": "notice",
                "payload": {
                    "message": "active planet: <PLANET_NAME>"
                }
            }
            """

            # Read and print message
            #msg = payload["payload"]["message"]
            #self.logger.debug(msg)
        # ready-Message
        elif payload_type == "planet":
            """
            Contains information about the planet name
            and the start position and orientation
            {
                "from": "server",
                "type": "planet",
                "payload": {
                    "planetName": "<PLANET_NAME>",
                    "startX": <X>,
                    "startY": <Y>,
                    "startOrientation": <O>
                }
            }
            """

            # Read information from payload

            start_x = payload["payload"]["startX"]
            start_y = payload["payload"]["startY"]
            start_dir = payload["payload"]["startOrientation"]

            self.robot.start_location = ((start_x, start_y), start_dir)
            self.robot.planet_name = payload["payload"]["planetName"]

            # Subscribe to planet channel
            self.client.subscribe('planet/%s/117' % self.robot.planet_name, qos=1)
        # path-Message
        elif payload_type == "path":
            """
            Contains information about the last taken path,
            its weight and some corrected positions
            start = end and weight = -1 if blocked
            {
                "from": "server",
                "type": "path",
                "payload": {
                    "startX": <Xs>,
                    "startY": <Ys>,
                    "startDirection": <Ds>,
                    "endX": <Xc>,
                    "endY": <Yc>,
                    "endDirection": <Dc>,
                    "pathStatus": "free|blocked",
                    "pathWeight": <weight>
                }
            }
            """

            start_x = payload["payload"]["startX"]
            start_y = payload["payload"]["startY"]
            start_dir = payload["payload"]["startDirection"]
            end_x = payload["payload"]["endX"]
            end_y = payload["payload"]["endY"]
            end_dir = payload["payload"]["endDirection"]
            blocked = payload["payload"]["pathStatus"] == "blocked"
            weight = payload["payload"]["pathWeight"]

            start = ((start_x, start_y), start_dir)
            end = ((end_x, end_y), end_dir)

            if blocked:
                weight = -1

            self.robot.planet.add_path(start, end, weight)
            self.robot.end_location = end

            pass
        # pathSelect-Message
        elif payload_type == "pathSelect":
            """
            Contains information about the real orientation
            {
                "from": "server",
                "type": "pathSelect",
                "payload": {
                    "startDirection": <Dc>
                }
            }
            """

            self.robot.path_choice = payload["payload"]["startDirection"]

            pass
        # pathUnveiled-Message
        elif payload_type == "pathUnveiled":
            """
            Contains information about a path which the roboter
            doesn't need to explore anymore
            {
                "from": "server",
                "type": "pathUnveiled",
                "payload": {
                    "startX": <Xs>,
                    "startY": <Ys>,
                    "startDirection": <Ds>,
                    "endX": <Xe>,
                    "endY": <Ye>,
                    "endDirection": <De>,
                    "pathStatus": "free|blocked",
                    "pathWeight": <weight>
                }
            }
            """

            start_x = payload["payload"]["startX"]
            start_y = payload["payload"]["startY"]
            start_dir = payload["payload"]["startDirection"]
            end_x = payload["payload"]["endX"]
            end_y = payload["payload"]["endY"]
            end_dir = payload["payload"]["endDirection"]
            blocked = payload["payload"]["pathStatus"] == "blocked"
            weight = payload["payload"]["pathWeight"]

            start = ((start_x, start_y), start_dir)
            end = ((end_x, end_y), end_dir)

            if blocked:
                weight = -1

            self.robot.planet.add_path(start, end, weight)

            pass
        # target-Message
        elif payload_type == "target":
            """
            Contains information about the planet target
            {
                "from": "server",
                "type": "target",
                "payload": {
                    "targetX": <Xt>,
                    "targetY": <Yt>
                }
            }
            """

            target_x = payload["payload"]["targetX"]
            target_y = payload["payload"]["targetY"]
            
            target = (target_x, target_y)
            
            self.robot.planet.target = target

            pass
        # done-Message
        elif payload_type == "done":
            """
            Received if roboter finished the planet
            {
                "from": "server",
                "type": "done",
                "payload": {
                    "message": "<TEXT>"
                }
            }
            """

            msg = payload["payload"]["message"]
            self.logger.debug(msg)

            self.robot.running = False
            pass
        else:
            raise Exception("Invalid Messagetype")

        self.robot.last_packet = time()

    def send_planet_name(self, name: str):
        """
        Sends to the mothership the testplanet-Message

        publish to explorer/117
        {
            "from": "client",
            "type": "testplanet",
            "payload": {
                "planetName": "<PLANET_NAME>"
            }
        }
        """

        payload = {
            "from": "client",
            "type": "testplanet",
            "payload": {
                "planetName": name
            }
        }

        self.send_message("explorer/117", payload)

    def send_ready(self):
        """
        Sends to the mothership the ready-Message

        publish to explorer/117
        {
            "from": "client",
            "type": "ready"
        }
        """

        payload = {
            "from": "client",
            "type": "ready"
        }

        self.send_message("explorer/117", payload)

    def send_path(self, start: Tuple[Tuple[int, int], Direction], end: Tuple[Tuple[int, int], Direction], blocked: bool):
        """
        Sends to the mothership the path-Message 
        with the information about the path and
        if it's blocked (start and end positions are the same)

        publish to planet/<PLANET>/117
        {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": <Xs>,
                "startY": <Ys>,
                "startDirection": <Ds>,
                "endX": <Xe>,
                "endY": <Ye>,
                "endDirection": <De>,
                "pathStatus": "free|blocked"
            }
        }
        """

        path_status = "blocked" if blocked else "free"

        payload = {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": start[0][0],
                "startY": start[0][1],
                "startDirection": start[1],
                "endX": end[0][0],
                "endY": end[0][1],
                "endDirection": end[1],
                "pathStatus": path_status
            }
        }

        self.send_message("planet/%s/117" % self.robot.planet_name, payload)
        
    def send_path_select(self, choice: object) -> object:
        """
        Sends to the mothership the pathSelect-Message 
        with the information about which path roboter will take
        
        publish to planet/<PLANET>/117
        {
            "from": "client",
            "type": "pathSelect",
            "payload": {
                "startX": <Xs>,
                "startY": <Ys>,
                "startDirection": <Ds>
            }
        }
        """

        payload = {
            "from": "client",
            "type": "pathSelect",
            "payload": {
                "startX": choice[0][0],
                "startY": choice[0][1],
                "startDirection": choice[1]
            }
        }

        self.send_message("planet/%s/117" % self.robot.planet_name, payload)
        
    def send_target_reached(self, msg: str):
        """
        Sends to the mothership the targetReached-Message 
        Used when target is reached

        publish to planet/<PLANET>/117
        {
            "from": "client",
            "type": "targetReached",
            "payload": {
                "message": "<TEXT>"
            }
        }
        """

        payload = {
            "from": "client",
            "type": "targetReached",
            "payload": {
                "message": msg
            }
        }

        self.send_message("planet/%s/117" % self.robot.planet_name, payload)
        
    def send_exploration_completed(self, msg: str):
        """
        Sends to the mothership the explorationCompleted-Message 
        Used when planet is completely explored

        publish to planet/<PLANET>/117
        {
            "from": "client",
            "type": "explorationCompleted",
            "payload": {
                "message": "<TEXT>"
            }
        }
        """
        
        payload = {
            "from": "client",
            "type": "explorationCompleted",
            "payload": {
                "message": msg
            }
        }

        self.send_message("planet/%s/117" % self.robot.planet_name, payload)

    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.
    def send_message(self, topic, message):
        """
        Sends given message to specified channel
        :param topic: String
        :param message: Object
        :return: void
        """
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))

        # YOUR CODE FOLLOWS
        print(">>> " + json.dumps(message))
        self.client.publish(topic, payload=json.dumps(message), qos=1)

    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"
    def safe_on_message_handler(self, client, data, message):
        """
        Handle exceptions thrown by the paho library
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise
