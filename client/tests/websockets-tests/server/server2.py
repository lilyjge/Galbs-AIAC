#!/usr/bin/env python

import asyncio
import pyaudio
import wave
from websockets.asyncio.server import serve

CHUNK = 1440
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 48000   

audio = pyaudio.PyAudio()

async def hello(websocket):
    index = 0
    # while True:
        # if index != 0:
        #     continue
    filename = "./ouput0.wav"
    wf = wave.open(filename, 'rb')
    chunk = 1024
    data = wf.readframes(chunk)
    while data != b'':
        print(f"{index}")
        index += 1
        await websocket.send(data)
        data = wf.readframes(chunk)

    # greeting = "received!!"

    # await websocket.send(greeting)
    # print(f">>> {greeting}")

async def main():
    async with serve(hello, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())