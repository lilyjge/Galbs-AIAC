# Module for interfacing with speaker.

import pyaudio
import websockets

class Speaker:
    # Speaker class.

    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100):
        """
        Initializes the speaker with specifications.

        format: datatype of audio
        channels: number of audio channels 
        rate: number of audio frames per second
        """
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=format, channels=channels, rate=rate, output=True)

    async def play_audio(self, data):
        """
        Plays audio.

        data: audio data
        """
        self.stream.write(data)
        print("DONE SPEAKING")

    def close(self):
        """
        Closes audio stream.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
