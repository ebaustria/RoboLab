#!/usr/bin/env python3

import unittest.mock
import paho.mqtt.client as mqtt
import json

from communication import Communication


class TestRoboLabCommunication(unittest.TestCase):
    @unittest.mock.patch('logging.Logger')
    def setUp(self, mock_logger):
        """
        Instantiates the communication class
        """
        client_id = 'brick-117'  # Replace YOURGROUPID with your group ID
        client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                             clean_session=False,  # We want to be remembered
                             protocol=mqtt.MQTTv311  # Define MQTT protocol version
                             )

        # Initialize your data structure here
        self.communication = Communication(client, mock_logger)

        # Syntax check channel
        client.subscribe('comtest/117', qos=1)

        self.ready_cor = {
            "from": "client",
            "type": "ready"
        }


    def __del__(self):
        del self.communication


    def test_message_ready(self):
        message = json.dumps(self.ready_cor)
        self.communication.send_message("comtest/117", message)

        finished = False

        def test(self, client, data, message):
            payload = json.loads(message.payload.decode('utf-8'))
            msg = payload["payload"]["message"]
            if msg != "Correct":
                self.fail("Message was right")
            finished = True

        self.communication.client.on_message = test

        while not finished:
            pass

    def test_message_path(self):
        """
        This test should check the syntax of the message type "path"
        """
        self.fail('implement me!')

    def test_message_path_invalid(self):
        """
        This test should check the syntax of the message type "path" with errors/invalid data
        """
        self.fail('implement me!')

    def test_message_select(self):
        """
        This test should check the syntax of the message type "pathSelect"
        """
        self.fail('implement me!')

    def test_message_complete(self):
        """
        This test should check the syntax of the message type "explorationCompleted" or "targetReached"
        """
        self.fail('implement me!')


if __name__ == "__main__":
    unittest.main()
