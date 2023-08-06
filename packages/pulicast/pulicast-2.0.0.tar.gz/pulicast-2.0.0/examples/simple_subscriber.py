# !/bin/python3
# Copyright (C) 2020 Kiteswarms GmbH - All Rights Reserved
#
# simple_subscriber.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com
import trio

from pulicast import TrioNode, Address


async def main():
    async with trio.open_nursery() as nursery:
        node = TrioNode("simple_subscriber", nursery)

        def msg_handler(msg: str, source: Address, lead: int):
            print(f"{source.port}: {msg}\t{lead}")

        node["my_test_channel"].subscribe(msg_handler)


if __name__ == '__main__':
    trio.run(main)
