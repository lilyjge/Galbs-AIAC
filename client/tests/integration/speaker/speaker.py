"""
Testing script for the speaker module.
"""

import asyncio

import pyaudio
import websockets


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000


def main() -> int:
    """
    Main function to test the speaker module.
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

    async def receive_and_play_audio(websocket_uri: str) -> None:
        async with websockets.connect(websocket_uri) as websocket:
            print("Waiting for audio data...")
            try:
                while True:
                    audio_data = await websocket.recv()
                    if not audio_data:
                        break
                    print("Playing received audio...")
                    stream.write(audio_data)
            except websockets.ConnectionClosed:
                print("Connection closed by server")
            finally:
                stream.stop_stream()
                stream.close()
                audio.terminate()

    asyncio.run(receive_and_play_audio("ws://localhost:8765"))

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
