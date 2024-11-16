import asyncio
from websockets.asyncio.server import serve
import json
import base64
import cv2
import numpy as np
import wave
import pyaudio

CHUNK = 1440
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 48000   

p = pyaudio.PyAudio()

async def hello(websocket):
    while True:
        data = await websocket.recv()
        load = json.loads(data)

        audio_bin = load["audio_data"]
        audio = base64.b64decode(audio_bin)
        wf = wave.open("./ouput.wav", "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio)
        wf.close()

        img = load["image_data"]
        jpg_og = base64.b64decode(img)
        jpgnp = np.frombuffer(jpg_og, dtype=np.uint8)
        img = cv2.imdecode(jpgnp, flags=1)
        cv2.imwrite(f"./test10.jpg", img)

        filename = "./ouput0.wav"
        wf = wave.open(filename, 'rb')
        chunk = 1024
        data = wf.readframes(chunk)
        frames = []
        while data != b'':
            frames.append(data)
            data = wf.readframes(chunk)
        data = b''.join(frames)
        audio = base64.b64encode(data).decode()
        output = {"audio_data": audio}
        outload = json.dumps(output)
        await websocket.send(outload)

    # greeting = "received!!"

    # await websocket.send(greeting)
    # print(f">>> {greeting}")

async def main():
    async with serve(hello, "localhost", 8765, max_size=None):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())