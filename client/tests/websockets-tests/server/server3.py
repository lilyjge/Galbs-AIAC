#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve
import base64
import json
import cv2
import numpy as np


async def hello(websocket):
    index = 0
    while True:
        # if index != 0:
        #     continue
        data = await websocket.recv()
        print("received")
        print(data)
        load = json.loads(data)
        str = load['image']
        jpg_og = base64.b64decode(str)
        jpgnp = np.frombuffer(jpg_og, dtype=np.uint8)
        img = cv2.imdecode(jpgnp, flags=1)
        cv2.imwrite(f"./test{index}.jpg", img)
        index += 1

    # greeting = "received!!"

    # await websocket.send(greeting)
    # print(f">>> {greeting}")

async def main():
    async with serve(hello, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())