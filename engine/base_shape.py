# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from my_frame import MyFrame

class base_shape(MyFrame):
    def __init__(self, **kwargs):
        '''radius = 1, length = 1 segments = 10, color=(1, 1, 1), pos=(0, 0, 0), axis=(1, 0, 0), up=(0, 1, 0)'''
        MyFrame.__init__(self, **kwargs)
        self.color = kwargs["color"] if "color" in kwargs else (1.0, 1.0, 1.0)       
        self.list_id = None
        self.visible = True
    
    def first_make(self):
        self.list_id = glGenLists(1)    
        self.make()

    def make(self):
        pass

    def __del__(self):
        if self.list_id is not None:
            glDeleteLists(self.list_id, 1)
        MyFrame.__del__(self)

    def update(self):
        if self.visible:
            glLoadMatrixd(self.get_matrix())
            glColor(self.color)
            glCallList(self.list_id)

if __name__ == '__main__':
    base_shape()

        