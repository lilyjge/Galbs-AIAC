import cv2
import time
import numpy as np
import websockets
import base64
import json
import asyncio

cam_port = 0
cam = cv2.VideoCapture(cam_port)

async def send_image(img, websocket):
    result, buffer = cv2.imencode('.jpg', img)
    s = base64.b64encode(buffer).decode()
    load = {'image': s}
    data = json.dumps(load)
    print("sending")
    await websocket.send(data)

async def run(websocket_uri):
    async with websockets.connect(websocket_uri) as websocket:
        last_mean = 0
        while True:
            time.sleep(1)
            result, image = cam.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result = np.abs(np.mean(gray) - last_mean)
            if result > 0.3:
                await send_image(image, websocket)
            last_mean = np.mean(gray)

asyncio.run(run("ws://localhost:8765"))