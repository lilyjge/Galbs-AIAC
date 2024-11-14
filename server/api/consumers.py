import json
import base64

from channels.generic.websocket import WebsocketConsumer
from output_generation.main import *
from facial_recognition.emotion import analyze_face
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

            # Detect emotions from the image
            facial_analysis_results = analyze_face(image_data)

            # Detect audio from the audio data
            # TODO: integrate audio input module. Dummy data for now.
            audio_text = "Today has been quite rough, I just want to go home and sleep."

            # Generate response
            response_text = generate_response(audio_text, format_emotions(detect_emotions(facial_analysis_results)))
            print("Response text:", response_text)

            # Generate TTS audio file of response
            print("AUDIO: ")
            audio_output_file_name = "output"
            tts(VOICE_ID, response_text, f"{audio_output_file_name}.mp3")
            print(f"To {audio_output_file_name}.mp3")

            # Read the audio file and convert to base64 json
            with open(f"output_generation/audio-output-files/{audio_output_file_name}.mp3", 'rb') as f:
                audio_output_data = f.read()
                audio_output_data_base64 = base64.b64encode(audio_output_data).decode('utf-8')

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
