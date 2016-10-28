# -*- coding: utf-8 -*-
from engine.scene_view import SceneView
from hand import Hand
from PyQt4.QtCore import pyqtSlot, pyqtSignal


class HandView(SceneView):
    # движение курсора
    angles_changed = pyqtSignal(object)

    def __init__(self, parent=None):
        SceneView.__init__(self, parent)
        self.hand = Hand()
        self.hand.set_save_state()

    def set_hand_pos(self, pos):
        self.hand.calk_ik_pos(pos)
        self.angles_changed.emit(self.hand.get_angles())

    def on_angle_changed(self, index, value):
        self.hand.set_angle(index, value)

    def on_enable_angle_changed(self, index, e):
        self.hand.set_enable_angle(index, e)

    def on_angle_range_changed(self, index, min, max):
        self.hand.set_angle_range_changed(index, min, max)


if __name__ == '__main__':
    from PyQt4 import QtGui
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = HandView()
    mainWin.show()
    sys.exit(app.exec_())
