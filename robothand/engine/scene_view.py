# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4.QtCore import pyqtSignal
import sphere
import scene


class SceneView(QtOpenGL.QGLWidget):
    # сигнал, движение курсора:
    # Camera, QPoint, состояние: 0-начало, 1-движение, 2-конец
    cursor_move = pyqtSignal(object, object, int)

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
        self.scale_camera = False
        self.rotate_camera = False
        self.move_cursor = False
        self.old_cursore_pos = None
        self.sphere = sphere.Sphere(radius=10)

    def sizeHint(self):
        return QtCore.QSize(1024, 768)

    def __del__(self):
        self.makeCurrent()

    def initializeGL(self):
        glutInit(sys.argv)
        self.scene = scene.Scene.GetCurScene()
        self.scene.initializeGL()

    def paintGL(self):
        self.scene.update()

    def resizeEvent(self, event):
        QtOpenGL.QGLWidget.resizeEvent(self, event)

    def resizeGL(self, width, height):
        self.scene.resizeGL(width, height)

    def update(self):
        self.updateGL()

    def mouseMoveEvent(self, event):
        if self.scale_camera:
            offset = (event.pos() - self.old_cursore_pos).y()
            self.scene.camera.move_eye(offset * 2)
        elif self.rotate_camera:
            offset = event.pos() - self.old_cursore_pos
            self.scene.camera.rotate_camera(
                -offset.x() * 0.001, -offset.y() * 0.001)
        elif self.move_cursor:
            # сдвиг камеры
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                s_p = self.scene.camera.get_mouse_pos(QtCore.QPoint(0, 0))
                n_p = self.scene.camera.get_mouse_pos(
                    event.pos() - self.old_cursore_pos)
                self.scene.camera.pos -= (n_p - s_p)
            else:
                self.cursor_move.emit(self.scene.camera, event.pos(), 1)
        self.old_cursore_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = False
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = False
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = False
            if not (event.modifiers() & QtCore.Qt.ShiftModifier):
                self.cursor_move.emit(self.scene.camera, event.pos(), 2)

    def mousePressEvent(self, event):
        self.old_cursore_pos = event.pos()

        # средняя кнопка
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = True
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = True
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = True
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                self.old_3d_cur_pos = self.scene.camera.get_mouse_pos(
                    event.pos())
            else:
                self.cursor_move.emit(self.scene.camera, event.pos(), 0)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = GLWidget()
    mainWin.show()
    sys.exit(app.exec_())
