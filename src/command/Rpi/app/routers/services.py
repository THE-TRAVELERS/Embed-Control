import logging
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import psutil

import cv2
import base64

from app.i2c import I2CUtils

DEFAULT_SENSOR_UPDATE_INTERVAL = 1
DEFAULT_MOTOR_CONTROL_INTERVAL = 0.0002


class WebSocketsServices:
    async def ws_debug(websocket: WebSocket):
        """
        A WebSocket endpoint for debugging purposes. Sends an incrementing count every second.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        count = 0
        while True:
            await websocket.send_text(str(count))
            count += 1
            await asyncio.sleep(1)

    async def ws_controller(
        websocket: WebSocket, delay: float = DEFAULT_MOTOR_CONTROL_INTERVAL
    ):
        """
        A WebSocket endpoint for controlling the device. Placeholder for actual control logic.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (float): The default speed for the control loop. Defaults to 0.0002.
        """
        DEFAULT_STOP_ORDER = "0,0"
        try:
            while True:
                # TODO: Not tested, forward to websocket and format (x,y)
                recieved_orders = await websocket.receive_text()
                I2CUtils.write_data(recieved_orders)
                # await asyncio.sleep(delay)  # May not be useful
        except WebSocketDisconnect:
            I2CUtils.write_data(DEFAULT_STOP_ORDER)
            logging.info("[WEBSOCKETS] Controller stopped.")
            raise WebSocketDisconnect
        except Exception as e:
            logging.error("[WEBSOCKETS] An error occured in the controller websocket.")
            raise e

    async def ws_camera(websocket: WebSocket):
        """
        A WebSocket endpoint for video streaming. Placeholder for actual video streaming logic.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        # TODO: Not tested
        try:
            I2CUtils.camera.start()
            while True:
                frame = I2CUtils.camera.capture_array()
                _, encoded = cv2.imencode(".jpg", frame)
                data = str(base64.b64encode(encoded))
                data = data[2 : len(data) - 1]  # remove the quotes from the encoding
                await websocket.send_text(data)
        except WebSocketDisconnect:
            I2CUtils.camera.stop()
            logging.info("[WEBSOCKETS] Video stream stopped.")
            raise WebSocketDisconnect
        except Exception as e:
            I2CUtils.camera.stop()
            logging.error(f"[WEBSOCKETS] Error in video stream: {e}")

    async def ws_external_humidity(
        websocket: WebSocket, delay: int = DEFAULT_SENSOR_UPDATE_INTERVAL
    ):
        """
        A WebSocket endpoint for external humidity sensor data. Placeholder for actual sensor data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            await websocket.send_text(str(I2CUtils.bme680.humidity))
            await asyncio.sleep(delay)

    async def ws_external_temperature(websocket: WebSocket, delay: int = 1):
        """
        A WebSocket endpoint for external temperature sensor data. Placeholder for actual sensor data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            await websocket.send_text(str(I2CUtils.bme680.temperature))
            await asyncio.sleep(delay)

    async def ws_external_pressure(
        websocket: WebSocket, delay: int = DEFAULT_SENSOR_UPDATE_INTERVAL
    ):
        """
        A WebSocket endpoint for external pressure sensor data. Placeholder for actual sensor data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            await websocket.send_text(str(I2CUtils.bme680.pressure))
            await asyncio.sleep(delay)

    async def ws_internal_cpu_temperature(
        websocket: WebSocket, delay: int = DEFAULT_SENSOR_UPDATE_INTERVAL
    ):
        """
        A WebSocket endpoint for internal CPU temperature data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            temps = psutil.sensors_temperatures()
            if not temps:
                await websocket.send_text("Cannot read any temperature")
            cpu_temp = temps["cpu_thermal"][0].current
            await websocket.send_text(str(round(cpu_temp, 2)))
            await asyncio.sleep(delay)

    async def ws_internal_cpu_usage(
        websocket: WebSocket, delay: int = DEFAULT_SENSOR_UPDATE_INTERVAL
    ):
        """
        A WebSocket endpoint for internal CPU usage data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            await websocket.send_text(str(round(psutil.cpu_percent(interval=1), 2)))
            await asyncio.sleep(delay)

    async def ws_internal_ram_usage(
        websocket: WebSocket, delay: int = DEFAULT_SENSOR_UPDATE_INTERVAL
    ):
        """
        A WebSocket endpoint for internal RAM usage data. Placeholder for actual data retrieval.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            delay (int): The delay between data sends. Defaults to 1 second.
        """
        while True:
            await websocket.send_text(str(round(psutil.virtual_memory().percent, 2)))
            await asyncio.sleep(delay)
