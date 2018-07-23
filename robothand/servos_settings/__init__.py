#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import sys
import logging
import math
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from robothand.servos_settings import servo_control
from robothand.servos_settings import create_servo_dialog

logger = logging.getLogger(__name__)


class ServosSettings(QtWidgets.QGroupBox):
    value_changed = pyqtSignal(int, int)
    angle_changed = pyqtSignal(int, float)
    angle_range_changed = pyqtSignal(int, float, float)
    value_range_changed = pyqtSignal(int, int, int)
    enable_angle_changed = pyqtSignal(int, bool)
    range_changed = pyqtSignal(int, object)

    def __init__(
            self, parent=None,
            settings=QtCore.QSettings("AlexLexx", "robot_hand")):
        super(QtWidgets.QGroupBox, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)
                                [0], "servos_settings.ui"), self)
        self.settings = settings
        self.scrollArea.addAction(self.action_add_servo)
        self.controlls = []
        self.controlls_map = {}

        self.open_settings(self.settings.value("last_file", ''))

    def on_angles_changed(self, data):
        for index, angle in data:
            if index in self.controlls_map:
                controll = self.controlls_map[index]
                controll.blockSignals(True)
                controll.set_angle(angle)
                controll.blockSignals(False)

    def get_servo_ids(self):
        return [c.index for c in self.controlls]

    def get_protocol_settings(self):
        res = {}

        for c in self.controlls:
            settings = c.get_settings()
            res[settings["index"]] = (settings["min"], settings["max"])
        return res

    @pyqtSlot('bool')
    def on_action_add_servo_triggered(self, v):
        dialog = create_servo_dialog.CreateServoDialog(self.get_servo_ids())

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            control_settings = {"min": [0.0, 500], "max": [
                math.pi, 2500], "index": dialog.get_id(), "value": 500}
            self.add_control(control_settings)

    def add_control(self, control_settings):
        controll = servo_control.ServoControl(control_settings)
        controll.value_changed.connect(self.value_changed)
        controll.angle_changed.connect(self.angle_changed)
        controll.angle_range_changed.connect(self.angle_range_changed)
        controll.value_range_changed.connect(self.value_range_changed)
        controll.enable_angle_changed.connect(self.enable_angle_changed)
        controll.range_changed.connect(self.range_changed)

        self.controlls_map[controll.index] = controll
        self.controlls.append(controll)
        controll.remove_control.connect(self.remove_control)
        self.verticalLayout.insertWidget(
            self.verticalLayout.count() - 1, controll)

    def remove_control(self, controll):
        self.verticalLayout.removeWidget(controll)
        self.controlls.remove(controll)

        controll.value_changed.disconnect(self.value_changed)
        controll.angle_changed.disconnect(self.angle_changed)
        controll.angle_range_changed.disconnect(self.angle_range_changed)
        controll.value_range_changed.disconnect(self.value_range_changed)
        controll.enable_angle_changed.disconnect(self.enable_angle_changed)
        controll.range_changed.connect(self.range_changed)

        del self.controlls_map[controll.index]
        controll.hide()

    @pyqtSlot('bool')
    def on_pushButton_save_settings_clicked(self, v):
        file_name = QtWidgets.QFileDialog.getSaveFileName(
            self, u"Сохраним файл",
            self.settings.value("last_file").toString(), "Settings (*.json)")

        if len(file_name):
            self.lineEdit_file.setText(file_name)
            self.settings.setValue("last_file", file_name)
            open(file_name, "wb").write(json.dumps(
                [c.get_settings() for c in self.controlls]))

    @pyqtSlot('bool')
    def on_pushButton_open_settings_clicked(self, v):
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self, u"Открыть настройки",
            self.settings.value("last_file").toString(), "Settings (*.json)")
        self.open_settings(file_name)

    def open_settings(self, file_name):
        if len(file_name):
            self.lineEdit_file.setText(file_name)
            self.settings.setValue("last_file", file_name)

            # чистим контролы
            while len(self.controlls):
                self.remove_control(self.controlls[0])
            try:
                for c_s in json.loads(open(file_name, "rb").read()):
                    self.add_control(c_s)
            except IOError as e:
                logger.warning(e)


if __name__ == '__main__':
    import logging
    logging.basicConfig(
        format='%(levelname)s %(name)s::%(funcName)s%(message)s',
        level=logging.DEBUG)
    logging.getLogger("PyQt5").setLevel(logging.INFO)

    app = QtWidgets.QApplication(sys.argv)
    widget = ServosSettings()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
