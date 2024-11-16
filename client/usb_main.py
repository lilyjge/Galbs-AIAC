import websockets
import asyncio
import json
import base64

from modules.camera import camera
from modules.microphone import microphone
from modules.speaker import speaker    

async def take_input(queue, mic, cam):
    while True:
        frame = mic.stream.read(mic.chunk)
        if mic.is_speech(frame, mic.rate):
            mic.silence = 0
            if not mic.recording:
                print("started")
                mic.recording = True
            mic.frames.append(frame)
        else:
            mic.silence += 1
            if mic.recording and mic.silence > 10:
                audio_data = mic.send_audio2()
                image_data = cam.send_image()
                send_data = {
                    "command": "send_input",
                    "image_data": image_data,
                    "audio_data": audio_data
                }
                input = json.dumps(send_data)
                await queue.put(input)
            elif not mic.recording:
                await asyncio.sleep(0)

async def output_audio(websocket, spk):
    while True:
        received_data = await websocket.recv()
        load = json.loads(received_data)
        audio_output = load["audio_data"]
        decoded_audio = base64.b64decode(audio_output)
        await spk.play_audio(decoded_audio)

async def send_to_server(queue, websocket):
    while True:
        print("getting frame")
        input = await queue.get()
        print("sending...")
        await websocket.send(input)
        print("sent!")

async def main(websocket_uri):
    cam = camera.Camera()
    mic = microphone.Microphone()
    spk = speaker.Speaker()
    queue = asyncio.Queue()
    async with websockets.connect(websocket_uri) as websocket:
        input_task = asyncio.create_task(take_input(queue, mic, cam))
        send_task = asyncio.create_task(send_to_server(queue, websocket))
        output_task = asyncio.create_task(output_audio(websocket, spk))
        await asyncio.gather(input_task, send_task, output_task)
          
asyncio.run(main("ws://localhost:8765"))