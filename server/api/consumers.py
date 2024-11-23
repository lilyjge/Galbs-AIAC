import json
import base64
import cv2
import wave
import pyaudio
import soundfile

from channels.generic.websocket import WebsocketConsumer
from output_generation.main import *
from facial_recognition.emotion import analyze_face
from audio_recognition.TranscriptionClient import TranscriptionClient
# from audio_recognition.audio import {...}


class ApiConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # Parse request data
        request = json.loads(text_data)
        if 'command' not in request:
            self.send(text_data=json.dumps({"message": "No command provided."}))
            return
        cmd = request['command']


        # Ping command to check if connection is working
        if cmd == 'ping':
            self.send(text_data=json.dumps({"message": "Connection working."}))


        # Send input command to send input data to the server and initiate the output generation process
        elif cmd == 'send_input':
            # Validate input data
            if 'image_data' not in request:
                self.send(text_data=json.dumps({"message": "No image data provided."}))
                return
            if 'audio_data' not in request:
                self.send(text_data=json.dumps({"message": "No image data provided."}))
                return
            image_data = base64.b64decode(request['image_data'])
            audio_data = base64.b64decode(request['audio_data'])

            # # Save image for testing
            # jpg_og = image_data
            # jpgnp = np.frombuffer(jpg_og, dtype=np.uint8)
            # img = cv2.imdecode(jpgnp, flags=1)
            # cv2.imwrite(f"./test10.jpg", img)

            # Save audio to file for transcription
            CHUNK = 1440
            FORMAT = pyaudio.paInt16
            CHANNELS = 1 
            RATE = 48000
            wf = wave.open("./user_audio.wav", "wb")
            wf.setnchannels(CHANNELS)
            p = pyaudio.PyAudio()
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_data)
            wf.close()

            # Detect emotions from the image
            facial_analysis_results = analyze_face(image_data)

            # Detect audio from the audio data
            user_audio_text = ""
            with open("./user_audio.wav", "rb") as f:
                user_audio_text = TranscriptionClient(f).transcribe()
            print("User audio text:", user_audio_text)

            # Generate response
            response_text = generate_response(user_audio_text, format_emotions(detect_emotions(facial_analysis_results)))
            print("Response text:", response_text)

            # Generate TTS audio file of response
            print("AUDIO: ")
            audio_output_file_name = "output"
            tts(VOICE_ID, response_text, f"{audio_output_file_name}.wav")
            print(f"To {audio_output_file_name}.wav")



            audio_output_file_path = f"output_generation/audio-output-files/{audio_output_file_name}.wav"
            # Read and write the audio file to fix the header
            data, samplerate = soundfile.read(audio_output_file_path)
            soundfile.write(audio_output_file_path, data, samplerate)
            # Read the audio file and convert to base64 json
            with wave.open(f"output_generation/audio-output-files/{audio_output_file_name}.wav") as wf:
                chunk = 1024
                data = wf.readframes(chunk)
                frames = []
                while data != b'':
                    frames.append(data)
                    data = wf.readframes(chunk)
                data = b''.join(frames)
                audio_output_data_base64 = base64.b64encode(data).decode()

            # Motor
            print("MOTOR: ")
            motor_response_data = motor_response(facial_analysis_results)
            print(motor_response_data)

            # Lights
            print("LIGHTS: ")
            lights_response_data = lights_response(facial_analysis_results)
            print(lights_response_data)

            # Send output data to the client
            self.send(text_data=json.dumps({
                "command": "send_output",
                "audio_data": audio_output_data_base64,
                "motor_data": motor_response_data,
                "led_data": lights_response_data
            }))


        # Unrecognized command
        else:
            self.send(text_data=json.dumps({"message": f"Unrecognized command: {cmd}."}))
