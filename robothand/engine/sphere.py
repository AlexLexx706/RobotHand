# -*- coding: utf-8 -*-
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from base_shape import base_shape


class sphere(base_shape):
    def __init__(self, **kwargs):
        """
            radius = 1, segments = 10, color=(1, 1, 1),
            pos=(0, 0, 0), axis=(1, 0, 0), up=(0, 1, 0)
        """
        base_shape.__init__(self, **kwargs)
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
        glNewList(self.list_id, GL_COMPILE)
        glBegin(GL_QUADS)           # Start Drawing The Cube
        glNormal3f(0.0, 1.0, 0.0)       # Top Right Of The Quad (Top)
        glVertex3f(-self.radius, self.radius, +self.radius)     # Top Right Of The Quad (Top)
        glVertex3f(+self.radius, self.radius, +self.radius)     # Top Left Of The Quad (Top)
        glVertex3f(+self.radius, self.radius, -self.radius)     # Bottom Left Of The Quad (Top)
        glVertex3f(-self.radius, self.radius, -self.radius)     # Bottom Right Of The Quad (Top)

        glNormal3f(0.0, -1.0, 0.0)      # Top Right Of The Quad (Top)
        glVertex3f(-self.radius, -self.radius, +self.radius)        # Top Right Of The Quad (Bottom)
        glVertex3f(-self.radius, -self.radius, -self.radius)        # Top Left Of The Quad (Bottom)
        glVertex3f(+self.radius, -self.radius, -self.radius)        # Bottom Left Of The Quad (Bottom)
        glVertex3f(+self.radius, -self.radius, +self.radius)        # Bottom Right Of The Quad (Bottom)

        glNormal3f(0.0, 0.0, 1.0)       # Top Right Of The Quad (Top)
        glVertex3f(-self.radius, +self.radius, +self.radius)  # Top Right Of The Quad (Front)
        glVertex3f(-self.radius, -self.radius, +self.radius)  # Top Left Of The Quad (Front)
        glVertex3f(+self.radius, -self.radius, +self.radius)  # Bottom Left Of The Quad (Front)
        glVertex3f(+self.radius, +self.radius, +self.radius)  # Bottom Right Of The Quad (Front)

        glNormal3f(0.0, 0.0, -1.0)      # Top Right Of The Quad (Top)
        glVertex3f(-self.radius, +self.radius, -self.radius)        # Bottom Left Of The Quad (Back)
        glVertex3f(+self.radius, +self.radius, -self.radius)        # Bottom Right Of The Quad (Back)
        glVertex3f(+self.radius, -self.radius, -self.radius)        # Top Right Of The Quad (Back)
        glVertex3f(-self.radius, -self.radius, -self.radius)        # Top Left Of The Quad (Back)

        glNormal3f(-1.0, 0.0, 0.0)      # Top Right Of The Quad (Top)
        glVertex3f(-self.radius, +self.radius, +self.radius)        # Top Right Of The Quad (Left)
        glVertex3f(-self.radius, +self.radius, -self.radius)        # Top Left Of The Quad (Left)
        glVertex3f(-self.radius, -self.radius, -self.radius)        # Bottom Left Of The Quad (Left)
        glVertex3f(-self.radius, -self.radius, +self.radius)        # Bottom Right Of The Quad (Left)

        glNormal3f(1.0, 0.0, 0.0)       # Top Right Of The Quad (Top)
        glVertex3f(self.radius, +self.radius, +self.radius)  # Top Right Of The Quad (Right)
        glVertex3f(self.radius, -self.radius, +self.radius)  # Top Left Of The Quad (Right)
        glVertex3f(self.radius, -self.radius, -self.radius)  # Bottom Left Of The Quad (Right)
        glVertex3f(self.radius, +self.radius, -self.radius)  # Bottom Right Of The Quad (Right)
        glEnd()                         # Done Drawing The Quad
        glEndList()


if __name__ == '__main__':
    sphere()
