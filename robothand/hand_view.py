# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
import logging
from engine_3d import scene_view
from robothand import hand

LOG = logging.getLogger()


class HandView(scene_view.SceneView):
    # движение курсора
    angles_changed = pyqtSignal(object)

    def __init__(self, parent=None):
        scene_view.SceneView.__init__(self, parent)
        self.hand = hand.Hand()
        self.hand.set_save_state()

    def set_hand_pos(self, pos):
        self.hand.calk_ik_pos(pos)
        self.angles_changed.emit(self.hand.get_angles())

    def on_angle_changed(self, index, value):
        try:
            self.hand.set_angle(index, value)
        except Hand.WrongIndexError as e:
            LOG.debug(e)

    def on_enable_angle_changed(self, index, e):
        self.hand.set_enable_angle(index, e)

    def on_angle_range_changed(self, index, min, max):
        self.hand.set_angle_range_changed(index, min, max)


if __name__ == '__main__':
    from PyQt5 import QtGui
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = HandView()
    mainWin.show()
    sys.exit(app.exec_())
