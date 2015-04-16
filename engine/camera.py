# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from my_frame import MyFrame
from vector import *

class camera(MyFrame):
    def __init__(self, **kwargs):
        MyFrame.__init__(self, **kwargs)
        self.koleno = MyFrame(frame=self)
        self.eye = MyFrame(frame=self.koleno, pos=vector(0, 0, 2000))
    
    def update_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 10000.0)
        
        center = self.get_matrix()[:3, 3]
        eye_m = self.eye.get_matrix()
        eye_pos = eye_m[:3, 3]
        eye_up = eye_m[:3, 1]

        gluLookAt(eye_pos[0], eye_pos[1],eye_pos[2],
                  center[0], center[1], center[2],
                  eye_up[0], eye_up[1], eye_up[2])
    
    def get_plain(self):
        return vector(self.eye.get_matrix()[:3, 2] * -1.0), vector(self.get_matrix()[:3, 3])

    def move_eye(self, offset):
        self.eye.pos[2] += offset
    
    def rotate_camera(self, x, y):
        self.rotate(x, vector(0,1,0))
        self.koleno.rotate(y, vector(1,0,0))

    def get_pos(self, x, y):
        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview = np.identity(4)
        y = viewport[3] - y
        z = 1
        return vector(gluUnProject(x, y, z, modelview, projection, viewport))
        
    def get_point_on_plain(self, x, y, plain):
        '''Возвращает точку на плоскости'''
        n, pos = plain
        p1 = self.get_pos(x, y)
        p0 = self.eye.get_matrix()[:3, 3]
        d = n.dot(p1 - p0)

        if d  == 0:
            return vector(0,0,0)

        r = n.dot(pos - p0) / d
        return vector(p0 + r * (p1 - p0))
        
        

if __name__ == '__main__':
    camera()

        