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
        
        from camera import camera
        self.camera = camera(pos=(200, 0, 2000), center=(0,0,0))
    
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for frame in self.frames:
            frame.update()
            

    def initializeGL(self):
        lightPos = (200, 0.0, 2000.0, 1.0)
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
        
        self.camera.update_camera()

    def resizeGL(self, width, height):
        side = min(width, height)

        if side < 0:
            return

        glViewport((width - side) / 2, (height - side) / 2, side, side)


        