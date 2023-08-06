#!/usr/bin/env python3
#     Copyright (C) 2021 Kiteswarms Ltd
#
#     This file is part of pulicast.
#
#     pulicast is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     pulicast is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with pulicast.  If not, see <https://www.gnu.org/licenses/>.

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
