import asyncio
import datetime
import hashlib
import os
import time
import traceback
import websockets
import pickle
import os

host = input("Enter host ip: ")

async def hello():
    clear_command = {
    "nt": "cls",
    "posix": "clear"
    }
    while True:
        try:
            uri = f"ws://{host}:8765"
            async with websockets.connect(uri) as websocket:
                while True:
                    message = hashlib.sha256(bytes(str(time.mktime(datetime.datetime.now().utctimetuple())).encode("utf-8"))).hexdigest()
                    await websocket.send(message)
                    
                    os.system(clear_command[os.name])
                    feedback = await websocket.recv()
                    data = pickle.loads(feedback)
                    print(f"<<< {data['payload']}")
                    await asyncio.sleep(data['wait_time'])
        except ConnectionRefusedError:
            print("Could not find an active server! Retrying connection in 5 seconds...")
            await asyncio.sleep(5)
        except websockets.exceptions.ConnectionClosedError:
            print("Server closed! Retrying connection in 5 seconds...")
        except KeyboardInterrupt:
            print("Exiting program.")
            exit()
        except websockets.exceptions.InvalidURI:
            print("Invalid URL!")
            host = input("Enter new host ip: ")
        except:
            print("Unknown error occurred! Retrying connection in 5 seconds...")
            with open("logs.txt", "w") as handle:
                traceback.print_exc(file=handle)
                handle.write(datetime.datetime.now())
            await asyncio.sleep(10)

        

if __name__ == "__main__":
    asyncio.run(hello())
