"""
Module for interfacing with camera.
"""

import base64

import cv2


class Camera:
    """
    Camera class.
    """

    def __init__(self, cam_port: int = 0) -> None:
        """
        Initializes the camera with specifications.

        cam_port: Camera port.
        """

        self.cam_port = cam_port
        self.cam = cv2.VideoCapture(self.cam_port)

    def send_image(self) -> str:
        """
        Takes image and return base64 encoded data of image.
        """
        _, image = self.cam.read()
        _, buffer = cv2.imencode(".jpg", image)
        s = base64.b64encode(buffer).decode()
        print("sending image")
        return s
