# Box2.0 WebSocket Test

This widget will keep sending data to given server with connections you set.

In default:

1. Use protocol TLS, 'wss' and will ignore TLS verification.
2. Clients will send binary packet.
3. Each client will send one data every 0.5s.

## Requirement

1. Python 3.4
2. Websocket-client

## Installation

Pull project and enter project directory, install with pip.

```shell
$ pip3 install .
```

## Package

Binary packet will be (100 bytes):

```c
[Timestampe 4bytes] + [Counting from 0-255] * 96
```

Timestamp(ms): `1501737366011` Counting at `6`

```c
b'\x01]\xa6\x85\xb1\xfb\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'
```

Json packet (JsonString) will be (over 100 bytes):

```json
{
    "ts": <Timestamp(ms)>,
    "idx": <Counting>,
    "data": "1" * 60
}
```

```json
{
	"ts": 1501726789,
	"idx": 19,
	"data": "111111111111111111111111111111111111111111111111111111111111"
}
```



## Usage

Run:

```shell
$ wbt <ClientsNumber> <ServerIP> <ServerPort>
```

10 clients:

```shell
$ wbt 10 localhost 8765
```

Connect with protocol 'ws'

```shell
$ wbt 10 localhost 8765 -ws
```

Each client send data with interval 0.1s

```shell
$ wbt 10 localhost 8765 -t 0.1
```

Send will json format:

```shell
$ wbt 10 localhost 8765 -json
```
