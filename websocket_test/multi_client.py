from websocket import WebSocketApp
import ssl, json, concurrent.futures
import ssl, json
from threading import Thread

from time import sleep, time
from random import randrange

from .args import parse_args


PACKET = {
    "ts": 1501665144,
    "idx": 0,
    "data": "1" * 60
}

PACKET_SIZE = 100


def raw_data_json(idx):
    data = PACKET.copy()
    data["idx"] = idx
    data["ts"] = int(time() * 1000)
    return json.dumps(data)

def raw_data(idx):
    t = int(time() * 1000).to_bytes(8, 'big')
    return t + idx.to_bytes(1, 'big') * (PACKET_SIZE - len(t))

def on_open(ws):
    # Wait for a while to simulate box will not connect at same time.
    sleep(randrange(0, 1000) / 1000)
    count = 0
    # Endless
    while True:
        idx = ws.idx

        if ws.is_json:
            d = raw_data_json(idx)
            ws.send(d)
        else:
            d = raw_data(idx)
            ws.sock.send_binary(d)

        ws.idx = idx + 1 if (idx + 1) <= 0xFF else 0

        if ws.has_log:
            print(ws.display_name, "sent with idx ", idx)

        count += 1
        if count >= ws.amount:
            print(ws.display_name, "stopped, reach amount:", ws.amount)
            ws.close()
            break

        sleep(ws.inv)

def on_message(ws, message):
    print(ws.name, message)

def on_error(ws, error):
    print(error)

def run_boy(name, url, inv, is_json, has_log, amount):
    ws = WebSocketApp(url)
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_error = on_error
    ws.display_name = name
    ws.idx = 0
    ws.inv = inv
    ws.is_json = is_json
    ws.has_log = has_log
    ws.amount = amount

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def main():
    cmds = parse_args()
    num = cmds.clients
    url = "{0}://{1}".format("ws" if cmds.ws else 'wss', cmds.url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num) as executor:
        for idx in range(0, num):
            tt = executor.submit(run_boy, "Box{0}".format(idx), url, cmds.t, cmds.json, cmds.log, cmds.a)

if __name__ == '__main__':
    main()
