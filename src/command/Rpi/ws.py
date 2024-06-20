# import cv2
# import board
# import base64
import asyncio
import websockets
from utils import Utils

# from busio import I2C
# import adafruit_bme680


class Websockets:
    def __init__(self):
        # self.i2c = I2C(board.SCL, board.SDA)
        # self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, debug=False)
        pass
    
    async def ws_controller(self, default_speed=200 * (10 ** (-6))):
        while True:
            recept = Utils.unwrap_message(self.sckt.recvfrom(1024))
            self.i2c_utils.write_data(recept)
            await asyncio.sleep(default_speed)
    
    def ws_controller_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(
            Websockets.ws_controller,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=int(Utils.read_variable("CONTROLLER_PORT")),
        )

        loop.run_until_complete(start_server)
        loop.run_forever()

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

    def ws_video_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(
            Websockets.ws_video,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=int(Utils.read_variable("CAMERA_PORT")),
        )

        loop.run_until_complete(start_server)
        loop.run_forever()

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

    def ws_external_sensor_loop(self, port):
        start_server = websockets.serve(
            Websockets.ws_external_sensor,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=port,
        )

        asyncio.get_event_loop().run_until_complete(start_server)

    async def ws_internal_sensors(self, websocket, port):
        pass

    def ws_internal_sensors_loop(self, port):
        start_server = websockets.serve(
            Websockets.ws_internal_sensors,
            host=Utils.read_variable("RPI_ADDRESS"),
            port=port,
        )

        asyncio.get_event_loop().run_until_complete(start_server)

    

    ##########################################################
    # ! Test
    async def ws_debug(websocket):
        count = 0
        try:
            while True:
                await websocket.send(str(count))
                count += 1
                await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosed:
            pass

    def ws_debug_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(
            Websockets.ws_debug,
            host=Utils.read_variable("LOCAL_ADDRESS"),
            port=8500,
        )

        loop.run_until_complete(start_server)
        loop.run_forever()

    #####################################################################
