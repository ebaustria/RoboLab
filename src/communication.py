#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import platform
import ssl

from planet import Path, Planet

# Fix: SSL certificate problem on macOS
if all(platform.mac_ver()):
    from OpenSSL import SSL


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    def __init__(self, mqtt_client, logger):
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

        self.client.username_pw_set('117', password='0QOfuyjhr0') # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)

        # TODO Add subscriber
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

        # YOUR CODE FOLLOWS (remove pass, please!)

        payload_type = payload["type"]

        # testplanet-Message
        if payload_type == "notice":
            pass
        # ready-Message
        elif payload_type == "planet":
            pass
        # pat-Message
        elif payload_type == "path":
            pass
        # pathSelect-Message
        elif payload_type == "pathSelect":
            pass
        # pathUnveiled-Message
        elif payload_type == "pathUnveiled":
            pass
        # target-Message
        elif payload_type == "target":
            pass
        # done-Message
        elif payload_type == "done":
            pass
        else:
            raise ReferenceError()


    def send_planet_name(self, name: str):
        """
        Sends to the mothership the testplanet-Message
        :param name: String

        publish to explorer/117
        {
            "from": "client",
            "type": "testplanet",
            "payload": {
                "planetName": "<PLANET_NAME>"
            }
        }
        """
        pass


    def register_planet(self, name: str):
        """
        
        :param name: String
        """
        pass


    def send_ready(self):
        """
        Sends to the mothership the ready-Message

        publish to explorer/117
        {
            "from": "client",
            "type": "ready"
        }
        """
        pass


    def send_path(self, path: Path, blocked: bool):
        pass
        

    

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

        # YOUR CODE FOLLOWS (remove pass, please!)
        pass

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
