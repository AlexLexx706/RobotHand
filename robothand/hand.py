#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from engine import box
from engine import bone
from engine import cylinder
from engine import vector

import time
import math
import logging


LOG = logging.getLogger(__name__)


def atr(angle):
    return angle / 180.0 * math.pi


class Hand:
    '''Рука'''
    save_state = ((1, 0), (2, 0), (3, atr(-90)), (4, atr(150)), (5, 0), (6, 85))

    class WrongIndexError(Exception):
        '''Ошибка не верный индекс'''
        pass

    def __init__(self):
        '''Модель руки робота'''
        self.cmd_queue = None
        self.sponge_angle = 0.0
        self.sponge_angle_range = (0, atr(85))
        self.max_sponge_move = 55.0 / 2.0

        self.base = bone.Bone()
        self.base_box = box.Box(
            pos=(95 / 2, 25, 0),
            length=95, height=75, width=75)

        self.base_table = box.Box(
            pos=(0, -218 - 5, 0),
            length=400, height=10, width=400)

        self.b0 = bone.Bone(
            parent=self.base, pos=(0, 0, 0),
            freedom_x_angle=(atr(-65), atr(90)))
        self.b0_celinder = cylinder.Cylinder(
            parent=self.b0,
            pos=(0, 0, 0), axis=(-30, 0, 0), radius=20)

        self.b1 = bone.Bone(
            parent=self.b0, pos=(0, 0, 0),
            freedom_z_angle=(atr(-135), 0))
        self.b1_celinder = cylinder.Cylinder(
            parent=self.b1,
            pos=(0, 0, -75 / 2), axis=(0, 0, 75), radius=20)
        self.b1_box = box.Box(
            parent=self.b1, pos=(0, -100 / 2, 0),
            length=40, height=100, width=75)

        self.b2 = bone.Bone(
            parent=self.b1, pos=(0, 0, 0),
            freedom_y_angle=(atr(-180), 0))

        self.b2_box = box.Box(
            parent=self.b2, pos=(0, -135, 0),
            length=25, height=70, width=65)

        self.b2_celinder_2 = cylinder.Cylinder(parent=self.b2, pos=(
            0, -165, -70 / 2), axis=(0, 0, 70), radius=5)

        self.b3 = bone.Bone(
            parent=self.b2, pos=(0, -165, 0),
            freedom_z_angle=(0, atr(110)))

        self.b3_box = box.Box(
            parent=self.b3, pos=(0, -85 / 2, 0),
            length=30, height=90, width=45)

        self.b4 = bone.Bone(
            parent=self.b3, pos=(0, -85, 0),
            freedom_y_angle=(atr(-80), atr(90)))

        self.b4_box = box.Box(
            parent=self.b4, pos=(0, -50 / 2, 0),
            length=25, height=50, width=50)

        self.b4_sponge_l = box.Box(parent=self.b4, pos=(
            0, -(50 + 55 / 2), 6 / 2), length=7, height=55, width=6)
        self.b4_sponge_r = box.Box(parent=self.b4, pos=(
            0, -(50 + 55 / 2), -6 / 2), length=7, height=55, width=6)
        self.open_sponges()

        self.b5 = bone.Bone(parent=self.b4, pos=(0, -105, 0))
        self.end = self.b5
        self.last_time = time.time()

        # self.b2.add_target(vector.Vector(-100, -10, -50), vector.Vector(0, 0, 0), 0.01)

        # мап фукнций
        self.fun_map = {
            1: {
                "set_angle": self.b0.set_angle_x,
                "get_angle": self.b0.get_angle_x,
                "enable": True,
                "set_freedom": self.b0.set_freedom_x_angle,
                "get_freedom": self.b0.get_freedom_x_angle},
            2: {
                "set_angle": self.b1.set_angle_z,
                "get_angle": self.b1.get_angle_z,
                "enable": True,
                "set_freedom": self.b1.set_freedom_z_angle,
                "get_freedom": self.b1.get_freedom_y_angle},
            3: {
                "set_angle": self.b2.set_angle_y,
                "get_angle": self.b2.get_angle_y,
                "enable": True,
                "set_freedom": self.b2.set_freedom_y_angle,
                "get_freedom": self.b2.get_freedom_y_angle},
            4: {
                "set_angle": self.b3.set_angle_z,
                "get_angle": self.b3.get_angle_z,
                "enable": True,
                "set_freedom": self.b3.set_freedom_z_angle,
                "get_freedom": self.b3.get_freedom_z_angle},
            5: {
                "set_angle": self.b4.set_angle_y,
                "get_angle": self.b4.get_angle_y,
                "enable": True,
                "set_freedom": self.b4.set_freedom_y_angle,
                "get_freedom": self.b4.get_freedom_y_angle},
            6: {
                "set_angle": self.set_sponge_value,
                "get_angle": self.get_sponge_value,
                "enable": True,
                "set_freedom": self.set_sponge_freedom,
                "get_freedom": self.get_sponge_freedom}
        }
        self.set_save_state()

    def set_sponge_freedom(self, freedom):
        '''установим перделы хода схвата'''
        LOG.debug('freedom: %s' % (freedom, ))
        self.sponge_angle_range = freedom

    def get_sponge_freedom(self):
        return self.sponge_angle_range

    def set_sponge_value(self, angle):
        '''Установить сжатие схвата'''
        LOG.debug('angle: %s' % (angle, ))
        if angle < self.sponge_angle_range[0]:
            angle = self.sponge_angle_range[0]

        if angle > self.sponge_angle_range[1]:
            angle = self.sponge_angle_range[1]

        self.sponge_angle = angle

        offset = self.max_sponge_move * (
            (angle - self.sponge_angle_range[0]) /
            (self.sponge_angle_range[1] - self.sponge_angle_range[0]))
        self.b4_sponge_l.pos = vector.Vector(0, -(50 + 55 / 2), 6 / 2 + offset)
        self.b4_sponge_r.pos = vector.Vector(0, -(50 + 55 / 2), -6 / 2 - offset)

    def get_sponge_value(self):
        return self.sponge_angle

    def open_sponges(self):
        '''Открыть схват'''
        self.set_sponge_value(atr(85))

    def close_sponges(self):
        '''Закрыть схват'''
        self.set_sponge_value(0)

    def set_save_state(self):
        '''Установить манипулятор в безопасное положение'''
        for i, angle in self.save_state:
            self.fun_map[i]["set_angle"](angle)

        if self.cmd_queue is not None:
            self.cmd_queue.put((1, [
                [k, self.fun_map[k]["get_angle"]()]
                for k in self.fun_map if self.fun_map[k]["enable"]]))

    def calk_ik_pos(self, target, count=1):
        '''Установить конец манипулятора в заданную точку'''
        for i in range(count):
            pos = self.end.calk_ik_pos_2(
                ((target, vector.Vector(0.0, 0.0, 0.0), 1.0), ))

        # с ориентируем клешню параллельно полу.
        self.b4.rotate_by_normal_y()

        if self.cmd_queue is not None:
            ct = time.time()
            dt = ct - self.last_time

            if dt > 0.05:
                self.last_time = ct
                self.cmd_queue.put((1, [[k, self.fun_map[k]["get_angle"](
                )] for k in self.fun_map if self.fun_map[k]["enable"]]))
        return pos

    def get_angles(self):
        '''Получить углы, сервисная функция'''
        return sorted(
            (k, self.fun_map[k]["get_angle"]()) for k in self.fun_map)

    def set_angle(self, index, value):
        '''Установить углы, сервисная функция'''
        LOG.debug('index: %s value: %s' % (index, value))

        if index not in self.fun_map:
            raise self.WrongIndexError(index)

        self.fun_map[index]["set_angle"](value)

        if self.cmd_queue is not None and self.fun_map[index]["enable"]:
            self.cmd_queue.put(
                (0, (index, self.fun_map[index]["get_angle"]())))

    def set_enable_angle(self, index, e):
        '''Установить разрешение генерить комманды'''
        LOG.debug('index: %s e: %s' % (index, e,))

        if index in self.fun_map:
            self.fun_map[index]["enable"] = e

    def get_enable_angle(self, index):
        '''Возвращает разрешение'''
        if index not in self.fun_map:
            raise self.WrongIndexError(index)

        return self.fun_map[index]["enable"]

    def set_angle_range_changed(self, index, _min, _max):
        '''Установить пределы, сервисная функция'''
        LOG.debug('index: %s _min: %s _max:%s' % (index, _min, _max))

        if index not in self.fun_map:
            raise self.WrongIndexError(index)
        if _min > _max:
            m = _max
            _max = _min
            _min = m

        self.fun_map[index]["set_freedom"]((_min, _max))

    def get_target_pos(self):
        '''Получить точку конца манипулятора'''
        return self.end.frame_to_world(vector.Vector(0, 0, 0))


if __name__ == '__main__':
    from PyQt4 import QtGui
    from engine.scene_view import SceneView
    import sys
    logging.basicConfig(
        format='%(levelname)s %(name)s::%(funcName)s %(message)s',
        level=logging.DEBUG)
    logging.getLogger("PyQt4").setLevel(logging.INFO)

    app = QtGui.QApplication(sys.argv)
    mainWin = SceneView()
    h = Hand()
    mainWin.show()
    sys.exit(app.exec_())
