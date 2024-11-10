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

async def save_audio(frame, filename="output.wave"):
    print(type(frame))
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(frame)
    wf.close()

async def hello(websocket):
    index = 0
    while True:
        data = await websocket.recv()
        print("received stuff")
        print(type(data))
        await save_audio(data, "ouput" + str(index) + ".wav")
        index += 1

    # greeting = "received!!"

    # await websocket.send(greeting)
    # print(f">>> {greeting}")

async def main():
    async with serve(hello, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())