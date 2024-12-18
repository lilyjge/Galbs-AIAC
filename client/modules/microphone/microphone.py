"""
Module for interfacing with microphone.
"""

import base64

import pyaudio
import pvcobra


class Microphone:
    """
    Microphone class.
    """

    def __init__(
        self,
        access_key: str,
        chunk: int = 1440,
        format: int = pyaudio.paInt16,
        channels: int = 1,
        rate: int = 48000,
        threshold: float = 0.5,
        silence_until_stop: int = 100,
    ) -> None:
        """
        Initializes the microphone with specifications.

        chunk: number of audio frames read in each processing cycle
        format: datatype of audio
        channels: number of audio channels
        rate: number of audio frames per second
        threshold: probability threshold for detecting sound, increase for stricter, less sensitive, and decrease for more sensitive
        silence_until_stop: number of silent frames before recording is stopped, adjust accordingly to frame rate
        """

        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
        )

        self.vad = pvcobra.create(access_key)
        self.threshold = threshold
        self.silence_until_stop = silence_until_stop

        self.frames = []
        self.recording = False
        self.silence = 0

    def is_speech(self, frame: bytes) -> bool:
        """
        Detects if there is sound in chunk of audio.

        frame: chunk of audio
        Returns True if there is sound and False if it is silent.
        """
        voice_probability = self.vad.process(frame)
        return voice_probability > self.threshold

    def send_audio(self) -> str:
        """
        Encodes audio with base64, resets recording variables, and returns encoded audio data.
        """
        f = b"".join(self.frames)
        encoded = base64.b64encode(f).decode()
        self.frames = []
        self.recording = False
        self.silence = 0
        return encoded

    async def record_audio(self) -> str:
        """
        Records audio to be sent until silence for period of time.
        """
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
                if self.recording and self.silence < self.silence_until_stop:
                    self.frames.append(frame)

    def close(self) -> None:
        """
        Closes audio stream.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.vad.delete()
