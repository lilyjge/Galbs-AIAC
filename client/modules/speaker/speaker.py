"""
Module for interfacing with speaker.
"""

import pyaudio


class Speaker:
    """
    Speaker class.
    """

    def __init__(self, format: int = pyaudio.paInt16, channels: int = 1, rate: int = 44100) -> None:
        """
        Initializes the speaker with specifications.

        format: datatype of audio
        channels: number of audio channels
        rate: number of audio frames per second
        """

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=format, channels=channels, rate=rate, output=True)

    async def play_audio(self, data: str) -> None:
        """
        Plays audio.

        data: audio data
        """
        self.stream.write(data)
        print("DONE SPEAKING")

    def close(self) -> None:
        """
        Closes audio stream.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
