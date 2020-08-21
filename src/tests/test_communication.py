#!/usr/bin/env python3

import unittest.mock

import paho.mqtt.client as mqtt
import json
import time

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
        self.ready_more = {
            "from": "client",
            "type": "ready",
            "extra": "stuff"
        }
        self.path_cor = {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": 0,
                "startY": 0,
                "startDirection": 0,
                "endX": 1,
                "endY": 1,
                "endDirection": 180,
                "pathStatus": "free"
            }
        }
        self.path_more = {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": 0,
                "startY": 0,
                "startDirection": 0,
                "endX": 1,
                "endY": 1,
                "endDirection": 180,
                "pathStatus": "free"
            },
            "extra": "stuff"
        }
        self.path_miss = {
            "from": "client",
            "type": "path"
        }
        self.path_status = {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": 0,
                "startY": 0,
                "startDirection": 0,
                "endX": 1,
                "endY": 1,
                "endDirection": 180,
                "pathStatus": "plakat"
            }
        }
        self.path_number = {
            "from": "client",
            "type": "path",
            "payload": {
                "startX": "Hey",
                "startY": "Hallo",
                "startDirection": "Guten Tag",
                "endX": 1,
                "endY": 1,
                "endDirection": 180,
                "pathStatus": "free"
            }
        }
        self.select_cor = {
            "from": "client",
            "type": "pathSelect",
            "payload": {
                "startX": 0,
                "startY": 0,
                "startDirection": 0
            }
        }
        self.select_more = {
            "from": "client",
            "type": "pathSelect",
            "payload": {
                "startX": 0,
                "startY": 0,
                "startDirection": 0
            },
            "extra": "stuff"
        }
        self.select_miss = {
            "from": "client",
            "type": "pathSelect"
        }
        self.select_number = {
            "from": "client",
            "type": "pathSelect",
            "payload": {
                "startX": "Heyho",
                "startY": "Moin",
                "startDirection": "Morgen"
            }
        }
        self.reached_cor = {
            "from": "client",
            "type": "targetReached",
            "payload": {
                "message": "Nachricht"
            }
        }
        self.reached_more = {
            "from": "client",
            "type": "targetReached",
            "payload": {
                "message": "Nachricht"
            },
            "extra": "stuff"
        }
        self.reached_miss = {
            "from": "client",
            "type": "targetReached"
        }
        self.reached_number = {
            "from": "client",
            "type": "targetReached",
            "payload": {
                "message": 1
            }
        }
        self.complete_cor = {
            "from": "client",
            "type": "explorationCompleted",
            "payload": {
                "message": "Nachricht"
            }
        }
        self.complete_more = {
            "from": "client",
            "type": "explorationCompleted",
            "payload": {
                "message": "Nachricht"
            },
            "extra": "stuff"
        }
        self.complete_miss = {
            "from": "client",
            "type": "explorationCompleted"
        }
        self.complete_number = {
            "from": "client",
            "type": "explorationCompleted",
            "payload": {
                "message": 1
            }
        }

    def __del__(self):
        del self.communication

    def test_message_ready(self):
        data = {"max": 2, "finished": 0, "failed": []}

        def test(client, _, message):
            payload = json.loads(message.payload.decode('utf-8'))
            print(payload)
            if payload["from"] != "debug":
                return

            msg = payload["payload"]["message"]

            if data["finished"] == 0 and msg != "Correct":
                data["failed"].append("Test 1 should be correct")
            elif data["finished"] == 1 and msg == "Correct":
                data["failed"].append("Test 2 should have to many fields")
            data["finished"] += 1

        # Set message channel listener
        self.communication.client.on_message = test

        # Send correct data
        message = json.dumps(self.ready_cor)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.ready_more)
        self.communication.send_message("comtest/117", message)

        # Wait until everything is received
        while data["finished"] < data["max"]:
            pass

        # Fail test for every test
        for m in data["failed"]:
            self.fail(m)

    def test_message_path(self):
        data = {"max": 3, "finished": 0, "failed": []}

        def test(client, _, message):
            payload = json.loads(message.payload.decode('utf-8'))
            print(payload)
            if payload["from"] != "debug":
                return

            msg = payload["payload"]["message"]

            if data["finished"] == 0 and msg != "Correct":
                data["failed"].append("Test 1 should be correct")
            elif data["finished"] == 1 and msg == "Correct":
                data["failed"].append("Test 2 should have too many fields")
            elif data["finished"] == 2 and msg == "Correct":
                data["failed"].append("Test 3 should have too few fields")
            data["finished"] += 1

        # Set message channel listener
        self.communication.client.on_message = test

        # Send correct data
        message = json.dumps(self.path_cor)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.path_more)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.path_miss)
        self.communication.send_message("comtest/117", message)

        # Wait until everything is received
        while data["finished"] < data["max"]:
            pass

        # Fail test for every test
        for m in data["failed"]:
            self.fail(m)

    def test_message_path_invalid(self):
        data = {"max": 2, "finished": 0, "failed": []}

        def test(client, _, message):
            payload = json.loads(message.payload.decode('utf-8'))
            print(payload)
            if payload["from"] != "debug":
                return

            msg = payload["payload"]["message"]

            if data["finished"] == 0 and msg == "Correct":
                data["failed"].append("Test 1 should have unknown path status")
            elif data["finished"] == 1 and msg == "Correct":
                data["failed"].append("Test 2 should have invalid data types")
            data["finished"] += 1

        # Set message channel listener
        self.communication.client.on_message = test

        # Send invalid data
        message = json.dumps(self.path_status)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.path_number)
        self.communication.send_message("comtest/117", message)

        # Wait until everything is received
        while data["finished"] < data["max"]:
            pass

        # Fail test for every test
        for m in data["failed"]:
            self.fail(m)

    def test_message_select(self):
        data = {"max": 4, "finished": 0, "failed": []}

        def test(client, _, message):
            payload = json.loads(message.payload.decode('utf-8'))
            print(payload)
            if payload["from"] != "debug":
                return

            msg = payload["payload"]["message"]

            if data["finished"] == 0 and msg != "Correct":
                data["failed"].append("Test 1 should be correct")
            elif data["finished"] == 1 and msg == "Correct":
                data["failed"].append("Test 2 should have too many fields")
            elif data["finished"] == 2 and msg == "Correct":
                data["failed"].append("Test 3 should have too few fields")
            elif data["finished"] == 3 and msg == "Correct":
                data["failed"].append("Test 4 should have invalid data types")
            data["finished"] += 1

        # Set message channel listener
        self.communication.client.on_message = test

        # Send correct data
        message = json.dumps(self.select_cor)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.select_more)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.select_miss)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.select_number)
        self.communication.send_message("comtest/117", message)

        # Wait until everything is received
        while data["finished"] < data["max"]:
            pass

        # Fail test for every test
        for m in data["failed"]:
            self.fail(m)

    def test_message_complete(self):
        data = {"max": 8, "finished": 0, "failed": []}

        def test(client, _, message):
            payload = json.loads(message.payload.decode('utf-8'))
            print(payload)
            if payload["from"] != "debug":
                return

            msg = payload["payload"]["message"]

            if data["finished"] == 0 and msg != "Correct":
                data["failed"].append("Test 1 should be correct")
            elif data["finished"] == 1 and msg == "Correct":
                data["failed"].append("Test 2 should have too many fields")
            elif data["finished"] == 2 and msg == "Correct":
                data["failed"].append("Test 3 should have too few fields")
            elif data["finished"] == 3 and msg == "Correct":
                data["failed"].append("Test 4 should have invalid data types")
            elif data["finished"] == 4 and msg != "Correct":
                data["failed"].append("Test 5 should be correct")
            elif data["finished"] == 5 and msg == "Correct":
                data["failed"].append("Test 6 should have too many fields")
            elif data["finished"] == 6 and msg == "Correct":
                data["failed"].append("Test 7 should have too few fields")
            elif data["finished"] == 7 and msg == "Correct":
                data["failed"].append("Test 8 should have invalid data types")
            data["finished"] += 1

        # Set message channel listener
        self.communication.client.on_message = test

        # Send correct data
        message = json.dumps(self.reached_cor)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.reached_more)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.reached_miss)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.reached_number)
        self.communication.send_message("comtest/117", message)

        # Send correct data
        message = json.dumps(self.complete_cor)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.complete_more)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.complete_miss)
        self.communication.send_message("comtest/117", message)

        # Sleep before sending next check
        time.sleep(0.3)

        # Send invalid data
        message = json.dumps(self.complete_number)
        self.communication.send_message("comtest/117", message)

        # Wait until everything is received
        while data["finished"] < data["max"]:
            pass

        # Fail test for every test
        for m in data["failed"]:
            self.fail(m)


if __name__ == "__main__":
    unittest.main()
