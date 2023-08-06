# !/bin/python3
# Copyright (C) 2020 Kiteswarms GmbH - All Rights Reserved
#
# qt_chat_client.py
#
# Maximilian Ernestus    [maximilian@kiteswarms.com]
#
# https://www.kiteswarms.com

from PySide2.QtCore import Qt

from pulicast import Address
from pulicast.pulicast_qt import QtNode
from PySide2.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QWidget, QLabel


def main():
    app = QApplication()
    window = QWidget()
    layout = QVBoxLayout()
    display_field = QLabel()
    display_field.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
    layout.addWidget(display_field)
    entry_field = QLineEdit()
    layout.addWidget(entry_field)
    window.setLayout(layout)

    node = QtNode("qt_chatter")

    def msg_handler(msg: str, source: Address):
        display_field.setText(f"{display_field.text()}\n{source.port}: {msg}")

    node["channel_1"].subscribe(msg_handler)

    def send_stuff():
        node["channel_1"] << entry_field.text()
        entry_field.clear()

    entry_field.returnPressed.connect(send_stuff)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
