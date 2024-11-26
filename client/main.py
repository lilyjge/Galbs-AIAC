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
from API_KEY import PVCOBRA_KEY

cam = camera.Camera()
mic = microphone.Microphone(PVCOBRA_KEY, rate=16000, chunk=256, threshhold=0.025, silence_until_stop=200)
spk = speaker.Speaker()
stepper_motor_left = stepper_motor.StepperMotor((18, 23, 24, 25), True)
stepper_motor_right = stepper_motor.StepperMotor((12, 16, 20, 21), False)
rgb_led1 = rgb_led.RgbLed(17, 27, 22, False)
rgb_led2 = rgb_led.RgbLed(5, 6, 13, True)

async def process(websocket: websockets.WebSocketClientProtocol) -> None:
    """
    Capture audio and image data when speech is detected and put it into the queue.
    """
    while True:
        frame = mic.stream.read(mic.chunk)
        if mic.is_speech(frame):
            audio_data = await mic.record_audio()
            image_data = cam.send_image()
            send_data = {
                "command": "send_input",
                "image_data": image_data,
                "audio_data": audio_data
            }
            input_data = json.dumps(send_data)
            await websocket.send(input_data)
            print("sent data")
            
            # Process data received from the server.
            received_data = await websocket.recv()
            print("received data")
            load = json.loads(received_data)
            if load["command"] == "send_output":
                print("Response received")
                if "led_data" in load:
                    await handle_rgb_led(load)
                if "motor_data" in load:
                    await handle_stepper_motor(load)
                if "audio_data" in load:
                    audio_output = load["audio_data"]
                    decoded_audio = base64.b64decode(audio_output)
                    await spk.play_audio(decoded_audio)
                if "motor_data" in load:
                    await handle_stepper_motor({"motor_data":0})
                if "led_data" in load:
                    await handle_rgb_led({"led_data":(0,0,0)})
            elif load["command"] == "ping":
                await websocket.send("Received ping")
            
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

async def main(websocket_uri: str) -> None:
    """
    Main function to initiate the connection and run tasks.
    """
    async with websockets.connect(websocket_uri) as websocket:
        task = asyncio.create_task(process(websocket))
        await asyncio.gather(task)

if __name__ == "__main__":
    asyncio.run(main("ws://172.20.10.4:8000/ws/api/"))
