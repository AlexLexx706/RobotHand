#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot


class CreateServoDialog(QtWidgets.QDialog):
    def __init__(self, exist_servo_list, parent=None):
        super(QtWidgets.QDialog, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)
                                [0], "create_servo_dialog.ui"), self)
        self.exist_servo_list = exist_servo_list
        self.before = 0

        if len(exist_servo_list) == self.spinBox_id.maximum():
            self.spinBox_id.setDisabled(True)

        self.on_spinBox_id_valueChanged(1)

    def get_id(self):
        return self.spinBox_id.value()

    @pyqtSlot('int')
    def on_spinBox_id_valueChanged(self, v):
        self.blockSignals(True)
        step = 0

        if self.before < v:
            while v in self.exist_servo_list and step < 32:
                v += 1
                v %= 33

                if v == 0:
                    v = 1
                step += 1
        else:
            while v in self.exist_servo_list and step < 32:
                v -= 1

                if v <= 0:
                    v = 32
                step += 1

        self.spinBox_id.setValue(v)
        self.before = v
        self.blockSignals(False)


if __name__ == '__main__':
    import sys
    import logging

    logging.basicConfig(
        format='%(levelname)s %(name)s::%(funcName)s%(message)s',
        level=logging.DEBUG)
    logging.getLogger("PyQt5").setLevel(logging.INFO)

    app = QtWidgets.QApplication(sys.argv)
    widget = CreateServoDialog([1, 2, 3, 4, 8, 12])
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
