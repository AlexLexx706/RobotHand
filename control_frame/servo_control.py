#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os

class ServoControl(QtGui.QFrame):
    value_changed = pyqtSignal(int, int)
    angle_changed = pyqtSignal(int, int)
    
    def __init__(self, index, parent=None):
        super(QtGui.QFrame, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)[0], "servo_control.ui"), self)
        self.settings = QtCore.QSettings("AlexLexx", "robot_hand")
        self.index = index
        
        #инициализация параметров
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.spinBox_min_value.setValue(self.settings.value("min_value", 500).toInt()[0])
        self.spinBox_max_value.setValue(self.settings.value("max_value", 2500).toInt()[0])
        self.spinBox_value.setValue(self.settings.value("value", 500).toInt()[0])
        self.doubleSpinBox_min_angle.setValue(self.settings.value("min_angle", 0.0).toDouble()[0])
        self.doubleSpinBox_max_angle.setValue(self.settings.value("max_angle", 180).toDouble()[0])
        
        self.settings.endGroup()
        self.settings.endGroup()
    
    def get_value(self):
        return self.spinBox_value.value()

    def get_angle(self):
        return ((self.spinBox_value.value() - self.spinBox_min_value.value()) /\
                float(self.spinBox_max_value.value() - self.spinBox_min_value.value())) *\
                (self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value()) +\
                self.doubleSpinBox_min_angle.value()
    
    def get_borders(self):
        return self.spinBox_min_value.value(), self.spinBox_max_value.value(),\
                self.doubleSpinBox_min_angle.value(), self.doubleSpinBox_max_angle.value()
    
    @pyqtSlot('int')
    def on_spinBox_min_value_valueChanged(self, value):
        self.spinBox_max_value.setMinimum(value)
        self.horizontalSlider_value.setMinimum(value)
        self.spinBox_value.setMinimum(value)
        
        #Сохраним значения
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("min_value", value)
        self.settings.endGroup()
        self.settings.endGroup()

    @pyqtSlot('int')
    def on_spinBox_max_value_valueChanged(self, value):
        self.spinBox_min_value.setMaximum(value)
        self.horizontalSlider_value.setMaximum(value)
        self.spinBox_value.setMaximum(value)
        
        #Сохраним значения
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("max_value", value)
        self.settings.endGroup()
        self.settings.endGroup()
    
    @pyqtSlot('int')
    def on_spinBox_value_valueChanged(self, value):
        #Сохраним значения
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("value", value)
        self.settings.endGroup()
        self.settings.endGroup()
        self.value_changed.emit(self.index, value)
        self.emit_angle_changed()
    
    def emit_angle_changed(self):
        value = self.get_angle()
        print value
        self.angle_changed.emit(self.index, value)
        
    @pyqtSlot('double')
    def on_doubleSpinBox_min_angle_valueChanged(self, value):
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("min_angle", value)
        self.settings.endGroup()
        self.settings.endGroup()
        self.emit_angle_changed()
        
    @pyqtSlot('double')
    def on_doubleSpinBox_max_angle_valueChanged(self, value):
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("max_angle", value)
        self.settings.endGroup()
        self.settings.endGroup()
        self.emit_angle_changed()

if __name__ == '__main__':
    import sys
    import logging
    
    logging.basicConfig(format='%(levelname)s %(name)s::%(funcName)s%(message)s', level=logging.DEBUG)
    logging.getLogger("PyQt4").setLevel(logging.INFO)
    
    app = QtGui.QApplication(sys.argv)
    widget = ServoControl(0)
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
