# Module for interfacing with camera.

import cv2
import base64

class Camera:
    # Camera class.

    def __init__(self, cam_port=0):
        """
        Initializes the camera with specifications.

        cam_port: port of the camera
        """

        self.cam_port = cam_port
        self.cam = cv2.VideoCapture(self.cam_port)

    def send_image(self):
        """
        Takes image and return base64 encoded data of image.
        """
        result, image = self.cam.read()
        result, buffer = cv2.imencode('.jpg', image)
        s = base64.b64encode(buffer).decode()
        print("sending image")
        return s