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
        client.subscribe('comtest/117', qos=2)

        correct = {"from": "debug", "type": "syntax", "payload": {"message": "Correct"}}
        more = {"from": "debug", "type": "syntax", "payload": {"message": "Incorrect", "errors": ["Invalid field: extra"]}}

        # Setup test cases
        self.ready_messages = [
            (
                {
                    "from": "client",
                    "type": "ready"
                },
                correct,
                "Message is correct"
            ),
            (
                {
                    "from": "client",
                    "type": "ready",
                    "extra": "stuff"
                },
                more,
                "Message has too many fields"
            )
        ]

        self.path_messages = [
            (
                {
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
                },
                correct,
                "Message is correct"
            ),
            (
                {
                    "from": "client",
                    "type": "path",
                    "payload": {
                        "startX": 0,
                        "startY": 0,
                        "startDirection": 0,
                        "endX": 1,
                        "endY": 1,
                        "endDirection": 180,
                        "pathStatus": "free",
                        "extra": "stuff"
                    }
                },
                more,
                "Message has too many fields"
            ),
            (
                {
                    "from": "client",
                    "type": "path"
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Missing field: payload", "Missing field: startX", "Missing field: startY", "Missing field: startDirection", "Missing field: endX", "Missing field: endY", "Missing field: endDirection", "Missing field: pathStatus"]
                    }
                },
                "Message has too few fields"
            )
        ]

        self.invalid_path_messages = [
            (
                {
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
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Unknown path status: plakat"]
                    }
                },
                "Message has invalid path status"
            ),
            (
                {
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
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Invalid data type (startX): string", "Invalid data type (startY): string", "Invalid data type (startDirection): string"]
                    }
                },
                "Message has invalid data type"
            )
        ]

        self.select_messages = [
            (
                {
                    "from": "client",
                    "type": "pathSelect",
                    "payload": {
                        "startX": 0,
                        "startY": 0,
                        "startDirection": 0
                    }
                },
                correct,
                "Message is correct"
            ),
            (
                {
                    "from": "client",
                    "type": "pathSelect",
                    "payload": {
                        "startX": 0,
                        "startY": 0,
                        "startDirection": 0
                    },
                    "extra": "stuff"
                },
                more,
                "Message has too many fields"
            ),
            (
                {
                    "from": "client",
                    "type": "pathSelect"
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Missing field: payload", "Missing field: startX", "Missing field: startY", "Missing field: startDirection"]
                    }
                },
                "Message has too few fields"
            ),
            (
                {
                    "from": "client",
                    "type": "pathSelect",
                    "payload": {
                        "startX": "Heyho",
                        "startY": "Moin",
                        "startDirection": "Morgen"
                    }
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Invalid data type (startX): string", "Invalid data type (startY): string", "Invalid data type (startDirection): string"]
                    }
                },
                "Message has invalid data types"
            )
        ]

        self.complete_messages = [
            (
                {
                    "from": "client",
                    "type": "targetReached",
                    "payload": {
                        "message": "Nachricht"
                    }
                },
                correct,
                "Message is correct"
            ),
            (
                {
                    "from": "client",
                    "type": "targetReached",
                    "payload": {
                        "message": "Nachricht"
                    },
                    "extra": "stuff"
                },
                more,
                "Message has too many fields"
            ),
            (
                {
                    "from": "client",
                    "type": "targetReached"
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Missing field: payload", "Missing field: message"]
                    }
                },
                "Message has too few fields"
            ),
            (
                {
                    "from": "client",
                    "type": "targetReached",
                    "payload": {
                        "message": 1
                    }
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Invalid data type (message): int"]
                    }
                },
                "Message has invalid data types"
            ),
            (
                {
                    "from": "client",
                    "type": "explorationCompleted",
                    "payload": {
                        "message": "Nachricht"
                    }
                },
                correct,
                "Message is correct"
            ),
            (
                {
                    "from": "client",
                    "type": "explorationCompleted",
                    "payload": {
                        "message": "Nachricht"
                    },
                    "extra": "stuff"
                },
                more,
                "Message has too many fields"
            ),
            (
                {
                    "from": "client",
                    "type": "explorationCompleted"
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Missing field: payload", "Missing field: message"]
                    }
                },
                "Message has too few fields"
            ),
            (
                {
                    "from": "client",
                    "type": "explorationCompleted",
                    "payload": {
                        "message": 1
                    }
                },
                {
                    "from": "debug",
                    "type": "syntax",
                    "payload": {
                        "message": "Incorrect",
                        "errors": ["Invalid data type (message): int"]
                    }
                },
                "Message has invalid data types"
            )
        ]

    def __del__(self):
        del self.communication

    def test_message_ready(self):
        """
        This test should check the syntax of the message type "ready"
        """

        for (message, expected, error_message) in self.ready_messages:
            response = self.get_response(message)

            sort_error_list(response)
            sort_error_list(expected)

            self.assertDictEqual(response, expected, error_message)

    def test_message_path(self):
        """
        This test should check the syntax of the message type "path"
        """

        for (message, expected, error_message) in self.path_messages:
            response = self.get_response(message)

            sort_error_list(response)
            sort_error_list(expected)

            self.assertDictEqual(response, expected, error_message)

    def test_message_path_invalid(self):
        """
        This test should check the syntax of the message type "path" with errors/invalid data
        """

        for (message, expected, error_message) in self.invalid_path_messages:
            response = self.get_response(message)

            sort_error_list(response)
            sort_error_list(expected)

            self.assertDictEqual(response, expected, error_message)

    def test_message_select(self):
        """
        This test should check the syntax of the message type "pathSelect"
        """

        for (message, expected, error_message) in self.select_messages:
            response = self.get_response(message)

            sort_error_list(response)
            sort_error_list(expected)

            self.assertDictEqual(response, expected, error_message)

    def test_message_complete(self):
        """
        This test should check the syntax of the message type "explorationCompleted" or "targetReached"
        """

        for (message, expected, error_message) in self.complete_messages:
            response = self.get_response(message)

            sort_error_list(response)
            sort_error_list(expected)

            self.assertDictEqual(response, expected, error_message)

    def get_response(self, payload):
        answer = {"data": {}}

        def on_message(client, _, message):
            # Parse Response
            response = json.loads(message.payload.decode('utf-8'))
            print(response)

            # Only accept syntax messages
            if response["type"] != "syntax":
                return

            # Save response
            answer["data"] = response

        # Set message channel listener
        self.communication.client.on_message = on_message

        # Send payload to comtest channel
        self.communication.send_message("comtest/117", payload)

        # Wait until message is received
        while answer["data"] == {}:
            pass

        return answer["data"]


def sort_error_list(payload):
    if "payload" in payload and "errors" in payload["payload"]:
        payload["payload"]["errors"].sort()


if __name__ == "__main__":
    unittest.main()
