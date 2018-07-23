#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import threading
import sys
import queue as Queue
import logging
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from robothand.protocol.hand_protocol import HandProtocol
from engine_3d import vector
import time
import serial


LOG = logging.getLogger(__name__)


class Configurator(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(
            __file__)[0], "configurator.ui"), self)
        self.save_state_thread = None
        self.settings = self.groupBox_settings.settings
        self.groupBox_settings.angle_changed.connect(
            self.scene_view.on_angle_changed)
        self.groupBox_settings.enable_angle_changed.connect(
            self.scene_view.on_enable_angle_changed)
        self.groupBox_settings.angle_range_changed.connect(
            self.scene_view.on_angle_range_changed)
        self.scene_view.cursor_move.connect(self.on_cursor_move)

        self.groupBox_settings.range_changed.connect(self.on_range_changed)
        self.groupBox_settings.value_changed.connect(self.on_value_changed)
        self.scene_view.angles_changed.connect(
            self.groupBox_settings.on_angles_changed)

        self.lineEdit_port_name.setText(
            self.settings.value("port_name", '27'))
        self.controll_thread = None
        self.proto = None

        for index, limmit in\
                self.groupBox_settings.get_protocol_settings().items():
            self.scene_view.hand.set_angle_range_changed(
                index, limmit[0][0], limmit[1][0])

        self.scene_view.hand.set_save_state()
        self.scene_view.sphere.pos = vector.Vector(0, -130, 130)

    def closeEvent(self, event):
        self.scene_view.timer.stop()
        # event.accept()

    @pyqtSlot()
    def on_lineEdit_port_name_editingFinished(self):
        self.settings.setValue("port_name", self.lineEdit_port_name.text())

    def on_range_changed(self, index, value):
        if self.proto is not None:
            self.proto.set_limmit(index, value)

    def on_value_changed(self, index, value):
        if self.proto is not None and not self.get_enable_angle(index):
            self.scene_view.hand.cmd_queue.put((2, (index, value)))

    def get_enable_angle(self, index):
        return self.scene_view.hand.get_enable_angle(index)

    @pyqtSlot(bool)
    def on_pushButton_connect_clicked(self, v):
        '''Подключим руку'''

        if self.controll_thread is None:
            try:
                self.proto = HandProtocol(port=str(
                    self.lineEdit_port_name.text()), baudrate=128000)
                for index, limmit in\
                        self.groupBox_settings.get_protocol_settings().items():
                    self.proto.set_limmit(index, limmit)
                    self.scene_view.hand.set_angle_range_changed(
                        index, limmit[0][0], limmit[1][0])

                self.lineEdit_port_name.setEnabled(False)
                self.scene_view.hand.cmd_queue = Queue.Queue()
                self.controll_thread = threading.Thread(target=self.proto_proc)
                self.controll_thread.start()
                self.pushButton_connect.setText(u'Отключить')
            except serial.serialutil.SerialException as e:
                QtWidgets.QMessageBox.warning(self, "Cannot open port", str(e))
        else:
            self.lineEdit_port_name.setEnabled(True)
            self.scene_view.hand.cmd_queue.put(None)
            self.controll_thread.join()
            self.scene_view.hand.cmd_queue = None
            self.controll_thread = None
            self.proto.close()
            self.pushButton_connect.setText(u'Подключить')

    def proto_proc(self):
        '''Обработка комманд'''
        while 1:
            try:
                data = self.scene_view.hand.cmd_queue.get()

                if data is None:
                    return
                cmd, data = data

                if cmd == 0:
                    self.proto.rotate(*data)
                elif cmd == 1:
                    self.proto.move_hand(data)
                elif cmd == 2:
                    # управление только при разблокировки
                    self.proto.move_servo(data[0], data[1], 0.1)
            except Exception as e:
                LOG.warning(e)

    def on_cursor_move(self, camera, cur_pos, state):
        if state == 0:
            self.plain_pos = vector.Vector(self.scene_view.sphere.pos)
        # плоскость x
        if self.radioButton_plain_x.isChecked():
            plain = (vector.Vector(1, 0, 0), self.plain_pos)
            pos = camera.get_point_on_plain(cur_pos, plain)
        elif self.radioButton_plain_y.isChecked():
            plain = (vector.Vector(0, 1, 0), self.plain_pos)
            pos = camera.get_point_on_plain(cur_pos, plain)
        elif self.radioButton_plain_z.isChecked():
            plain = (vector.Vector(0, 0, 1), self.plain_pos)
            pos = camera.get_point_on_plain(cur_pos, plain)
        else:
            plain = (camera.get_plain()[0], self.plain_pos)
            pos = camera.get_point_on_plain(cur_pos, plain)

        # начало смещения
        if state == 0:
            self.offset = self.plain_pos - pos
        new_pos = pos + self.offset

        if not self.checkBox_o_x.isChecked():
            new_pos[0] = self.plain_pos[0]

        if not self.checkBox_o_y.isChecked():
            new_pos[1] = self.plain_pos[1]

        if not self.checkBox_o_z.isChecked():
            new_pos[2] = self.plain_pos[2]

        self.scene_view.sphere.pos = new_pos

        # кинематика
        if self.checkBox_kinematic.isChecked():
            self.scene_view.set_hand_pos(new_pos)

    @pyqtSlot(bool)
    def on_pushButton_reset_hand_clicked(self, v):
        if not self.save_state_thread:
            self.scene_view.sphere.pos = vector.Vector(0, -130, 130)
            self.save_state_thread = threading.Thread(
                target=self.save_state_thread_proc)
            self.save_state_thread.start()

    def save_state_thread_proc(self):
        start_angles = self.scene_view.hand.get_angles()
        dt = 0.05
        count = int(1.0 / dt * 2.5)

        steps = [
            (end[1] - start[1]) / count
            for start, end in zip(
                start_angles, self.scene_view.hand.save_state)]
        LOG.debug('dt: %s start_angles: %s count: %s steps: %s' % (
            dt, start_angles, count, steps))

        i = 1
        while (i < count):
            for start_angle, step in zip(start_angles, steps):
                self.scene_view.hand.set_angle(
                    start_angle[0], start_angle[1] + step * i)
            time.sleep(dt)
            i += 1
        self.save_state_thread = None


def main():
    logging.basicConfig(
        format='%(levelname)s %(name)s::%(funcName)s %(message)s',
        level=logging.DEBUG)
    logging.getLogger("PyQt5").setLevel(logging.INFO)

    app = QtWidgets.QApplication(sys.argv)
    widget = Configurator()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
