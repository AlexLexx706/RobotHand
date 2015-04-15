# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from my_frame import *
from box import box
from sphere import sphere
from scene import Scene
from cylinder import cylinder

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20)
        self.sphere = sphere(radius=20)
        

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
    
    def mousePressEvent(self, event):
        pos = event.pos()
        self.sphere.pos = self.scene.camera.get_point_on_plain(pos.x(), pos.y(), vector(0,0,1), vector(0,0,0))
        #self.sphere.pos = self.scene.camera.get_pos(pos.x(), pos.y())
        print self.sphere.pos
        #self.scene.camera.rotate(0.05, vector(0, 1, 0), vector(0, 0, 0))
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = GLWidget()
    mainWin.show()
    sys.exit(app.exec_())    

        