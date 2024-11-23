import requests
from API_KEY import ELEVENLABS_API_KEY

ID = "9BWtsMINqrJLrRacOk9x"
TEXT = "Congratulations on your promotion! I'm beyond thrilled for you! You must be feeling on top of the world right now! That's amazing news, and you totally deserve it! Your hard work and dedication have paid off, and I'm so happy to see you achieving your goals. You should definitely celebrate with your friends - you've earned it! What are your plans to mark this special occasion? Are you going out for drinks, dinner, or maybe a weekend getaway?"  # Text you want to convert to speech

headers = {
    "Accept": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}

data = {
    "text": TEXT,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True
    }
}

response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/{ID}/stream", headers=headers, json=data, stream=True)

with open("output.mp3", "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):
        file.write(chunk)