#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from protocol.hand_protocol import HandProtocol
import os
import multiprocessing

class Configurator(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)[0], "configurator.ui"), self)
        self.groupBox_settings.value_changed.connect(self.scene_view.on_value_changed)
        
        self.groupBox_settings.angle_changed.connect(self.scene_view.on_angle_changed)
        self.groupBox_settings.angle_range_changed.connect(self.scene_view.on_angle_range_changed)
        
        self.scene_view.angles_changed.connect(self.groupBox_settings.on_angles_changed)
        

if __name__ == '__main__':
    import sys
    import logging
    
    logging.basicConfig(format='%(levelname)s %(name)s::%(funcName)s%(message)s', level=logging.DEBUG)
    logging.getLogger("PyQt4").setLevel(logging.INFO)
    
    app = QtGui.QApplication(sys.argv)
    widget = Configurator()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
