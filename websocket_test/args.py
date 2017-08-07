import argparse

parser = argparse.ArgumentParser(prog='WebSocket Test Script')

parser.add_argument('amount', type=int, help='How many client you needs to start?')
parser.add_argument('url', type=str, help='Sever url include host, port, subprotocols.')
parser.add_argument('-ws', action='store_true', help="No TLS.")
parser.add_argument('-t', type=float, default=0.5, help='Interval between two data, in second.')
parser.add_argument('-json', action='store_true', help='Clients will send json format.')
parser.add_argument('-log', action='store_true', help='Show log at command line.')

def parse_args():
    return parser.parse_args()

if __name__ == '__main__':
    print(parser.parse_args())
