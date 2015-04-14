# -*- coding: utf-8 -*-
import numpy as np
from scene import Scene

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
        self.pos = np.array((0.0, 0.0, 0.0)) if "pos" not in kwargs else np.array(kwargs["pos"])
        self.axis = np.array((1.0, 0.0, 0.0)) if "axis" not in kwargs else np.array(kwargs["axis"])
        self.up = np.array((0.0, 1.0, 0.0)) if "up" not in kwargs else np.array(kwargs["up"])
        
        self.axis_len = np.linalg.norm(self.axis)
        self.up_len = np.linalg.norm(self.up)

        #нормализация
        self.up = np.cross(np.cross(self.axis, self.up), self.axis)
        self.axis /= self.axis_len
        self.up /= np.linalg.norm(self.up)
        
        
        
        if "x" in kwargs:
            self.pos[0] = kwargs[0]
        
        if "y" in kwargs:
            self.pos[1] = kwargs[1]

        if "z" in kwargs:
            self.pos[2] = kwargs[2]
        
        self.scene = Scene.GetCurScene()
        self.scene.frames.append(self)
        print self.scene.frames
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
        grob_matrix[:3,0] = self.axis
        grob_matrix[:3,1] = self.up
        grob_matrix[:3,2] = np.cross(self.axis, self.up)
        grob_matrix[:3,3] = self.pos
     
        if self.frame is None:
            return grob_matrix

        return np.dot(self.frame.get_matrix(), grob_matrix)
    
    def frame_to_world(self, frame_pos):
        u'''Преобразует локальные координаты frame_pos в глобальные'''
        return np.dot(self.get_matrix(), np.array((frame_pos[0], frame_pos[1], frame_pos[2], 1.0)))[:3]

    def world_to_frame(self, world_pos):
        u'''Преобразует глобальные координаты world_pos в локальные координаты фрейма'''
        m = self.get_matrix()
        pos = np.array(world_pos) - m[:3,3]
        return np.dot(m.T, np.array((pos[0], pos[1], pos[2], 0.)))[:3]
    
    def update(self):
        pass

if __name__ == "__main__":
    f = MyFrame(pos=(12,23,3))
    print f.pos
    print f.up
    print f.axis
    print f.get_matrix()
    print f.frame_to_world(np.array((1,2,3)))
    print f.world_to_frame((12,12,23))
    
    
