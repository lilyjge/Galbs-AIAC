'''
A script that takes in text input and emotions to generate a relevant text output.
'''

import numpy as np
from API_KEY import GROQ_API_KEY
api_key = GROQ_API_KEY
from groq import Groq

client = Groq(
    api_key=api_key,
)

VALID_EMOTION_LEVEL = 0.5

# TO BE COMPLETED DURING INTEGRATION
# Obtains user audio input text data from audio-recognition
def detect_audio(text):
    return text

# TO BE COMPLETED DURING INTEGRATION
# Obtains user facial emotions data from facial-recognition
def detect_emotions(emotions):
    valid_emotions = {}
    for emotion in emotions['emotion']:
        if emotions['emotion'][emotion] > VALID_EMOTION_LEVEL:
            valid_emotions[emotion] = emotions['emotion'][emotion]
    
    return valid_emotions


# Formats emotions
def format_emotions(emotions):
    emotions_text = ""
    for emotion in emotions:
        emotions_text += (emotion + " at " + str(emotions[emotion]) + ", ")
    return emotions_text[:-2]


# Generates text reponse using openAI API
def generate_response(input_text, emotions):

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a good friend that provides insightful responses. Emotions Detected: " + emotions
            },
            {
                "role": "user",
                "content": input_text
            }
        ]
    )

    return response.choices[0].message.content


# TESTING
if __name__ == "__main__":
    print("TEXT: ")
    user_input = input()
    emotions_input = {'emotion': {'angry': np.float32(6.2788945e-06), 'disgust': np.float32(1.12710405e-13), 'fear': np.float32(8.1948154e-10), 'happy': np.float32(99.39528), 'sad': np.float32(1.3383974e-06), 'surprise': np.float32(0.00043022225), 'neutral': np.float32(0.60428834)}, 'dominant_emotion': 'happy', 'region': {'x': 1, 'y': 1, 'w': 114, 'h': 114, 'left_eye': None, 'right_eye': None}, 'face_confidence': np.float64(0.94)}

    text = detect_audio(user_input)
    emotions = format_emotions(detect_emotions(emotions_input))

    response = generate_response(text, emotions)
    
    print(response)

