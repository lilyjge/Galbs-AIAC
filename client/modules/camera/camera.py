# Module for interfacing with camera.

import cv2
import time
import numpy as np
import websockets
import base64
import json

class Camera:
    # Camera class.

    def __init__(self, cam_port=0):
        # Initializes the camera with specifications.

        # cam_port: port of the camera

        self.cam_port = cam_port
        self.cam = cv2.VideoCapture(self.cam_port)

    def send_image(self):
        # Encodes and sends image by websocket.c
        
        # img: captured image to be sent (numpy array)
        # websocket: websocket to send images through
        result, image = self.cam.read()
        result, buffer = cv2.imencode('.jpg', image)
        s = base64.b64encode(buffer).decode()
        # load = {'image': s}
        # data = json.dumps(load)
        print("sending")
        return s

    async def run(self, websocket_uri):
        # Every second, check if there was motion and takes and sends picture if there is.
        # websocket_uri: the uri of the websocket to connect with and send images to
        async with websockets.connect(websocket_uri) as websocket:
            last_mean = 0
            while True:
                time.sleep(1)
                result, image = self.cam.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                result = np.abs(np.mean(gray) - last_mean)
                if result > 0.3:
                    await self.send_image(image, websocket)
                last_mean = np.mean(gray)