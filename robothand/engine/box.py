# -*- coding: utf-8 -*-
from OpenGL.GL import *
from base_shape import base_shape
from vector import *


class box(base_shape):
    def __init__(self, **kwargs):
        """
            length=1, height=1, width=1,
            color=(1, 1, 1), pos=(0, 0, 0),
            axis=(1, 0, 0), up=(0, 1, 0)"""
        base_shape.__init__(self, **kwargs)

        if "size" in kwargs:
            self.length = kwargs["size"][0]
            self.height = kwargs["size"][1]
            self.width = kwargs["size"][2]
        else:
            self.length = kwargs["length"] if "length" in kwargs else (
                1.0 if "axis" not in kwargs else vector(kwargs["axis"]).mag)
            self.height = kwargs["height"] if "height" in kwargs else (
                1.0 if "up" not in kwargs else vector(kwargs["up"]).mag)
            self.width = kwargs["width"] if "width" in kwargs else 1.0

    def make(self):
        d_x = self.length / 2.0
        d_y = self.height / 2.0
        d_z = self.width / 2.0

        glNewList(self.list_id, GL_COMPILE)
        glBegin(GL_QUADS)           # Start Drawing The Cube
        glNormal3f(0.0, 1.0, 0.0)       # Top Right Of The Quad (Top)
        glVertex3f(-d_x, d_y, +d_z)     # Top Right Of The Quad (Top)
        glVertex3f(+d_x, d_y, +d_z)     # Top Left Of The Quad (Top)
        glVertex3f(+d_x, d_y, -d_z)     # Bottom Left Of The Quad (Top)
        glVertex3f(-d_x, d_y, -d_z)     # Bottom Right Of The Quad (Top)

        glNormal3f(0.0, -1.0, 0.0)      # Top Right Of The Quad (Top)
        glVertex3f(-d_x, -d_y, +d_z)        # Top Right Of The Quad (Bottom)
        glVertex3f(-d_x, -d_y, -d_z)        # Top Left Of The Quad (Bottom)
        glVertex3f(+d_x, -d_y, -d_z)        # Bottom Left Of The Quad (Bottom)
        glVertex3f(+d_x, -d_y, +d_z)        # Bottom Right Of The Quad (Bottom)

        glNormal3f(0.0, 0.0, 1.0)       # Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, +d_z)  # Top Right Of The Quad (Front)
        glVertex3f(-d_x, -d_y, +d_z)  # Top Left Of The Quad (Front)
        glVertex3f(+d_x, -d_y, +d_z)  # Bottom Left Of The Quad (Front)
        glVertex3f(+d_x, +d_y, +d_z)  # Bottom Right Of The Quad (Front)

        glNormal3f(0.0, 0.0, -1.0)      # Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, -d_z)        # Bottom Left Of The Quad (Back)
        glVertex3f(+d_x, +d_y, -d_z)        # Bottom Right Of The Quad (Back)
        glVertex3f(+d_x, -d_y, -d_z)        # Top Right Of The Quad (Back)
        glVertex3f(-d_x, -d_y, -d_z)        # Top Left Of The Quad (Back)

        glNormal3f(-1.0, 0.0, 0.0)      # Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, +d_z)        # Top Right Of The Quad (Left)
        glVertex3f(-d_x, +d_y, -d_z)        # Top Left Of The Quad (Left)
        glVertex3f(-d_x, -d_y, -d_z)        # Bottom Left Of The Quad (Left)
        glVertex3f(-d_x, -d_y, +d_z)        # Bottom Right Of The Quad (Left)

        glNormal3f(1.0, 0.0, 0.0)       # Top Right Of The Quad (Top)
        glVertex3f(d_x, +d_y, +d_z)  # Top Right Of The Quad (Right)
        glVertex3f(d_x, -d_y, +d_z)  # Top Left Of The Quad (Right)
        glVertex3f(d_x, -d_y, -d_z)  # Bottom Left Of The Quad (Right)
        glVertex3f(d_x, +d_y, -d_z)  # Bottom Right Of The Quad (Right)
        glEnd()                         # Done Drawing The Quad
        glEndList()


if __name__ == '__main__':
    box()
