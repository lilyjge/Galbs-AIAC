from audio_recognition.TranscriptionClient import TranscriptionClient

with open("angry_converted.wav", "rb") as f:
    res = TranscriptionClient(f).transcribe()
    print("result")
    print(res)
