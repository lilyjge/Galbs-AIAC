"""
Testing script for the microphone module.
"""

import asyncio

import pyaudio
import webrtcvad
import websockets


CHUNK = 1440
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
SERVER_URL = "ws://localhost:8765"


def main() -> int:
    """
    Main function to test the microphone module.
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    vad = webrtcvad.Vad(3)

    async def record_and_send_audio(websocket: websockets.WebSocketServerProtocol) -> None:
        print("Listening...")
        try:
            while True:
                frame = stream.read(CHUNK)
                if vad.is_speech(frame, RATE):
                    print("Speech detected, recording...")
                    frames = [frame]
                    while True:
                        frame = stream.read(CHUNK)
                        frames.append(frame)
                        if not vad.is_speech(frame, RATE):
                            print("Speech ended, sending audio...")
                            audio_data = b"".join(frames)
                            await websocket.send(audio_data)
                            break
                else:
                    await asyncio.sleep(0.01)
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    async def run() -> None:
        async with websockets.connect(SERVER_URL) as websocket:
            await record_and_send_audio(websocket)

    asyncio.run(run())

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
