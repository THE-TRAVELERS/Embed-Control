import asyncio
import websockets
import cv2
import board
import base64
from busio import I2C
import adafruit_bme680


class Websockets:
    def __init__(self):
        self.i2c = I2C(board.SCL, board.SDA)
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, debug=False)

    async def ws_video(websocket):
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
