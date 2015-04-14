# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from my_frame import *

class camera(MyFrame):
    def __init__(self, **kwargs):
        MyFrame.__init__(self, **kwargs)
        self.center = np.array(kwargs["center"], float) if "center" in kwargs else vector(0,0,0)
    
    def update_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 10000.0)
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                  self.center[0], self.center[1], self.center[2],
                  self.up[0], self.up[1], self.up[2])

if __name__ == '__main__':
    camera()

        