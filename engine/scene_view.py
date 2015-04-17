# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from sphere import sphere
from scene import Scene

class SceneView(QtOpenGL.QGLWidget):
    #движение курсора
    cursor_move = pyqtSignal(object, object)
    
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20)
        self.scale_camera = False
        self.rotate_camera = False
        self.move_cursor = False
        self.old_cursore_pos = None
        self.sphere = sphere()

    def sizeHint(self):
        return QtCore.QSize(1024, 768)

    def __del__(self):
        self.makeCurrent()

    def initializeGL(self):
        glutInit(sys.argv)
        self.scene = Scene.GetCurScene()
        self.scene.initializeGL()

    def paintGL(self):
        self.scene.update()

    def resizeGL(self, width, height):
        self.scene.resizeGL(width, height)

    def update(self):
        self.updateGL()
        #self.sphere.rotate(0.1, vector(1,0,0))
    
    def mouseMoveEvent(self, event):
        if self.scale_camera:
            offset = (event.pos() - self.old_cursore_pos).y()
            self.scene.camera.move_eye(offset*2)
        elif self.rotate_camera:
            offset = event.pos() - self.old_cursore_pos
            self.scene.camera.rotate_camera(-offset.x()*0.001, -offset.y()*0.001)
        elif self.move_cursor:
            #сдвиг камеры
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                pos = self.scene.camera.get_mouse_pos(event.pos())
                self.scene.camera.pos += (pos - self.old_3d_cur_pos)
                self.old_3d_cur_pos = pos
            else:
                self.cursor_move.emit(self.scene.camera, event.pos())
        self.old_cursore_pos = event.pos()
    
    def mouseReleaseEvent(self, event):
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = False
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = False
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = False

    def mousePressEvent(self, event):
        self.old_cursore_pos = event.pos()

        #средняя кнопка
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = True
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = True
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = True
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                self.old_3d_cur_pos = self.scene.camera.get_mouse_pos(event.pos())
            else:
                self.cursor_move.emit(self.scene.camera, event.pos())
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = GLWidget()
    mainWin.show()
    sys.exit(app.exec_())    

        