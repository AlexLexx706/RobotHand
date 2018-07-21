# -*- coding: utf-8 -*-
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import base_shape


class Sphere(base_shape.BaseShape):
    def __init__(self, **kwargs):
        """
            radius = 1, segments = 10, color=(1, 1, 1),
            pos=(0, 0, 0), axis=(1, 0, 0), up=(0, 1, 0)
        """
        base_shape.BaseShape.__init__(self, **kwargs)
        self.color = kwargs["color"] if "color" in kwargs else (1.0, 1.0, 1.0)
        self.radius = kwargs["radius"] if "radius" in kwargs else 1
        self.segments = kwargs["segments"] if "segments" in kwargs else 10

    def make(self):
        if sys.platform != 'win32':
            glNewList(self.list_id, GL_COMPILE)
            glutSolidSphere(self.radius, self.segments, self.segments)
            glEndList()
        else:
            self.create_box()

    def create_box(self):
        print('Sphere.create_box radius: self.radius:%s' % (self.radius, ))
        glNewList(self.list_id, GL_COMPILE)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-self.radius, self.radius, +self.radius)
        glVertex3f(+self.radius, self.radius, +self.radius)
        glVertex3f(+self.radius, self.radius, -self.radius)
        glVertex3f(-self.radius, self.radius, -self.radius)

        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-self.radius, -self.radius, +self.radius)
        glVertex3f(-self.radius, -self.radius, -self.radius)
        glVertex3f(+self.radius, -self.radius, -self.radius)
        glVertex3f(+self.radius, -self.radius, +self.radius)

        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-self.radius, +self.radius, +self.radius)
        glVertex3f(-self.radius, -self.radius, +self.radius)
        glVertex3f(+self.radius, -self.radius, +self.radius)
        glVertex3f(+self.radius, +self.radius, +self.radius)

        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-self.radius, +self.radius, -self.radius)
        glVertex3f(+self.radius, +self.radius, -self.radius)
        glVertex3f(+self.radius, -self.radius, -self.radius)
        glVertex3f(-self.radius, -self.radius, -self.radius)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-self.radius, +self.radius, +self.radius)
        glVertex3f(-self.radius, +self.radius, -self.radius)
        glVertex3f(-self.radius, -self.radius, -self.radius)
        glVertex3f(-self.radius, -self.radius, +self.radius)

        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(self.radius, +self.radius, +self.radius)
        glVertex3f(self.radius, -self.radius, +self.radius)
        glVertex3f(self.radius, -self.radius, -self.radius)
        glVertex3f(self.radius, +self.radius, -self.radius)
        glEnd()
        glEndList()


if __name__ == '__main__':
    sphere()
