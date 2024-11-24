import websockets
import asyncio
import json
import base64
import time

# from modules.camera import camera
# from modules.microphone import microphone
# from modules.speaker import speaker
from modules.stepper_motor import stepper_motor
from modules.rgb_led import rgb_led
from modules.rgb_led import color

from modules.stepper_motor import simultaneous

# Initialize stepper motors and RGB LEDs
stepper_motor_left = stepper_motor.StepperMotor((18, 23, 24, 25), True)
stepper_motor_right = stepper_motor.StepperMotor((12, 16, 20, 21), False)
rgb_led1 = rgb_led.RgbLed(17, 27, 22, False)
rgb_led2 = rgb_led.RgbLed(5, 6, 13, True)

async def take_input(queue):
    while True:
        send_data = {
            "command": "send_input",
            "image_data": "null",
            "audio_data": "null",
        }
        input_data = json.dumps(send_data)
        print("data sent")
        await queue.put(input_data)
        await asyncio.sleep(3)
        
async def handle_stepper_motor(data):
    angle = data['motor_data']
    speed = 300  # Default speed, adjust as needed
    simultaneous.set_position(angle, stepper_motor_left, stepper_motor_right)

async def handle_rgb_led(data):
    rgb_color = data['led_data']
    duration = 500  # Default duration, adjust as needed
    result, color_obj = color.Color.create(*rgb_color)
    if result:
        rgb_led1.fade_color(color_obj, duration)
        rgb_led2.fade_color(color_obj, duration)

async def process_received_data(websocket):
    while True:
        received_data = await websocket.recv()
        load = json.loads(received_data)
        if load["command"] == "send_output":
            print("response received")
            if "motor_data" in load:
                await handle_stepper_motor(load)
            if "led_data" in load:
                await handle_rgb_led(load)
        elif load["command"] == "ping":
            await websocket.send("received ping")

async def send_to_server(queue, websocket):
    while True:
        input_data = await queue.get()
        await websocket.send(input_data)

async def main(websocket_uri):
    queue = asyncio.Queue()
    async with websockets.connect(websocket_uri) as websocket:
        input_task = asyncio.create_task(take_input(queue))
        send_task = asyncio.create_task(send_to_server(queue, websocket))
        output_task = asyncio.create_task(process_received_data(websocket))
        await asyncio.gather(input_task, send_task, output_task)

asyncio.run(main("ws://172.20.10.3:8001/ws/api/"))
