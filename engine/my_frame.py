# -*- coding: utf-8 -*-
from matplotlib.rcsetup import validate_nseq_float
import numpy as np
from scene import Scene
import transformations
from vector import *

class MyFrame:
    '''Класс фрейм с корректными методами frame_to_world и world_to_frame'''
    def __init__(self, **kwargs):
        u'''Создание фрейма.
        Параметры:
        frame - родитель
        pos - позиция в локальных координатах
        x, y, z - то же что и pos
        axis - орт x
        up  - орт y
        '''
        self.frame = kwargs["frame"] if "frame" in kwargs else None

        #Определение осей
        if "axis" in kwargs:
            axis = norm(vector(kwargs["axis"]))
            up = vector(0.0, 1.0, 0.0) if "up" not in kwargs else vector(kwargs["up"]).norm()
            up = axis.cross(up).cross(axis)

            if up.mag == 0:
                up = vector(-1.0, 0.0, 0.0)
        else:
            if "up" not in kwargs:
                axis = vector(1.0, 0.0, 0.0)
                up = vector(0.0, 1.0, 0.0)
            else:
                up = norm(vector(kwargs["up"]))
                axis = kwargs.cross((0.0, 1.0, 0.0)).cross(up)
                if axis.mag == 0:
                    axis = vector(1.0, 0.0, 0.0)

        pos = vector(0.0, 0.0, 0.0) if "pos" not in kwargs else vector(kwargs["pos"])

        if "x" in kwargs:
            pos[0] = kwargs[0]

        if "y" in kwargs:
            pos[1] = kwargs[1]

        if "z" in kwargs:
            pos[2] = kwargs[2]

        self.matrix = np.identity(4)
        self.matrix[:3, 0] = axis
        self.matrix[:3, 1] = up
        self.matrix[:3, 2] = axis.cross(up)
        self.matrix[:3, 3] = pos

        self.scene = Scene.GetCurScene()
        self.scene.frames.append(self)
        self.childs = []
        
        if self.frame is not None:
            self.frame.childs.append(self)

    def __getattr__(self, name):
        if name == "axis":
            return self.matrix[:3, 0].view(vector)
        elif name == "up":
            return self.matrix[:3, 1].view(vector)
        elif name == "pos":
            return self.matrix[:3, 3].view(vector)
        raise AttributeError()

    def __setattr__(self, name, value):
        if name == "pos":
            self.matrix[:3, 3] = value
        else:
            self.__dict__[name] = value


    def remove(self):
        self.scene.frames.remove(self)
        
        for ch in self.childs:
            ch.frame = None

        if self.frame is not None:
            self.frame.childs.remove(self)
        self.childs = []

    def __del__(self):
        print "REMOVE my_frame"

    def get_matrix(self):
        u'''Возвращает матрицу фрейма'''
        if self.frame is None:
            return self.matrix

        return self.frame.get_matrix().dot(self.matrix)

    def frame_to_world(self, frame_pos):
        u'''Преобразует локальные координаты frame_pos в глобальные'''
        return vector(self.get_matrix().dot(np.array((frame_pos[0], frame_pos[1], frame_pos[2], 1.0)))[:3])

    def world_to_frame(self, world_pos):
        u'''Преобразует глобальные координаты world_pos в локальные координаты фрейма'''
        m = self.get_matrix()
        pos = vector(world_pos) - m[:3, 3]
        return vector(m.T.dot(np.array((pos[0], pos[1], pos[2], 0.)))[:3])
    
    def rotate(self, angle, axis, point=None):
        pos = self.matrix[:3, 3].copy()
        self.matrix[:3, 3] = (0, 0, 0)
        r_m = transformations.rotation_matrix(angle, axis, point)
        self.matrix = r_m.dot(self.matrix)
        self.matrix[:3, 3] = pos

    def update(self):
        pass

if __name__ == "__main__":
    f = MyFrame(pos=(12,23,3))
    print f.pos
    print f.up
    print f.axis
    print f.get_matrix()
    print f.frame_to_world(vector((1,2,3)))
    print f.world_to_frame((12,12,23))
    
    
