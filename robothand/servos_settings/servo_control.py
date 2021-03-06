#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import math
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal


class ServoControl(QtWidgets.QGroupBox):
    value_changed = pyqtSignal(int, int)
    angle_changed = pyqtSignal(int, float)
    remove_control = pyqtSignal(object)
    angle_range_changed = pyqtSignal(int, float, float)
    value_range_changed = pyqtSignal(int, int, int)
    range_changed = pyqtSignal(int, object)
    enable_angle_changed = pyqtSignal(int, bool)

    def __init__(self,
                 settings={"min": [0.0, 500], "max": [
                     math.pi, 2500], "index": 1, "value": 500},
                 parent=None):

        super(QtWidgets.QGroupBox, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)
                                [0], "servo_control.ui"), self)
        self.settings = settings
        self.set_index(settings["index"])
        self.addAction(self.action_remove)

        self.horizontalSlider_value.addAction(self.action_set_min_value)
        self.horizontalSlider_value.addAction(self.action_set_max_value)

        self.horizontalSlider_angle.addAction(self.action_set_min_angle)
        self.horizontalSlider_angle.addAction(self.action_set_max_angle)
        self.horizontalSlider_angle.addAction(self.action_reverse)

        self.load_default()

    def set_index(self, index):
        self.index = index
        self.setTitle("ID:{}".format(index))

    def load_default(self):
        # инициализация параметров
        self.spinBox_min_value.blockSignals(True)
        self.spinBox_max_value.blockSignals(True)
        self.doubleSpinBox_min_angle.blockSignals(True)
        self.doubleSpinBox_max_angle.blockSignals(True)

        self.spinBox_min_value.setValue(self.settings["min"][1])
        self.spinBox_max_value.setValue(self.settings["max"][1])

        if self.spinBox_min_value.value() < self.spinBox_max_value.value():
            self.spinBox_value.setMinimum(self.spinBox_min_value.value())
            self.spinBox_value.setMaximum(self.spinBox_max_value.value())
        else:
            self.spinBox_value.setMinimum(self.spinBox_max_value.value())
            self.spinBox_value.setMaximum(self.spinBox_min_value.value())

        self.doubleSpinBox_min_angle.setValue(self.settings["min"][0])
        self.doubleSpinBox_max_angle.setValue(self.settings["max"][0])

        if self.doubleSpinBox_min_angle.value() <\
                self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(
                self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(
                self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(
                self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(
                self.doubleSpinBox_max_angle.value())

        self.spinBox_min_value.blockSignals(False)
        self.spinBox_max_value.blockSignals(False)
        self.doubleSpinBox_min_angle.blockSignals(False)
        self.doubleSpinBox_max_angle.blockSignals(False)
        self.set_value(self.settings["value"])

    @pyqtSlot('bool')
    def on_action_remove_triggered(self, v):
        self.remove_control.emit(self)

    def get_settings(self):
        return {
            "min": [
                self.doubleSpinBox_min_angle.value(),
                self.spinBox_min_value.value()],
            "max": [
                self.doubleSpinBox_max_angle.value(),
                self.spinBox_max_value.value()],
            "index": self.index,
            "value": self.spinBox_value.value()}

    @pyqtSlot('int')
    def on_spinBox_min_value_valueChanged(self, value):
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)

        if self.spinBox_min_value.value() < self.spinBox_max_value.value():
            self.spinBox_value.setMinimum(self.spinBox_min_value.value())
            self.spinBox_value.setMaximum(self.spinBox_max_value.value())
        else:
            self.spinBox_value.setMinimum(self.spinBox_max_value.value())
            self.spinBox_value.setMaximum(self.spinBox_min_value.value())

        self.value_range_changed.emit(
            self.index,
            self.spinBox_min_value.value(),
            self.spinBox_max_value.value())
        self.range_changed.emit(
            self.index, (
                (
                    self.doubleSpinBox_min_angle.value(),
                    self.spinBox_min_value.value()),
                (
                    self.doubleSpinBox_min_angle.value(),
                    self.spinBox_max_value.value())))

        self.set_value(self.spinBox_value.value())
        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)

    @pyqtSlot('int')
    def on_horizontalSlider_value_valueChanged(self, value):
        value = int(
            value / float(self.horizontalSlider_value.maximum()) *
            (self.spinBox_max_value.value() - self.spinBox_min_value.value()) +
            self.spinBox_min_value.value())
        self.set_value(value)

    @pyqtSlot('int')
    def on_spinBox_max_value_valueChanged(self, value):
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)

        if self.spinBox_min_value.value() < self.spinBox_max_value.value():
            self.spinBox_value.setMinimum(self.spinBox_min_value.value())
            self.spinBox_value.setMaximum(self.spinBox_max_value.value())
        else:
            self.spinBox_value.setMinimum(self.spinBox_max_value.value())
            self.spinBox_value.setMaximum(self.spinBox_min_value.value())

        self.value_range_changed.emit(
            self.index,
            self.spinBox_min_value.value(),
            self.spinBox_max_value.value())
        self.range_changed.emit(
            self.index, (
                (
                    self.doubleSpinBox_min_angle.value(),
                    self.spinBox_min_value.value()),
                (
                    self.doubleSpinBox_min_angle.value(),
                    self.spinBox_max_value.value())))

        self.set_value(self.spinBox_value.value())
        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)

    @pyqtSlot('int')
    def on_spinBox_value_valueChanged(self, value):
        self.set_value(value)

    @pyqtSlot('double')
    def on_doubleSpinBox_min_angle_valueChanged(self, value):
        self.doubleSpinBox_angle.blockSignals(True)

        if self.doubleSpinBox_min_angle.value() <\
                self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(
                self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(
                self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(
                self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(
                self.doubleSpinBox_max_angle.value())

        self.angle_range_changed.emit(
            self.index,
            self.doubleSpinBox_min_angle.value(),
            self.doubleSpinBox_max_angle.value())

        self.range_changed.emit(
            self.index, (
                (
                    self.doubleSpinBox_min_angle.value(),
                    self.spinBox_min_value.value()),
                (
                    self.doubleSpinBox_max_angle.value(),
                    self.spinBox_max_value.value())))

        self.set_angle(self.doubleSpinBox_angle.value())
        self.doubleSpinBox_angle.blockSignals(False)

    @pyqtSlot('double')
    def on_doubleSpinBox_max_angle_valueChanged(self, value):
        self.doubleSpinBox_angle.blockSignals(True)

        if self.doubleSpinBox_min_angle.value() <\
                self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(
                self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(
                self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(
                self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(
                self.doubleSpinBox_max_angle.value())

        self.angle_range_changed.emit(
            self.index,
            self.doubleSpinBox_min_angle.value(),
            self.doubleSpinBox_max_angle.value())
        self.range_changed.emit(
            self.index,
            (
                (
                    self.doubleSpinBox_min_angle.value(),
                    self.spinBox_min_value.value()),
                (
                    self.doubleSpinBox_max_angle.value(),
                    self.spinBox_max_value.value())))

        self.set_angle(self.doubleSpinBox_angle.value())
        self.doubleSpinBox_angle.blockSignals(False)

    @pyqtSlot('int')
    def on_horizontalSlider_angle_valueChanged(self, value):
        angle = value / float(self.horizontalSlider_angle.maximum()) * (
            self.doubleSpinBox_max_angle.value() -
            self.doubleSpinBox_min_angle.value()) +\
            self.doubleSpinBox_min_angle.value()

        self.set_angle(angle)

    @pyqtSlot('double')
    def on_doubleSpinBox_angle_valueChanged(self, value):
        self.set_angle(value)

    def set_value(self, value):
        '''Установить значение'''
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        self.doubleSpinBox_angle.blockSignals(True)
        self.horizontalSlider_angle.blockSignals(True)

        # установка значения
        self.spinBox_value.setValue(value)
        norm_value = abs((self.spinBox_min_value.value() - value) / float(
            self.spinBox_max_value.value() - self.spinBox_min_value.value()))

        self.horizontalSlider_value.setValue(
            int(norm_value * self.horizontalSlider_value.maximum()))

        # установка угла
        if self.checkBox_sinch.checkState() == QtCore.Qt.Checked:
            angle = norm_value * (
                self.doubleSpinBox_max_angle.value() -
                self.doubleSpinBox_min_angle.value()) +\
                self.doubleSpinBox_min_angle.value()

            self.doubleSpinBox_angle.setValue(angle)
            self.horizontalSlider_angle.setValue(
                int(norm_value * self.horizontalSlider_angle.maximum()))

        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
        self.doubleSpinBox_angle.blockSignals(False)
        self.horizontalSlider_angle.blockSignals(False)

        self.value_changed.emit(self.index, value)

        if self.checkBox_sinch.checkState() == QtCore.Qt.Checked:
            self.angle_changed.emit(self.index, angle)

    def set_angle(self, angle):
        '''Установить угол'''
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        self.doubleSpinBox_angle.blockSignals(True)
        self.horizontalSlider_angle.blockSignals(True)

        self.doubleSpinBox_angle.setValue(angle)
        norm_value = abs((
            (self.doubleSpinBox_min_angle.value() - angle) /
            float(
                self.doubleSpinBox_max_angle.value() -
                self.doubleSpinBox_min_angle.value())))

        self.horizontalSlider_angle.setValue(
            int(norm_value * self.horizontalSlider_angle.maximum()))

        if self.checkBox_sinch.checkState() == QtCore.Qt.Checked:
            value = norm_value * (
                self.spinBox_max_value.value() -
                self.spinBox_min_value.value()) +\
                self.spinBox_min_value.value()

            self.horizontalSlider_value.setValue(
                norm_value * self.horizontalSlider_value.maximum())
            self.spinBox_value.setValue(value)

        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
        self.doubleSpinBox_angle.blockSignals(False)
        self.horizontalSlider_angle.blockSignals(False)

        if self.checkBox_sinch.checkState() == QtCore.Qt.Checked:
            self.value_changed.emit(self.index, value)

        self.angle_changed.emit(self.index, angle)

    @pyqtSlot('bool')
    def on_action_set_min_angle_triggered(self, v):
        self.doubleSpinBox_min_angle.setValue(self.doubleSpinBox_angle.value())

    @pyqtSlot('bool')
    def on_action_set_max_angle_triggered(self, v):
        self.doubleSpinBox_max_angle.setValue(self.doubleSpinBox_angle.value())

    @pyqtSlot('bool')
    def on_action_reverse_triggered(self, v):
        self.doubleSpinBox_max_angle.blockSignals(True)
        self.doubleSpinBox_min_angle.blockSignals(True)

        max = self.doubleSpinBox_max_angle.value()
        min = self.doubleSpinBox_min_angle.value()

        self.doubleSpinBox_max_angle.setValue(min)
        self.doubleSpinBox_min_angle.setValue(max)

        self.on_doubleSpinBox_min_angle_valueChanged(
            self.doubleSpinBox_min_angle.value())

        self.doubleSpinBox_max_angle.blockSignals(False)
        self.doubleSpinBox_min_angle.blockSignals(False)

    @pyqtSlot('bool')
    def on_action_set_min_value_triggered(self, v):
        self.spinBox_min_value.setValue(self.spinBox_value.value())

    @pyqtSlot('bool')
    def on_action_set_max_value_triggered(self, v):
        self.spinBox_max_value.setValue(self.spinBox_value.value())

    def on_checkBox_sinch_stateChanged(self, v):
        self.enable_angle_changed.emit(self.index, QtCore.Qt.Checked == v)


if __name__ == '__main__':
    import sys
    import logging

    logging.basicConfig(
        format='%(levelname)s %(name)s::%(funcName)s%(message)s',
        level=logging.DEBUG)
    logging.getLogger("PyQt5").setLevel(logging.INFO)

    app = QtWidgets.QApplication(sys.argv)
    widget = ServoControl()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
