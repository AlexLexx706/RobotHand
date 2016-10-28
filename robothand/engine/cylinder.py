# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from base_shape import base_shape
from vector import *


class cylinder(base_shape):
    def __init__(self, **kwargs):
        """
            radius = 1, length = 1 segments = 10,
            color=(1, 1, 1), pos=(0, 0, 0),
            axis=(1, 0, 0), up=(0, 1, 0)
        """
        base_shape.__init__(self, **kwargs)

        self.color = kwargs["color"] if "color" in kwargs else (1.0, 1.0, 1.0)
        self.radius = kwargs["radius"] if "radius" in kwargs else 1
        self.length = kwargs["length"] if "length" in kwargs else (
            1.0 if "axis" not in kwargs else vector(kwargs["axis"]).mag)
        self.segments = kwargs["segments"] if "segments" in kwargs else 10

    def make(self):
        glNewList(self.list_id, GL_COMPILE)
        glRotate(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluQuadricOrientation(quadric, GLU_INSIDE)
        gluDisk(quadric, 0, self.radius, self.segments, 1)
        gluQuadricOrientation(quadric, GLU_OUTSIDE)
        gluCylinder(quadric, self.radius, self.radius,
                    self.length, self.segments, 1)
        glTranslatef(0, 0, self.length)
        gluDisk(quadric, 0, self.radius, self.segments, 1)
        glEndList()


if __name__ == '__main__':
    sphere()
