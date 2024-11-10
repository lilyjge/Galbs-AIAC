import pyaudio
import websockets
import asyncio

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000, output=True)
async def run(websocket_uri):
    async with websockets.connect(websocket_uri) as websocket:
        while True:
            data = await websocket.recv()
            index = 0
            while data != ' ':
                print(f"{index}")
                index += 1
                stream.write(data)
                data = await websocket.recv()
asyncio.run(run("ws://localhost:8765"))
stream.close()
audio.terminate()