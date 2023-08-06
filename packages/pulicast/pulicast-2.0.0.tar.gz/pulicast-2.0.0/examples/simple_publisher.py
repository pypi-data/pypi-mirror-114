# !/bin/python3
# Copyright (C) 2020 Kiteswarms GmbH - All Rights Reserved
#
# simple_publisher.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com
import trio

from pulicast import TrioNode


async def main():
    async with trio.open_nursery() as nursery:
        node = TrioNode("simple_publisher", nursery)

        node["my_test_channel"] << await trio.to_thread.run_sync(input, "Input Message: ")

        node.stop()


if __name__ == '__main__':
    trio.run(main)
