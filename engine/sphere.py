# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from base_shape import base_shape

class sphere(base_shape):
    def __init__(self, **kwargs):
        '''radius = 1, segments = 10, color=(1, 1, 1), pos=(0, 0, 0), axis=(1, 0, 0), up=(0, 1, 0)'''

        base_shape.__init__(self, **kwargs)

        self.color = kwargs["color"] if "color" in kwargs else (1.0, 1.0, 1.0)       
        self.radius = kwargs["radius"] if "radius" in kwargs else 1
        self.segments = kwargs["segments"] if "segments" in kwargs else 10
    
    def make(self):
        glNewList(self.list_id, GL_COMPILE)
        glutSolidSphere(self.radius, self.segments, self.segments)
        glEndList()

if __name__ == '__main__':
    sphere()

        