# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from visual_common.cvisual import vector
from box import box
from sphere import sphere
from scene import Scene
from cylinder import cylinder
from hand import Hand

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20)
        self.sphere = sphere(radius=20)
        self.scale_camera = False
        self.rotate_camera = False
        self.move_cursor = False
        self.old_cursore_pos = None
        self.hand = Hand()

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
            pos = event.pos()
            #self.hand.calk_ik_pos(self.scene.camera.get_point_on_plain(pos.x(), pos.y(), self.scene.camera.get_plain()))
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

        #средн€€ кнопка
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = True
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = True
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = True
            pos = event.pos()
            #self.sphere.pos = self.scene.camera.get_pos(pos.x(), pos.y())
            pos = self.scene.camera.get_point_on_plain(pos.x(), pos.y(), self.scene.camera.get_plain())
            print pos
            self.hand.calk_ik_pos(pos)

            
        #pos = event.pos()
        #self.sphere.pos = self.scene.camera.get_point_on_plain(pos.x(), pos.y(), vector(0,0,1), vector(0,0,0))
        #self.sphere.pos = self.scene.camera.get_pos(pos.x(), pos.y())
        #print self.sphere.pos
        #self.scene.camera.rotate(0.05, vector(0, 1, 0), vector(0, 0, 0))
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = GLWidget()
    mainWin.show()
    sys.exit(app.exec_())    

        