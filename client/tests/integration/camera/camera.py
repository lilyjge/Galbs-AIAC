"""
Testing script for the camera module.
"""

import asyncio
import json
import base64
import time

import cv2
import numpy as np
import websockets


def main() -> int:
    """
    Main function to test the camera module.
    """
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    async def send_image(img: np.ndarray, websocket: websockets.WebSocketServerProtocol) -> None:
        _, buffer = cv2.imencode(".jpg", img)
        img_str = base64.b64encode(buffer).decode()
        payload = {"image": img_str}
        data = json.dumps(payload)
        print("Sending image...")
        await websocket.send(data)

    async def run(websocket_uri: str) -> None:
        async with websockets.connect(websocket_uri) as websocket:
            last_mean = 0
            while True:
                time.sleep(1)
                ret, image = cam.read()
                if not ret:
                    print("Failed to capture image")
                    continue
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                mean_diff = np.abs(np.mean(gray) - last_mean)
                if mean_diff > 0.3:
                    await send_image(image, websocket)
                last_mean = np.mean(gray)

    asyncio.run(run("ws://localhost:8765"))

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
