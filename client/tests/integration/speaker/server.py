"""
Test server script to send audio data to the speaker client.
"""

import asyncio
import wave

import websockets


AUDIO_FILE = "./test_audio.wav"


def main() -> int:
    """
    Main function to run the test server for the speaker module.
    """

    async def send_audio(websocket: websockets.WebSocketServerProtocol) -> None:
        print("Sending audio data to client...")
        with wave.open(AUDIO_FILE, "rb") as wf:
            data = wf.readframes(wf.getnframes())
            try:
                await websocket.send(data)
                print("Audio data sent")
            except websockets.ConnectionClosed:
                print("Connection closed by client")

    async def main_server() -> None:
        async with websockets.serve(send_audio, "localhost", 8765):
            await asyncio.Future()  # Run forever

    asyncio.run(main_server())

    return 0


if __name__ == "__main__":
    result = main()
    if result != 0:
        print(f"ERROR: Status code: {result}")
    print("Server shut down")
