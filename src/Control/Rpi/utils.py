import os
import cv2
import board
import base64
import asyncio
import websockets
from busio import I2C
import adafruit_bme680


class Utils:
    """
    A class to represent a utility object.

    ...

    Methods
    -------
    unwrap_message(message: list) -> str:
        Unwraps a message from a list and returns it as a string.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the utility object.
        """
        self.i2c = I2C(board.SCL, board.SDA)
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, debug=False)

    def unwrap_message(self, message):
        """
        Unwraps a message from a list and returns it as a string.

        Parameters
        ----------
            message : list
                a list containing a single string

        Returns
        -------
            str
                a string representing the unwrapped message
        """
        if not isinstance(message, list) or not all(
            isinstance(m, str) for m in message
        ):
            raise ValueError("Input must be a list of strings")

        unwrapped_message = str(message[0])
        unwrapped_message = unwrapped_message[1:].strip("'")
        return unwrapped_message

    async def ws_video(websocket):
        """
        Captures the video stream from the camera and transmits it to the client.

        Parameters
        ----------
            websocket : websockets.WebSocketServerProtocol
                a WebSocket server protocol object

        Raises
        ------
            websockets.connection.ConnectionClosed
                if the client disconnects from the server

            Exception
                if an error occurs during the transmission

        """
        print("Client Connected !")
        await websocket.send("Connection Established")

        try:
            capture = cv2.VideoCapture(0)

            while capture.isOpened():
                _, frame = capture.read()

                encoded = cv2.imencode(".jpg", frame)[1]

                data = str(base64.b64encode(encoded))
                data = data[2 : len(data) - 1]

                await websocket.send(data)

            capture.release()

        except websockets.connection.ConnectionClosed:
            print("Client Disconnected !")
            capture.release()

        except Exception as e:
            print(f"Something went wrong: {e}")

    async def ws_sensor(self, websocket, port):
        """
        Captures the sensor data and transmits it to the client.

        Parameters
        ----------
            port: int
                the port number to listen on

        Raises
        ------
            websockets.connection.ConnectionClosed
                if the client disconnects from the server

            Exception
                if an error occurs during the transmission

        """
        client_id = 0
        client_id += 1
        current_client_id = client_id
        print(f"New client connected: {current_client_id}")
        value = -1

        try:
            while True:
                if port == 8765:
                    value = self.bme680.pressure
                elif port == 8766:
                    value = self.bme680.temperature
                elif port == 8767:
                    value = self.bme680.humidity
                await websocket.send(str(value))
                print(value)
                await asyncio.sleep(1)

        except websockets.exceptions.ConnectionClosed:
            print(f"Client {current_client_id} disconnected")

    def clear_console(self):
        """
        Clears the console screen.
        """
        os.system("clear")
