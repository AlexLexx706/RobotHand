# -*- coding: utf-8 -*-
from OpenGL.GL import *
import my_frame


class BaseShape(my_frame.MyFrame):
    def __init__(self, **kwargs):
        """
            radius = 1, length = 1 segments = 10,
            color=(1, 1, 1), pos=(0, 0, 0), axis=(1, 0, 0), up=(0, 1, 0)
        """
        my_frame.MyFrame.__init__(self, **kwargs)
        self.color = kwargs["color"] if "color" in kwargs else (1.0, 1.0, 1.0)
        self.list_id = None
        self.visible = True
        self.first_make = True

    def make(self):
        pass

    def remove(self):
        if self.list_id is not None:
            glDeleteLists(self.list_id, 1)
        my_frame.MyFrame.remove(self)

    def update(self):
        # построение
        if self.first_make:
            if self.list_id is None:
                self.list_id = glGenLists(1)
            self.make()
            self.first_make = False

        if self.visible:
            glLoadMatrixd(self.matrix.T)
            glColor(self.color)
            glCallList(self.list_id)


if __name__ == '__main__':
    BaseShape()
