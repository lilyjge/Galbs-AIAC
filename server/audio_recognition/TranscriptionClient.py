import os

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class TranscriptionClient:
    def __init__(self, wav):
        self.wav = wav

    def transcribe(self):
        transcription = client.audio.transcriptions.create(model="whisper-1", file=self.wav)
        return transcription.text
