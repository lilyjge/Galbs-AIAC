'''

takes in audio input file returns sentiment
'''

import torch
from transformers import Wav2Vec2Processor, Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification


import librosa

audio_path = "angry.wav"

model_name = "superb/wav2vec2-large-superb-er"  # Replace with the correct model path
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

def process_audio(file_path):
    audio, sample_rate = librosa.load(file_path, sr=16000)  # Resample to 16kHz
    inputs = feature_extractor(audio, sampling_rate=sample_rate, return_tensors="pt", padding=True)
    return inputs

# Load an audio file and preprocess it
inputs = process_audio(audio_path)

# prediction
with torch.no_grad():
    logits = model(**inputs).logits
    predicted_class_id = torch.argmax(logits).item()

# Interpret the result
labels = model.config.id2label 
print(labels)
emotion = labels[predicted_class_id]
print(f"The emotion is: {emotion}")
