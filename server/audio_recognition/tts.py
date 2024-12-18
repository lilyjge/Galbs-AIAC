# returns text to speech contents for a file

from google.cloud import texttospeech


def text_to_speech_from_file(input_file, output_audio_file):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Read text from the input file
    with open(input_file, "r") as file:
        text = file.read()

    # Set up text input and synthesis configuration
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Perform text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the output to an audio file
    with open(output_audio_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to '{output_audio_file}'")


# Usage
text_to_speech_from_file("input_text.txt", "output_audio.mp3")
