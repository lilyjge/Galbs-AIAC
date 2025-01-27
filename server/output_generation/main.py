"""
A script that takes text input (parsed from audio input) and emotions dictionary (parsed from facial input) to generate audio output, motor angle for arm response, and LED light response as RGB.
"""

import numpy as np
from groq import Groq
from output_generation.API_KEY import GROQ_API_KEY, ELEVENLABS_API_KEY
from output_generation.BEHAVIOUR import ANGLE_SCALE, MOTOR, COLOUR
import requests

client = Groq(
    api_key=GROQ_API_KEY,
)

headers = {"Accept": "application/json", "xi-api-key": ELEVENLABS_API_KEY}

VOICE_ID = "9BWtsMINqrJLrRacOk9x"
VALID_EMOTION_LEVEL = 0.5


# Obtains user audio input text data from audio-recognition
def detect_audio(text):
    return text


# Obtains user facial emotions data from facial-recognition
def detect_emotions(emotions):
    if emotions == None:
        return None

    valid_emotions = {}
    for emotion in emotions["emotion"]:
        if emotions["emotion"][emotion] > VALID_EMOTION_LEVEL:
            valid_emotions[emotion] = emotions["emotion"][emotion]

    return valid_emotions


# Formats emotions
def format_emotions(emotions):
    if emotions == None:
        return None

    emotions_text = ""
    for emotion in emotions:
        emotions_text += emotion + " at " + str(emotions[emotion]) + ", "
    return emotions_text[:-2]


# Generates text reponse using openAI API
def generate_response(input_text, emotions):
    system_prompt = (
        "You are a good friend that provides insightful and brief (maximum 12 words) responses."
    )
    if emotions is not None:
        system_prompt += " Emotions Detected: " + emotions
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ],
    )
    return response.choices[0].message.content


# Text to Speech
def tts(voice_id, text, output_file):
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
        headers=headers,
        json=data,
        stream=True,
    )

    with open(f"output_generation/audio_output_files/{output_file}", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)


# Generate motor control response
def motor_response(emotions):
    if emotions is None:
        return MOTOR["neutral"]
    return int(ANGLE_SCALE * MOTOR[emotions["dominant_emotion"]])


# Generate LED lights response
def lights_response(emotions):
    if emotions is None:
        return COLOUR["neutral"]
    return COLOUR[emotions["dominant_emotion"]]


# Testing
if __name__ == "__main__":
    # Input
    print("TEXT: ")
    user_input = input()
    print("EMOTIONS: ")
    emotions_input = {
        "emotion": {
            "happy": np.float32(6.2788945e-06),
            "disgust": np.float32(1.12710405e-13),
            "fear": np.float32(8.1948154e-10),
            "angry": np.float32(99.39528),
            "sad": np.float32(1.3383974e-06),
            "surprise": np.float32(0.00043022225),
            "neutral": np.float32(0.60428834),
        },
        "dominant_emotion": "angry",
        "region": {"x": 1, "y": 1, "w": 114, "h": 114, "left_eye": None, "right_eye": None},
        "face_confidence": np.float64(0.94),
    }
    print("FILE (___.wav): ")
    output = input()

    text = detect_audio(user_input)

    # Text response
    response = generate_response(text, format_emotions(detect_emotions(emotions_input)))
    print(response)

    # Audio file
    print("AUDIO: ")
    tts(VOICE_ID, response, f"{output}.wav")
    print(f"To {output}.wav")

    # Motor
    print("MOTOR: ")
    print(motor_response(emotions_input))

    # Lights
    print("LIGHTS: ")
    print(lights_response(emotions_input))
