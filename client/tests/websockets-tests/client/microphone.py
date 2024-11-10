import wave
import webrtcvad
import pyaudio
import asyncio
import websockets

CHUNK = 1440
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 48000   

SERVER_URL = "ws://localhost:8765"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

vad = webrtcvad.Vad()
vad.set_mode(3)

def is_speech(frame, sample_rate):
    return vad.is_speech(frame, sample_rate)

async def record_audio(queue):
    frames = []
    recording = False
    index = 0
    print("listening")
    try:
        while True:
            frame = stream.read(CHUNK)
            if is_speech(frame, RATE):
                if not recording:
                    print("started")
                    recording = True
                frames.append(frame)
            else:
                if recording:
                    print("no more recording")
                    fn = "output" + str(index) + ".wav"
                    index += 1
                    # save_audio(frames, fn)
                    await queue.put(frames)
                    frames = []
                    recording = False
                else:
                    await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        print("ended")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        pass

async def send_audio(websocket, queue):
    while True:
        print("getting frame")
        frames = await queue.get()
        # process data...
        print("sending...")
        frame = b''.join(frames)
        await websocket.send(frame)
        queue.task_done()
        print("sent!")

async def main():
    queue = asyncio.Queue()
    async with websockets.connect(SERVER_URL) as websocket:
        listener_task = asyncio.create_task(record_audio(queue))
        sender_task = asyncio.create_task(send_audio(websocket, queue))
        await asyncio.gather(listener_task, sender_task)

asyncio.run(main())

def save_audio(frames, filename="output.wave"):
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()