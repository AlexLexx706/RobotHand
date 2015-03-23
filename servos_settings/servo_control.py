#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os
import math

class ServoControl(QtGui.QGroupBox):
    value_changed = pyqtSignal(int, int)
    angle_changed = pyqtSignal(int, int)
    remove_control = pyqtSignal(object)
    
    def __init__(self, index, settings=QtCore.QSettings("AlexLexx", "robot_hand"), parent=None):
        super(QtGui.QGroupBox, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)[0], "servo_control.ui"), self)
        self.settings = settings
        self.index = index
        self.setTitle("ID:{}".format(index))
        self.addAction(self.action_remove)
        
        #инициализация параметров
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))

        self.spinBox_min_value.setValue(self.settings.value("min_value", 500).toInt()[0])
        self.spinBox_max_value.setValue(self.settings.value("max_value", 2500).toInt()[0])
        self.doubleSpinBox_min_angle.setValue(self.settings.value("min_angle", 0.0).toDouble()[0])
        self.doubleSpinBox_max_angle.setValue(self.settings.value("max_angle", 180).toDouble()[0])
        
        self.spinBox_value.setValue(self.settings.value("value", 500).toInt()[0])

        self.settings.endGroup()
        self.settings.endGroup()
    
    @pyqtSlot('bool')
    def on_action_remove_triggered(self, v):
        self.remove_control.emit(self)
   
    def get_settings(self):
        res = ((self.doubleSpinBox_min_angle.value() / 180. * math.pi, self.spinBox_min_value.value()),\
               (self.doubleSpinBox_max_angle.value() / 180. * math.pi, self.spinBox_max_value.value()),\
               self.index, self.spinBox_value.value())
        return res
    
    def set_settings(self, settings):
        self.doubleSpinBox_min_angle.setValue(int(settings[0][0] / math.pi * 180.))
        self.spinBox_min_value.setValue(settings[0][1])
        
        self.doubleSpinBox_max_angle.setValue(int(settings[1][0] / math.pi * 180.))
        self.spinBox_max_value.setValue(settings[1][1])
        self.index = settings[2]
        self.spinBox_value.setValue(settings[3])

    @pyqtSlot('int')
    def on_spinBox_min_value_valueChanged(self, value):
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        
        self.spinBox_max_value.setMinimum(value)
        self.horizontalSlider_value.setMinimum(value)
        self.spinBox_value.setMinimum(value)
        
        #Сохраним значения
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("min_value", value)
        self.settings.endGroup()
        self.settings.endGroup()
        
        self.update_value(self.spinBox_value.value())

        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)


    @pyqtSlot('int')
    def on_spinBox_max_value_valueChanged(self, value):
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        
        self.spinBox_min_value.setMaximum(value)
        self.horizontalSlider_value.setMaximum(value)
        self.spinBox_value.setMaximum(value)
        
        #Сохраним значения
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("max_value", value)
        self.settings.endGroup()
        self.settings.endGroup()
        
        self.update_value(self.spinBox_value.value())
        
        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
    
    @pyqtSlot('int')
    def on_spinBox_value_valueChanged(self, value):
        self.update_value(value)
        
    @pyqtSlot('double')
    def on_doubleSpinBox_min_angle_valueChanged(self, value):
        self.doubleSpinBox_angle.blockSignals(True)
        
        if self.doubleSpinBox_min_angle.value() < self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_max_angle.value())

        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("min_angle", value)
        self.settings.endGroup()
        self.settings.endGroup()
        
        self.update_angle(self.doubleSpinBox_angle.value())
        self.doubleSpinBox_angle.blockSignals(False) 
        
    @pyqtSlot('double')
    def on_doubleSpinBox_max_angle_valueChanged(self, value):
        self.doubleSpinBox_angle.blockSignals(True)
        
        if self.doubleSpinBox_min_angle.value() < self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_max_angle.value())

        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("max_angle", value)
        self.settings.endGroup()
        self.settings.endGroup()

        self.update_angle(self.doubleSpinBox_angle.value())
        self.doubleSpinBox_angle.blockSignals(False) 
    
    @pyqtSlot('int')
    def on_horizontalSlider_angle_valueChanged(self, value):
        angle = value / float(self.horizontalSlider_angle.maximum()) *\
               (self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value()) +\
               self.doubleSpinBox_min_angle.value()
        
        self.update_angle(angle)
    
    @pyqtSlot('double')
    def on_doubleSpinBox_angle_valueChanged(self, value):
        self.update_angle(value)
    
    def update_value(self, value):
        '''Обновилось значение'''
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        self.doubleSpinBox_angle.blockSignals(True)
        self.horizontalSlider_angle.blockSignals(True)
        
        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("value", value)
        self.settings.endGroup()
        self.settings.endGroup()

        
        self.horizontalSlider_value.setValue(value)
        self.spinBox_value.setValue(value)
        
        angle = ((self.spinBox_value.value() - self.spinBox_min_value.value()) /\
                float(self.spinBox_max_value.value() - self.spinBox_min_value.value())) *\
                (self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value()) +\
                self.doubleSpinBox_min_angle.value()
        
        self.doubleSpinBox_angle.setValue(angle)

        slider_value = ((self.doubleSpinBox_min_angle.value() - angle) /\
                float(self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value())) *\
                self.horizontalSlider_angle.maximum()

        self.horizontalSlider_angle.setValue(abs(slider_value))

        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
        self.doubleSpinBox_angle.blockSignals(False)
        self.horizontalSlider_angle.blockSignals(False)        
        
        self.value_changed.emit(self.index, value)
        self.angle_changed.emit(self.index, angle)
        
    def update_angle(self, angle):
        '''Обновился угол'''
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        self.doubleSpinBox_angle.blockSignals(True)
        self.horizontalSlider_angle.blockSignals(True)
       
        
        self.doubleSpinBox_angle.setValue(angle)
        slider_value = ((self.doubleSpinBox_min_angle.value() - angle) /\
                float(self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value())) *\
                self.horizontalSlider_angle.maximum()
        self.horizontalSlider_angle.setValue(abs(slider_value))

        value = int((angle - self.doubleSpinBox_min_angle.value())/\
            float(self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value()) * \
            (self.spinBox_max_value.value() - self.spinBox_min_value.value()) + self.spinBox_min_value.value())

        self.settings.beginGroup("servo_control")
        self.settings.beginGroup(str(self.index))
        self.settings.setValue("value", value)
        self.settings.endGroup()
        self.settings.endGroup()
        print value

        self.horizontalSlider_value.setValue(value)
        self.spinBox_value.setValue(value)
        
        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
        self.doubleSpinBox_angle.blockSignals(False)
        self.horizontalSlider_angle.blockSignals(False)        
        
        self.value_changed.emit(self.index, value)
        self.angle_changed.emit(self.index, angle)
        
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
