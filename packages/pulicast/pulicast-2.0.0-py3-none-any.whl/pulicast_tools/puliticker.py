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
import time
from typing import List

from PySide2.QtGui import QPainter, QResizeEvent, QShowEvent
from PySide2.QtWidgets import QApplication, QGraphicsItemGroup, QGraphicsLineItem, \
    QGraphicsScene, \
    QGraphicsTextItem, \
    QGraphicsView

from pulicast import QtNode
from pulicast_tools.puliconf.zcm_utils import zcom_to_dict

starttime = time.time()


def msg_to_string(msg):
    msg_as_dict = zcom_to_dict(msg)
    del msg_as_dict["__msg_type__"]
    return str(msg_as_dict)


class MessageItem(QGraphicsTextItem):
    def __init__(self, message, parent):
        QGraphicsTextItem.__init__(self, msg_to_string(message), parent)
        self.ts = time.time()
        self.setToolTip(str(self.ts))
        self.setY((self.ts - starttime) * 500)

# class CrosshairItem(QGraphicsItemGroup):
#     def __init__(self):
#         QGraphicsItemGroup.__init__(self)
#         self._hline = QGraphicsLineItem()
#         self._vline = QGraphicsLineItem()
#         self.addToGroup(self._hline)
#         self.addToGroup(self._vline)
#
#     def setToMouseCoords(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
#         mouse_pos = event.scenePos()
#
#
#
#         self._hline.setLine(QLine(-1e7, mouse_pos.y(), 1e7, mouse_pos.y()))
#         self._vline.setLine(QLine(mouse_pos.x(), 1e7, mouse_pos.x(), -1e7))

class MessageStream(QGraphicsItemGroup):
    def __init__(self):
        QGraphicsItemGroup.__init__(self)
        self._message_items: List[MessageItem] = list()

    def addMessage(self, message):
        item = MessageItem(message, self)

        self._message_items.append(item)

        if len(self._message_items) > 1:
            prev_item = self._message_items[-2]
            start = prev_item.pos()
            start.setY(start.y() + prev_item.boundingRect().height())
            end = item.pos()
            litem = QGraphicsLineItem(start.x(), start.y(), end.x(), end.y(), self)
            litem.setToolTip(str(item.ts - prev_item.ts))

class PuliTicker(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.viewport()
        scene = QGraphicsScene()
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)

    def resizeEvent(self, event: QResizeEvent):
        self.fit_scene_into_view()

    def showEvent(self, event: QShowEvent):
        self.fit_scene_into_view()

    def fit_scene_into_view(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        # self.setSceneRect(self.scene().itemsBoundingRect())
        # self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication()

    node = QtNode("puliticker")
    view = PuliTicker()

    def setup_stream(channel, offset):
        message_stream = MessageStream()
        message_stream.setX(offset)

        def on_new_msg(msg):
            print(msg)
            message_stream.addMessage(msg)
            view.fit_scene_into_view()
        node[channel].subscribe(on_new_msg)
        view.scene().addItem(message_stream)

    node["__ndoes"].subscribe(lambda msg: None)  # Just to mark this one as a debug tool
    setup_stream("names/.config/function_name", 0)
    setup_stream("names/.config/function_name.r", 0)
    view.show()

    app.exec_()