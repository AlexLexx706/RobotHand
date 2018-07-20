# -*- coding: utf-8 -*-
import logging
import numpy as np
from scene import Scene
import transformations
from vector import *

LOG = logging.getLogger(__name__)


class MyFrame:
    '''Класс фрейм с корректными методами frame_to_world и world_to_frame'''

    def __init__(
            self,
            parent=None,
            pos=vector(0.0, 0.0, 0.0),
            axis=vector(1.0, 0.0, 0.0),
            up=None):
        """
            Создание фрейма.
            Параметры:
            parent - родитель
            pos - позиция в локальных координатах
            axis - орт x
            up  - орт y
        """
        self.parent = kwargs["parent"] if "parent" in kwargs else None

        axis.norm()

        # Определение осей
        up = vector(0.0, 1.0, 0.0) if up is None else up.norm()
        up = axis.cross(up).cross(axis)

        if up.mag == 0:
            up = vector(-1.0, 0.0, 0.0)

        self._matrix = np.identity(4)
        self._matrix[:3, 0] = axis
        self._matrix[:3, 1] = up
        self._matrix[:3, 2] = axis.cross(up)
        self._matrix[:3, 3] = pos

        self.scene = Scene.GetCurScene()
        self.scene.frames.append(self)
        self.childs = []

        if self.parent is not None:
            self.parent.childs.append(self)

    @property
    def axis(self):
        '''орт оси x'''
        return self._matrix[:3, 0].view(vector)

    @property
    def up(self):
        '''орт оси y'''
        return self._matrix[:3, 1].view(vector)

    @property
    def pos(self):
        '''позиция в локальных координатах'''
        return self._matrix[:3, 3].view(vector)

    @pos.setter
    def set_pos(self, pos):
        '''установит позицию в локальных координатах'''
        self._matrix[:3, 3] = value

    @property
    def matrix(self):
        '''Возвращает матрицу фрейма'''
        return self._matrix if self.parent is None else\
            self.parent.matrix.dot(self._matrix)

    def remove(self):
        '''Удалить со сцены'''
        self.scene.frames.remove(self)

        for ch in self.childs:
            ch.parent = None

        if self.parent is not None:
            self.parent.childs.remove(self)
        self.childs = []

    def frame_to_world(self, frame_pos):
        u'''Преобразует локальные координаты frame_pos в глобальные'''
        return vector(
            self.get_matrix().dot(
                np.array((frame_pos[0], frame_pos[1], frame_pos[2], 1.0)))[:3])

    def world_to_frame(self, world_pos):
        """
            Преобразует глобальные координаты world_pos
            в локальные координаты фрейма
        """
        m = self.get_matrix()
        pos = vector(world_pos) - m[:3, 3]
        return vector(m.T.dot(np.array((pos[0], pos[1], pos[2], 0.)))[:3])

    def rotate(self, angle, axis, point=None):
        '''
            вращать во круг заданной оси axis
            относительно заданной точки point
            на угол angle
        '''
        pos = self._matrix[:3, 3].copy()
        self._matrix[:3, 3] = (0, 0, 0)
        r_m = transformations.rotation_matrix(angle, axis, point)
        self._matrix = r_m.dot(self._matrix)
        self._matrix[:3, 3] = pos

    def update(self):
        '''
            Вызывается сценой нужно использовать для
            обновления внутренней логики'''
        pass


if __name__ == "__main__":
    f = MyFrame(pos=(12, 23, 3))
    print f.pos
    print f.up
    print f.axis
    print f.get_matrix()
    print f.frame_to_world(vector((1, 2, 3)))
    print f.world_to_frame((12, 12, 23))
