# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

class Scene():
    CUR_SCENE = None
    
    @staticmethod
    def GetCurScene():
        if Scene.CUR_SCENE is None:
            return Scene()
        return Scene.CUR_SCENE

    def __init__(self):
        self.frames = []

        if Scene.CUR_SCENE is None:
            Scene.CUR_SCENE = self
    
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for frame in self.frames:
            frame.update()

    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_COLOR_MATERIAL)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_SMOOTH)
        
        for f in self.frames:
            f.first_make()

    def resizeGL(self, width, height):
        side = min(width, height)

        if side < 0:
            return

        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 1000.0)
        glTranslated(0.0, -10.0, -100.0)
        glRotate(20, 1, 0, 0)

        