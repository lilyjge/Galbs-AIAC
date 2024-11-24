"""
Main client script.
"""

import base64
import json
import time

import asyncio
import websockets

from modules.camera import camera
from modules.microphone import microphone
from modules.speaker import speaker    
from modules.stepper_motor import stepper_motor
from modules.stepper_motor import simultaneous
from modules.rgb_led import rgb_led
from modules.rgb_led import color

cam = camera.Camera()
mic = microphone.Microphone()
spk = speaker.Speaker()
stepper_motor_left = stepper_motor.StepperMotor((18, 23, 24, 25), True)
stepper_motor_right = stepper_motor.StepperMotor((12, 16, 20, 21), False)
rgb_led1 = rgb_led.RgbLed(17, 27, 22, False)
rgb_led2 = rgb_led.RgbLed(5, 6, 13, True)

async def take_input(queue: asyncio.Queue) -> None:
    """
    Capture audio and image data when speech is detected and put it into the queue.
    """
    while True:
        frame = mic.stream.read(mic.chunk)
        if mic.is_speech(frame, mic.rate):
            audio_data = await mic.record_audio()
            image_data = cam.send_image()
            send_data = {
                "command": "send_input",
                "image_data": image_data,
                "audio_data": audio_data
            }
            input_data = json.dumps(send_data)
            await queue.put(input_data)
        else:
            await asyncio.sleep(0)  # Yield control to the event loop

async def handle_stepper_motor(data: dict) -> None:
    """
    Handle stepper motor movements based on the received data.
    """
    angle = data['motor_data']
    simultaneous.set_position(angle, stepper_motor_left, stepper_motor_right)

async def handle_rgb_led(data: dict) -> None:
    """
    Handle RGB LED color changes based on the received data.
    """
    rgb_color = data['led_data']
    duration = 500
    result, color_obj = color.Color.create(*rgb_color)
    if result:
        rgb_led1.fade_color(color_obj, duration)
        rgb_led2.fade_color(color_obj, duration)

async def process_received_data(websocket: websockets.WebSocketClientProtocol) -> None:
    """
    Process data received from the server.
    """
    while True:
        received_data = await websocket.recv()
        load = json.loads(received_data)
        if load["command"] == "send_output":
            print("Response received")
            if "audio_data" in load:
                audio_output = load["audio_data"]
                decoded_audio = base64.b64decode(audio_output)
                spk.play_audio(decoded_audio)
            if "motor_data" in load:
                await handle_stepper_motor(load)
            if "led_data" in load:
                await handle_rgb_led(load)
        elif load["command"] == "ping":
            await websocket.send("Received ping")

async def send_to_server(queue: asyncio.Queue, websocket: websockets.WebSocketClientProtocol) -> None:
    """
    Send data from the queue to the server.
    """
    while True:
        input_data = await queue.get()
        await websocket.send(input_data)

async def main(websocket_uri: str) -> None:
    """
    Main function to initiate the connection and run tasks.
    """
    queue = asyncio.Queue()
    async with websockets.connect(websocket_uri) as websocket:
        input_task = asyncio.create_task(take_input(queue))
        send_task = asyncio.create_task(send_to_server(queue, websocket))
        output_task = asyncio.create_task(process_received_data(websocket))
        await asyncio.gather(input_task, send_task, output_task)

if __name__ == "__main__":
    asyncio.run(main("ws://172.20.10.3:8001/ws/api/"))