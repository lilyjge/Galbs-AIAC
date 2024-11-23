# Files to help test audo emotion recognize.py
from audio_recognition.audio_emotion_recognize import AudioEmotionRecognize

if __name__ == '__main__':
    wav_file = "angry.wav"
    a = AudioEmotionRecognize(None, wav_file)
    
    emotion = a.get_emotion()
    print(emotion)
    
    
    happy_file = "../output_generation/audio_output_files/happy.mp3"
    b = AudioEmotionRecognize(None, wav_file)

    emotion = b.get_emotion()
    print(emotion)
    
    
    angry_file = "../output_generation/audio_output_files/angry.mp3"
    c = AudioEmotionRecognize(None, angry_file)

    emotion = c.get_emotion()
    print(emotion)
