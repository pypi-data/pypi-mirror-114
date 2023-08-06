# !/bin/python3
# Copyright (C) 2020 Kiteswarms GmbH - All Rights Reserved
#
# simple_chat_client_async.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com
from pulicast import ThreadedNode, Address


def main():

    node = ThreadedNode("chatter")
    node.start()

    def msg_handler(msg: str, source: Address, lead: int):
        print(f"{source.port}: {msg}\t{lead}")

    node["channel_1"].subscribe(msg_handler)

    while True:
        node['channel_1'] << input("Input Message: ")


if __name__ == '__main__':
    main()


