#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os
import math

class ServoControl(QtGui.QGroupBox):
    value_changed = pyqtSignal(int, int)
    angle_changed = pyqtSignal(int, float)
    remove_control = pyqtSignal(object)
    angle_range_changed = pyqtSignal(int, float, float)
    value_range_changed = pyqtSignal(int, int, int)
    
    def __init__(self,
                settings={"min": [0.0, 500], "max": [180.0, 2500], "index": 1, "value": 500},
                parent=None):

        super(QtGui.QGroupBox, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)[0], "servo_control.ui"), self)
        self.settings = settings
        print "self.settings: ", self.settings
        self.set_index(settings["index"])
        self.addAction(self.action_remove)
        self.load_default()
    
    def set_index(self, index):
        self.index = index
        self.setTitle("ID:{}".format(index))
        
    
    def load_default(self):
        #инициализация параметров
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

        if self.doubleSpinBox_min_angle.value() < self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_max_angle.value())
        
        self.spinBox_min_value.blockSignals(False)
        self.spinBox_max_value.blockSignals(False)
        self.doubleSpinBox_min_angle.blockSignals(False)
        self.doubleSpinBox_max_angle.blockSignals(False)
        self.set_value(self.settings["value"])
    
    @pyqtSlot('bool')
    def on_action_remove_triggered(self, v):
        self.remove_control.emit(self)
   
    def get_settings(self):
        return {"min":[self.doubleSpinBox_min_angle.value(), self.spinBox_min_value.value()],
                "max":[self.doubleSpinBox_max_angle.value(), self.spinBox_max_value.value()],
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
        
        self.value_range_changed.emit(self.index, self.spinBox_value.minimum(), self.spinBox_value.maximum())

        self.set_value(self.spinBox_value.value())
        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
    
    @pyqtSlot('int')
    def on_horizontalSlider_value_valueChanged(self, value):
        value = int(value / float(self.horizontalSlider_value.maximum()) *\
               (self.spinBox_max_value.value() - self.spinBox_min_value.value()) +\
               self.spinBox_min_value.value())
        #print "value: ", value
        
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
        
        self.value_range_changed.emit(self.index, self.spinBox_value.minimum(), self.spinBox_value.maximum())
        
        self.set_value(self.spinBox_value.value())
        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
    
    @pyqtSlot('int')
    def on_spinBox_value_valueChanged(self, value):
        self.set_value(value)
        
    @pyqtSlot('double')
    def on_doubleSpinBox_min_angle_valueChanged(self, value):
        self.doubleSpinBox_angle.blockSignals(True)
        
        if self.doubleSpinBox_min_angle.value() < self.doubleSpinBox_max_angle.value():
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_max_angle.value())
        else:
            self.doubleSpinBox_angle.setMaximum(self.doubleSpinBox_min_angle.value())
            self.doubleSpinBox_angle.setMinimum(self.doubleSpinBox_max_angle.value())

        self.angle_range_changed.emit(self.index, self.doubleSpinBox_angle.minimum(), self.doubleSpinBox_angle.maximum())
        
        self.set_angle(self.doubleSpinBox_angle.value())
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

        self.angle_range_changed.emit(self.index, self.doubleSpinBox_angle.minimum(), self.doubleSpinBox_angle.maximum())

        self.set_angle(self.doubleSpinBox_angle.value())
        self.doubleSpinBox_angle.blockSignals(False) 
    
    @pyqtSlot('int')
    def on_horizontalSlider_angle_valueChanged(self, value):
        angle = value / float(self.horizontalSlider_angle.maximum()) *\
               (self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value()) +\
               self.doubleSpinBox_min_angle.value()
        
        self.set_angle(angle)
    
    @pyqtSlot('double')
    def on_doubleSpinBox_angle_valueChanged(self, value):
        self.set_angle(value)
    
    def set_value(self, value):
        '''Обновилось значение'''
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        self.doubleSpinBox_angle.blockSignals(True)
        self.horizontalSlider_angle.blockSignals(True)
        
        #установка значения
        self.spinBox_value.setValue(value)
        norm_value = abs((self.spinBox_min_value.value() - value) / float(self.spinBox_max_value.value() - self.spinBox_min_value.value()))
        self.horizontalSlider_value.setValue(int(norm_value * self.horizontalSlider_value.maximum()))
        
        #установка угла
        angle = norm_value * (self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value()) + self.doubleSpinBox_min_angle.value()
        
        self.doubleSpinBox_angle.setValue(angle)
        self.horizontalSlider_angle.setValue(int(norm_value * self.horizontalSlider_angle.maximum()))

        self.horizontalSlider_value.blockSignals(False)
        self.spinBox_value.blockSignals(False)
        self.doubleSpinBox_angle.blockSignals(False)
        self.horizontalSlider_angle.blockSignals(False)        
        
        self.value_changed.emit(self.index, value)
        self.angle_changed.emit(self.index, angle)
        
    def set_angle(self, angle):
        '''Обновился угол'''
        self.horizontalSlider_value.blockSignals(True)
        self.spinBox_value.blockSignals(True)
        self.doubleSpinBox_angle.blockSignals(True)
        self.horizontalSlider_angle.blockSignals(True)
       
        
        self.doubleSpinBox_angle.setValue(angle)
        norm_value = abs(((self.doubleSpinBox_min_angle.value() - angle) / float(self.doubleSpinBox_max_angle.value() - self.doubleSpinBox_min_angle.value())))
        self.horizontalSlider_angle.setValue(int(norm_value * self.horizontalSlider_angle.maximum()))

        value = norm_value * (self.spinBox_max_value.value() - self.spinBox_min_value.value()) + self.spinBox_min_value.value()

        self.horizontalSlider_value.setValue(norm_value * self.horizontalSlider_value.maximum())
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
