"""
Test server script to receive audio data from the microphone client and save it to a file.
"""

import asyncio
import wave

import pyaudio
import websockets


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000


def main() -> int:
    """
    Main function to run the test server for the microphone module.
    """
    audio = pyaudio.PyAudio()

    async def save_audio(data: bytes, filename: str = "received_audio.wav") -> None:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(data)
        print(f"Audio saved as {filename}")

    async def handle_client(websocket: websockets.WebSocketServerProtocol) -> None:
        index = 0
        while True:
            audio_data = await websocket.recv()
            print("Received audio data")
            filename = f"received_audio_{index}.wav"
            await save_audio(audio_data, filename)
            index += 1

    async def main_server() -> None:
        async with websockets.serve(handle_client, "localhost", 8765):
            await asyncio.Future()  # Run forever

    asyncio.run(main_server())

    return 0


if __name__ == "__main__":
    result = main()
    if result != 0:
        print(f"ERROR: Status code: {result}")
    print("Server shut down")
