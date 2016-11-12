#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import threading
import Queue
import logging
import sys
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot
from robothand.protocol.hand_protocol import HandProtocol
from robothand.engine import vector

LOG = logging.getLogger(__name__)


class Configurator(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(
            __file__)[0], "configurator.ui"), self)
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
            self.settings.value("port_name", '27').toString())
        self.controll_thread = None
        self.proto = None
        self.on_pushButton_reset_hand_clicked(1)

    def closeEvent(self, event):
        self.scene_view.timer.stop()
        # event.accept()

    @pyqtSlot()
    def on_lineEdit_port_name_editingFinished(self):
        self.settings.setValue("port_name", self.lineEdit_port_name.text())

    def on_range_changed(self, index, value):
        if self.proto is not None:
            print "on_range_changed", index, value
            self.proto.set_limmit(index, value)

    def on_value_changed(self, index, value):
        print "on_value_changed", index, value, self.get_enable_angle(index), self.proto is not None

        if self.proto is not None and not self.get_enable_angle(index):
            self.scene_view.hand.cmd_queue.put((2, (index, value)))

    def get_enable_angle(self, index):
        return self.scene_view.hand.get_enable_angle(index)

    @pyqtSlot(bool)
    def on_pushButton_connect_clicked(self, v):
        '''Подключим руку'''

        if self.controll_thread is None:
            self.proto = HandProtocol(port=str(
                self.lineEdit_port_name.text()), baudrate=128000)
            limmits = self.groupBox_settings.get_protocol_settings()

            for index in limmits:
                self.proto.set_limmit(index, limmits[index])

            self.lineEdit_port_name.setEnabled(False)
            self.scene_view.hand.cmd_queue = Queue.Queue()
            self.controll_thread = threading.Thread(target=self.proto_proc)
            self.controll_thread.start()
            self.pushButton_connect.setText(u'Отключить')
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
                print 'SASASAMBA: ', data[0], data[1], 0.1
                self.proto.move_servo(data[0], data[1], 0.1)

    def on_cursor_move(self, camera, cur_pos, state):
        if state == 0:
            self.plain_pos = vector(self.scene_view.sphere.pos)
        # плоскость x
        if self.radioButton_plain_x.isChecked():
            plain = (vector(1, 0, 0), self.plain_pos)
            pos = camera.get_point_on_plain(cur_pos, plain)
        elif self.radioButton_plain_y.isChecked():
            plain = (vector(0, 1, 0), self.plain_pos)
            pos = camera.get_point_on_plain(cur_pos, plain)
        elif self.radioButton_plain_z.isChecked():
            plain = (vector(0, 0, 1), self.plain_pos)
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
        self.scene_view.hand.set_save_state()
        self.scene_view.sphere.pos = vector(0, -130, 130)


def main():
    logging.basicConfig(
        format='%(levelname)s %(name)s::%(funcName)s %(message)s',
        level=logging.DEBUG)
    logging.getLogger("PyQt4").setLevel(logging.INFO)

    app = QtGui.QApplication(sys.argv)
    widget = Configurator()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
