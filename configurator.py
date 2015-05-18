#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from protocol.hand_protocol import HandProtocol
import os
import threading 
import Queue
import logging


logger = logging.getLogger(__name__)

class Configurator(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)[0], "configurator.ui"), self)
        self.settings = self.groupBox_settings.settings
        self.groupBox_settings.angle_changed.connect(self.scene_view.on_angle_changed)
        self.groupBox_settings.enable_angle_changed.connect(self.scene_view.on_enable_angle_changed)
        self.groupBox_settings.angle_range_changed.connect(self.scene_view.on_angle_range_changed)
        
        self.groupBox_settings.range_changed.connect(self.on_range_changed)
        self.groupBox_settings.value_changed.connect(self.on_value_changed)
        self.scene_view.angles_changed.connect(self.groupBox_settings.on_angles_changed)
        
        self.spinBox_port.setValue(self.settings.value("port_name", 27).toInt()[0])
        self.controll_thread = None
        self.proto = None
    
    @pyqtSlot(int)
    def on_spinBox_port_valueChanged(self, v):
        self.settings.setValue("port_name", v)
    
    def on_range_changed(self, index, value):
        if self.proto is not None:
            self.proto.set_limmit(index, value)

    def on_value_changed(self, index, value):
        print "on_value_changed", index, value

        if self.proto is not None:
            self.scene_view.hand.cmd_queue.put((2, (index, value)))

            
    @pyqtSlot(bool)
    def on_pushButton_connect_clicked(self, v):
        '''Подключим руку'''
        if self.controll_thread is None:
            self.proto = HandProtocol(port="COM{0}".format(self.spinBox_port.value()), baudrate=128000)
            limmits = self.groupBox_settings.get_protocol_settings()

            for index in limmits:
                self.proto.set_limmit(index , limmits[index])

            self.spinBox_port.setEnabled(False)
            self.scene_view.hand.cmd_queue = Queue.Queue()
            self.controll_thread = threading.Thread(target=self.proto_proc)
            self.controll_thread.start()
            self.pushButton_connect.setText(u'Отключить')
        else:
            self.spinBox_port.setEnabled(True)
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
                self.proto.move_servo(data[0], data[1], time_move_sec=0.05)

                
if __name__ == '__main__':
    import sys
    import logging
    
    logging.basicConfig(format='%(levelname)s %(name)s::%(funcName)s %(message)s', level=logging.DEBUG)
    logging.getLogger("PyQt4").setLevel(logging.INFO)
    
    app = QtGui.QApplication(sys.argv)
    widget = Configurator()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
