# import cv2
# import board
# import base64
import asyncio
import websockets
from utils import Utils

# from busio import I2C
import adafruit_bme680


class Websockets:
    def __init__(self):
        # self.i2c = I2C(board.SCL, board.SDA)
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, debug=False)

    async def ws_video(websocket):
        # await websocket.send("Connection Established")

        # try:
        #     capture = cv2.VideoCapture(0)

        #     while capture.isOpened():
        #         _, frame = capture.read()

        #         encoded = cv2.imencode(".jpg", frame)[1]

        #         data = str(base64.b64encode(encoded))
        #         data = data[2 : len(data) - 1]

        #         await websocket.send(data)

        #     capture.release()

        # except websockets.connection.ConnectionClosed:
        #     capture.release()

        # except Exception as e:
        #     raise e
        pass

    async def ws_external_sensor(self, websocket, port, delay=1):
        try:
            sensor_values = {
                int(Utils.read_variable("SENSOR_HUMIDITY_PORT")): self.bme680.humidity,
                int(
                    Utils.read_variable("SENSOR_TEMPERATURE_PORT")
                ): self.bme680.temperature,
                int(Utils.read_variable("SENSOR_PRESSURE_PORT")): self.bme680.pressure,
            }

            while True:
                value = sensor_values.get(port, -1)
                await websocket.send(str(value))
                await asyncio.sleep(delay)

        except websockets.exceptions.ConnectionClosed:
            pass

    async def ws_internal_sensors(self, websocket, port):
        pass
