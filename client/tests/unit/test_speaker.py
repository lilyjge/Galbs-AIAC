"""
Testing script for the speaker module.
"""

import base64
import wave

import soundfile

from modules.speaker import speaker


def main() -> int:
    """
    Main.
    """
    file_path = "./client/output.wav"

    # Read and rewrite the file with soundfile
    data, samplerate = soundfile.read(file_path)
    soundfile.write(file_path, data, samplerate)

    # Now try to open the file with wave
    with wave.open(file_path) as wf:
        print("File opened!")
        chunk = 1024
        data = wf.readframes(chunk)
        frames = []
        while data != b"":
            frames.append(data)
            data = wf.readframes(chunk)
        data = b"".join(frames)
        encoded = base64.b64encode(data).decode()
        decoded_audio = base64.b64decode(encoded)
        spk = speaker.Speaker()
        spk.play_audio(decoded_audio)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
