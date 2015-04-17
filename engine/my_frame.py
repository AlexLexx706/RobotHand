# -*- coding: utf-8 -*-
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
        self.pos = vector(0.0, 0.0, 0.0) if "pos" not in kwargs else vector(kwargs["pos"])
        self.axis = vector(1.0, 0.0, 0.0) if "axis" not in kwargs else vector(kwargs["axis"])
         
        #проверка up
        if "up" not in kwargs:
            self.up_len = 1.0
            self.up = vector(self.axis).cross(vector(0,1,0)).cross(self.axis)

            if self.up.mag == 0:
                self.up = vector(-1,0,0)
        else:
            self.up = self.axis.cross(vector(kwargs["up"])).cross(self.axis)
            self.up_len = self.up.mag

        self.axis_len = self.axis.mag

        #нормализация
        self.axis.norm()
        self.up.norm()
        
        if "x" in kwargs:
            self.pos[0] = kwargs[0]
        
        if "y" in kwargs:
            self.pos[1] = kwargs[1]

        if "z" in kwargs:
            self.pos[2] = kwargs[2]
        
        self.scene = Scene.GetCurScene()
        self.scene.frames.append(self)
        self.childs = []
        
        if self.frame is not None:
            self.frame.childs.append(self)
    
    def __del__(self):
        self.scene.frames.remove(self)
        
        for ch in self.childs:
            ch.frame = None

        self.frame.childs = []

    def get_matrix(self):
        u'''Возвращает матрицу фрейма'''
        #найдём все фреймы.
        grob_matrix = np.identity(4)
        grob_matrix[:3, 0] = self.axis
        grob_matrix[:3, 1] = self.up
        grob_matrix[:3, 2] = self.axis.cross(self.up)
        grob_matrix[:3, 3] = self.pos
     
        if self.frame is None:
            return grob_matrix

        return np.dot(self.frame.get_matrix(), grob_matrix)

    def frame_to_world(self, frame_pos):
        u'''Преобразует локальные координаты frame_pos в глобальные'''
        return vector(self.get_matrix().dot(np.array((frame_pos[0], frame_pos[1], frame_pos[2], 1.0)))[:3])

    def world_to_frame(self, world_pos):
        u'''Преобразует глобальные координаты world_pos в локальные координаты фрейма'''
        m = self.get_matrix()
        pos = vector(world_pos) - m[:3, 3]
        return vector(m.T.dot(np.array((pos[0], pos[1], pos[2], 0.)))[:3])
    
    def rotate(self, angle, axis, point=None):
        m = np.identity(4)
        m[:3, 0] = self.axis
        m[:3, 1] = self.up
        m[:3, 2] = self.axis.cross(self.up)
        m[:3, 3] = self.pos
        r_m = transformations.rotation_matrix(angle, axis, point)
        n_m = r_m.dot(m)
        self.axis = vector(n_m[:3, 0])
        self.up = vector(n_m[:3, 1])
        self.pos = vector(n_m[:3, 3])

    def update(self):
        pass
    
    def first_make(self):
        pass

if __name__ == "__main__":
    f = MyFrame(pos=(12,23,3))
    print f.pos
    print f.up
    print f.axis
    print f.get_matrix()
    print f.frame_to_world(vector((1,2,3)))
    print f.world_to_frame((12,12,23))
    
    
