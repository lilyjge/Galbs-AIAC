"""
Test server script to receive image data from the camera client and save it as an image file.
"""

import asyncio
import json
import base64

import cv2
import numpy as np
import websockets


def main() -> int:
    """
    Main function to run the test server for the camera module.
    """

    async def handle_client(websocket: websockets.WebSocketServerProtocol) -> None:
        index = 0
        while True:
            data = await websocket.recv()
            print("Received image data")
            payload = json.loads(data)
            img_str = payload["image"]
            img_data = base64.b64decode(img_str)
            img_np = np.frombuffer(img_data, dtype=np.uint8)
            img = cv2.imdecode(img_np, flags=1)
            filename = f"./received_image_{index}.jpg"
            cv2.imwrite(filename, img)
            print(f"Image saved as {filename}")
            index += 1

    async def main_server() -> None:
        async with websockets.serve(handle_client, "localhost", 8765):
            await asyncio.Future()  # Run forever

    asyncio.run(main_server())

    return 0


if __name__ == "__main__":
    result = main()
    if result != 0:
        print(f"ERROR: Status code: {result}")
    print("Server shut down")
