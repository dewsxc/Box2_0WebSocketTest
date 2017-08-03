from websocket import WebSocketApp
import ssl, json, concurrent.futures

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
    t = int(time() * 1000).to_bytes(6, 'big')
    return t + idx.to_bytes(1, 'big') * (PACKET_SIZE - len(t))

def on_open(ws):
    # Wait for a while to simulate box will not connect at same time.
    sleep(randrange(0, 1000) / 1000)

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
            print(ws.name, "sent with idx ", idx)
        sleep(ws.inv)

def on_message(ws, message):
    print(ws.name, message)

def on_error(ws, error):
    print(error)

def run_boy(name, url, inv, is_json, has_log):
    ws = WebSocketApp(url)
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_error = on_error
    ws.name = name
    ws.idx = 0
    ws.inv = inv
    ws.is_json = is_json
    ws.has_log = has_log

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def main():
    cmds = parse_args()
    num = cmds.amount
    url = "{0}://{1}:{2}".format("ws" if cmds.ws else 'wss', cmds.addr, cmds.port)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num) as executor:
        for idx in range(0, num):
            executor.submit(run_boy, "Box{0}".format(idx), url, cmds.t, cmds.json, cmds.log)


if __name__ == '__main__':
    main()
