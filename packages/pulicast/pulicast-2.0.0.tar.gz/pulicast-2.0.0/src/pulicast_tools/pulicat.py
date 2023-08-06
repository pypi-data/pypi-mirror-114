# !/bin/python3
# Copyright (C) 2021 Kiteswarms GmbH - All Rights Reserved
#
# pulicat.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com
import argparse
import datetime
import logging
from pprint import pprint

from PySide2.QtWidgets import QApplication

import pulicast
from pulicast import QtNode
from pulicast_tools.puliconf.zcm_utils import zcom_to_dict


def print_msg(msg, indent=""):
    for field in msg.__slots__:
        val = getattr(msg, field)
        if hasattr(val, "__slots__"):
            print_msg(val, indent + "  ")
        elif isinstance(val, (list, tuple)):
            print(f"{indent}{field}:")
            for elem in val:
                print_msg(elem, indent + "  ")
        else:
            print(f"{indent}{field}: {getattr(msg, field)}")




def main():
    parser = argparse.ArgumentParser(description="A tool to print the messages arriving at a single pulicast channel")
    parser.add_argument("-p", "--port", type=int, default=pulicast.DEFAULT_PORT, help="The pulicast port to listen on.")
    parser.add_argument("channel", type=str, help="The channel to print.")

    args = parser.parse_args()
    app = QApplication()
    node = QtNode("pulicat", args.port)
    logger = logging.getLogger(args.channel)

    def print_msg(msg):
        print("HI")
        msg_dict = zcom_to_dict(msg)
        del msg_dict["__msg_type__"]
        pprint((datetime.datetime.now(), args.channel, msg_dict), width=200, compact=True)
    print("Subscribign to", node[args.channel].name)
    node[args.channel].subscribe(print_msg)

    app.exec_()


if __name__ == '__main__':
    main()