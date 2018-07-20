# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import my_frame
import vector


class camera(my_frame.MyFrame):
    def __init__(self, **kwargs):
        my_frame.MyFrame.__init__(self, **kwargs)
        self.koleno = my_frame.MyFrame(parent=self)
        self.eye = my_frame.MyFrame(
            parent=self.koleno, pos=vector.Vector(0, 0, 2000))

    def update_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 10000.0)

        center = self.matrix[:3, 3]
        eye_m = self.eye.matrix
        eye_pos = eye_m[:3, 3]
        eye_up = eye_m[:3, 1]

        gluLookAt(eye_pos[0], eye_pos[1], eye_pos[2],
                  center[0], center[1], center[2],
                  eye_up[0], eye_up[1], eye_up[2])

    def get_plain(self):
        '''возвращает плосоксть камеры: (нормаль, позицию)'''
        return (
            vector.Vector(self.eye.matrix[:3, 2] * -1.0),
            vector.Vector(self.matrix[:3, 3]))

    def move_eye(self, offset):
        self.eye.pos[2] += offset

    def rotate_camera(self, x, y):
        self.rotate(x, vector.Vector(0, 1, 0))
        self.koleno.rotate(y, vector.Vector(1, 0, 0))

    def get_pos(self, pos):
        '''Преобразует курсор pos в точку в плоскости камеры'''
        x = pos.x()
        y = pos.y()
        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview = np.identity(4)
        y = viewport[3] - y
        z = 0
        return vector.Vector(
            gluUnProject(x, y, z, modelview, projection, viewport))

    def get_point_on_plain(self, m_pos, plain):
        '''Преобразует курсор m_pos в точку на плоскости'''
        n = vector.Vector(plain[0])
        pos = vector.Vector(plain[1])
        p1 = self.get_pos(m_pos)
        p0 = self.eye.matrix[:3, 3]
        d = n.dot(p1 - p0)

        if d == 0:
            return vector.Vector(0, 0, 0)

        r = n.dot(pos - p0) / d
        return vector.Vector(p0 + r * (p1 - p0))

    def get_mouse_pos(self, pos, plain=None):
        return self.get_point_on_plain(
            pos, self.get_plain() if plain is None else plain)


if __name__ == '__main__':
    camera()
