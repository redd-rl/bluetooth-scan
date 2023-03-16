import asyncio
import datetime
import hashlib
import time
import websockets
import sys
import pickle

wait_time = sys.argv[1]
async def hello(websocket, the_magic_slash_that_occurs_for_some_reason_and_i_thought_it_was_funny_so_i_am_keeping_it):
    async for message in websocket:
        
        with open("output.txt", "r") as handle:
            if message == hashlib.sha256(bytes(str(time.mktime(datetime.datetime.now().utctimetuple())).encode("utf-8"))).hexdigest():
                serialized = pickle.dumps({
                    "payload": "\n" + handle.read(),
                    "wait_time": int(wait_time) / 1000
                    })
                await websocket.send(serialized)
            elif message == "name":
                await websocket.send("Your version is out of date! Get the latest version here: https://github.com/redd-rl/bluetooth-scan")
            else:
                await websocket.send("Hello client user!\n" + handle.read())

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())