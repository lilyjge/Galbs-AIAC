# Module for interfacing with microphone.

import pyaudio
import asyncio
import websockets
import base64
import pvcobra

class Microphone:
    # Microphone class.

    def __init__(self, access_key, chunk=1440, format=pyaudio.paInt16, channels=1, rate=48000, threshhold=0.5, silence_until_stop=100):
        """
        Initializes the microphone with specifications.

        chunk: number of audio frames read in each processing cycle
        format: datatype of audio
        channels: number of audio channels 
        rate: number of audio frames per second
        threshhold: probability threshhold for detecting sound, increase for stricter, less sensitive, and decrease for more sensitive
        silence_until_stop: number of silent frames before recording is stopped, adjust accordingly to frame rate 
        """

        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

        self.queue = asyncio.Queue()

        # self.vad = webrtcvad.Vad()
        # self.vad.set_mode(3)
        
        self.vad = pvcobra.create(access_key)
        self.threshhold = threshhold
        self.silence_until_stop = silence_until_stop

        self.frames = []
        self.recording = False
        self.silence = 0

    def is_speech(self, frame):
        # Detects if there is sound in chunk of audio.
        # frame: chunk of audio
        # sample_rate: number of audio frames per second
        # Returns True if there is sound and False if it is silent.
        voice_probability = self.vad.process(frame)
        # return self.vad.is_speech(frame, sample_rate)
        print(voice_probability > self.threshhold)
        return voice_probability > self.threshhold
    
    def send_audio(self):
        f = b''.join(self.frames)
        encoded = base64.b64encode(f).decode()
        self.frames = []
        self.recording = False
        self.silence = 0
        return encoded
    
    async def record_audio(self):
        # Processes audio input and places audio chunks with sound into queue to be sent.
        # print("listening")
        while True:
            frame = self.stream.read(self.chunk)
            if self.is_speech(frame):
                self.silence = 0
                if not self.recording:
                    print("started")
                    self.recording = True
                self.frames.append(frame)
            else:
                self.silence += 1
                if self.recording and self.silence > self.silence_until_stop:
                    print("no more recording")
                    return self.send_audio()
                elif self.recording and self.silence < self.silence_until_stop:
                    self.frames.append(frame)

    async def direct_send(self, websocket):
        # Sends recorded audio chunks by websocket. 
        # websocket: websocket to send audio through
        while True:
            print("getting frame")
            frames = await self.queue.get()
            print("sending...")
            frame = b''.join(frames)
            await websocket.send(frame)
            self.queue.task_done()
            print("sent!")

    async def run(self, websocket_uri):
        # Records and sends audio asynchronously. 
        # websocket_uri: the uri of the websocket to connect with and send audio to
        async with websockets.connect(websocket_uri) as websocket:
            listener_task = asyncio.create_task(self.record_audio())
            sender_task = asyncio.create_task(self.send_audio(websocket))
            await asyncio.gather(listener_task, sender_task)
    
    def close(self):
        # Closes audio stream. 
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.vad.delete()
