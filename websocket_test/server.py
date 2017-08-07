#!/usr/bin/env python3

import asyncio
import websockets
import ssl

async def hello(websocket, path):

    while True:
        m = await websocket.recv()
        print(m)


sc = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# sc.check_hostname = False
# sc.verify_mode = ssl.CERT_NONE
sc.load_cert_chain('./server.pem', './server.key')

start_server = websockets.serve(hello, 'localhost/123', 8765, ssl=sc)
# start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
