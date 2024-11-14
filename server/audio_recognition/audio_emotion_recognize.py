# For now we use hugging face, we may extend this to use a different library in the future

import torch
from transformers import Wav2Vec2Processor, Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification


import librosa

audio_path = "angry.wav"

model_name = "superb/wav2vec2-large-superb-er"  # Replace with the correct model path
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)


def processed(file_path):
    audio, sample_rate = librosa.load(file_path, sr=16000)  # Resample to 16kHz
    inputs = feature_extractor(audio, sampling_rate=sample_rate, return_tensors="pt", padding=True)
    return inputs


class AudioEmotionRecognize:
    def __init__(self, wav, wav_file):
        self.wav = wav
        self.wav_file = wav_file
        self.recognizer_inputs = processed(wav_file) # inputs for hugging face model to use
    
    # for now we use filepath, we may change in the future

    """
    {0: 'neu', 1: 'hap', 2: 'ang', 3: 'sad'}
    ENUM of: neu, hap, ang, sad
    """

    def get_emotion(self):
        # prediction
        with torch.no_grad():
            logits = model(**self.recognizer_inputs).logits
            predicted_class_id = torch.argmax(logits).item()

        # Interpret the result
        labels = model.config.id2label
        emotion = labels[predicted_class_id]
        return emotion                
        
        