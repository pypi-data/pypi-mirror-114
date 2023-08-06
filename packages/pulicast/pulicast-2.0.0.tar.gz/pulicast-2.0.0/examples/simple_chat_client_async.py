# !/bin/python3
# Copyright (C) 2020 Kiteswarms GmbH - All Rights Reserved
#
# simple_chat_client_async.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com

import trio

from pulicast import TrioNode, Address


async def main():

    async with trio.open_nursery() as nursery:
        node = TrioNode("chatter", nursery)

        def msg_handler(msg: str, source: Address, lead: int):
            print(f"{source.port}: {msg}\t{lead}")

        node["channel_1"].subscribe(msg_handler)

        while True:
            node['channel_1'] << await trio.to_thread.run_sync(input, "Input Message: ")

if __name__ == '__main__':
    trio.run(main)


