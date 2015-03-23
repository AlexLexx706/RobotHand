#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os
from servo_control import ServoControl
from create_servo_dialog import CreateServoDialog
import json
import sys
import logging

logger = logging.getLogger(__name__)

class ServosSettings(QtGui.QGroupBox):
    def __init__(self, parent=None, settings=QtCore.QSettings("AlexLexx", "robot_hand")):
        super(QtGui.QGroupBox, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.split(__file__)[0], "servos_settings.ui"), self)
        self.settings = settings
        self.scrollArea.addAction(self.action_add_servo)
        self.controlls = []

        #инициализация параметров
        self.settings.beginGroup("servo_control")
        self.settings.endGroup()
        
        self.open_settings(self.settings.value("last_file").toString())
    
    def get_servo_ids(self):
        return [ c.index for c in self.controlls]
        
        
    @pyqtSlot('bool')
    def on_action_add_servo_triggered(self, v):
        dialog = CreateServoDialog(self.get_servo_ids())
        
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.add_control(dialog.get_id(), None)

    def add_control(self, index, settings):
            controll = ServoControl(index, self.settings)
            self.controlls.append(controll)
            controll.remove_control.connect(self.remove_control)
            self.verticalLayout.insertWidget(self.verticalLayout.count()-1, controll)
            
            if settings is not None:
                controll.set_settings(settings)
    
    def remove_control(self, control):
        self.verticalLayout.removeWidget(control)
        self.controlls.remove(control)
        control.hide()

        self.settings.beginGroup("servo_control")
        self.settings.remove("")
        self.settings.endGroup()

    @pyqtSlot('bool')
    def on_pushButton_save_settings_clicked(self, v):
        file_name = QtGui.QFileDialog.getSaveFileName(self, u"Сохраним файл",
                    self.settings.value("last_file").toString(), "Settings (*.json)")
        
        if len(file_name):
            self.lineEdit_file.setText(file_name)
            self.settings.setValue("last_file", file_name)
            open(file_name, "wb").write(json.dumps([c.get_settings() for c in self.controlls]))

    @pyqtSlot('bool')
    def on_pushButton_open_settings_clicked(self, v):
        file_name = QtGui.QFileDialog.getOpenFileName(self, u"Открыть настройки",
                                                 self.settings.value("last_file").toString(),
                                                 "Settings (*.json)")
        self.open_settings(file_name)

    def open_settings(self, file_name):
        if len(file_name):
            self.lineEdit_file.setText(file_name)
            self.settings.setValue("last_file", file_name)

            #чистим контролы
            while len(self.controlls):
                self.remove_control(self.controlls[0])
            try:
                for settings in json.loads(open(file_name, "rb").read()):
                    self.add_control(settings[2], settings)
            except IOError as e:
                logger.warning(e)
   
if __name__ == '__main__':
    import sys
    import logging
    
    logging.basicConfig(format='%(levelname)s %(name)s::%(funcName)s%(message)s', level=logging.DEBUG)
    logging.getLogger("PyQt4").setLevel(logging.INFO)
    
    app = QtGui.QApplication(sys.argv)
    widget = ServosSettings()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
