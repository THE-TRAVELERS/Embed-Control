########################################################################################################################
#
# TODO: Implement the content in the project, prototype not final code. NOT TESTED.
#
########################################################################################################################

import asyncio
import argparse
import websockets
from websockets.exceptions import ConnectionClosed
import psutil
import os

client_id = 0


def get_cpu_temp():
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    return float(cpu_temp.replace("temp=", "").replace("'C\n", ""))


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_ram_usage():
    ram_usage = psutil.virtual_memory()
    return ram_usage.percent


async def runner_cpu_temp(websocket):
    global client_id
    client_id += 1
    current_client_id = client_id
    print(f"New client connected to CPU Temp server: {current_client_id}")
    try:
        while True:
            cpu_temp = get_cpu_temp()
            await websocket.send(str(cpu_temp))
            await asyncio.sleep(1)
            print(cpu_temp)
    except ConnectionClosed:
        print(f"Client {current_client_id} disconnected from CPU Temp server")


async def runner_cpu_usage(websocket):
    global client_id
    client_id += 1
    current_client_id = client_id
    print(f"New client connected to CPU Usage server: {current_client_id}")
    try:
        while True:
            cpu_usage = get_cpu_usage()
            await websocket.send(str(cpu_usage))
            await asyncio.sleep(1)
            print(cpu_usage)
    except ConnectionClosed:
        print(f"Client {current_client_id} disconnected from CPU Usage server")


async def runner_ram_usage(websocket):
    global client_id
    client_id += 1
    current_client_id = client_id
    print(f"New client connected to RAM Usage server: {current_client_id}")
    try:
        while True:
            ram_usage = get_ram_usage()
            await websocket.send(str(ram_usage))
            await asyncio.sleep(1)
            print(ram_usage)
    except ConnectionClosed:
        print(f"Client {current_client_id} disconnected from RAM Usage server")


async def main_cpu_temp(port):
    async with websockets.serve(runner_cpu_temp, "localhost", port):
        await asyncio.Future()


async def main_cpu_usage(port):
    async with websockets.serve(runner_cpu_usage, "localhost", port):
        await asyncio.Future()


async def main_ram_usage(port):
    async with websockets.serve(runner_ram_usage, "localhost", port):
        await asyncio.Future()


async def start_servers(cpu_temp_port, cpu_usage_port, ram_usage_port):
    print("Starting WebSocket servers...\n")
    if cpu_temp_port:
        asyncio.create_task(main_cpu_temp(cpu_temp_port))
        print(f"CPU Temp server started on: ws://localhost:{cpu_temp_port}")
    if cpu_usage_port:
        asyncio.create_task(main_cpu_usage(cpu_usage_port))
        print(f"CPU Usage server started on: ws://localhost:{cpu_usage_port}")
    if ram_usage_port:
        asyncio.create_task(main_ram_usage(ram_usage_port))
        print(f"RAM Usage server started on: ws://localhost:{ram_usage_port}")

    event = asyncio.Event()
    await event.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start WebSocket servers for CPU Temp, CPU Usage, and RAM Usage."
    )
    parser.add_argument(
        "--cpu-temp-port", type=int, help="The port number for the CPU Temp server."
    )
    parser.add_argument(
        "--cpu-usage-port", type=int, help="The port number for the CPU Usage server."
    )
    parser.add_argument(
        "--ram-usage-port", type=int, help="The port number for the RAM Usage server."
    )

    args = parser.parse_args()
    try:
        asyncio.run(
            start_servers(args.cpu_temp_port, args.cpu_usage_port, args.ram_usage_port)
        )
    except KeyboardInterrupt:
        print("WebSocket servers stopped.")
