#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from engine import *
from threading import Thread
from Queue import Queue
import time
import math

class Hand:
    '''Рука'''
    def __init__(self):
        '''Модель руки робота'''
        self.cmd_queue = None
        self.sponge_angle=0.0
        self.sponge_angle_range=(0, 85 / 180.0 * math.pi)
        self.max_sponge_move=55.0 / 2.0

        self.base = Bone()
        self.base_box = box(pos=(95/2, 25, 0), length=95, height=75, width=75)
        self.base_table = box(pos=(0, -218-5, 0), length=400, height=10, width=400)
        

        self.b0 = Bone(frame=self.base, pos=(0, 0, 0), freedom_x_angle=(-65/180 *math.pi, math.pi / 2))
        self.b0_celinder = cylinder(frame=self.b0, pos=(0, 0, 0), axis=(-30,0,0), radius=20)

        self.b1 = Bone(frame=self.b0, pos=(0, 0, 0), freedom_z_angle=(-135/180*math.pi, 0))
        self.b1_celinder = cylinder(frame=self.b1, pos=(0, 0, -75/2), axis=(0,0, 75), radius=20)
        self.b1_box = box(frame=self.b1, pos=(0, -100/2, 0), length=40, height=100, width=75)
        
        self.b2 = Bone(frame=self.b1, pos=(0, 0, 0), freedom_y_angle=(-math.pi, 0))
        self.b2_box = box(frame=self.b2, pos=(0, -135, 0), length=25, height=70, width=65)
        self.b2_celinder_2 = cylinder(frame=self.b2, pos=(0, -165, -70/2), axis=(0, 0, 70), radius=5)
        
        self.b3 = Bone(frame=self.b2, pos=(0, -165, 0), freedom_z_angle=(0, 110/180 * math.pi))
        self.b3_box = box(frame=self.b3, pos=(0, -85/2, 0), length=30, height=90, width=45)
        
        self.b4 = Bone(frame=self.b3, pos=(0, -85, 0), freedom_y_angle=(-80/180.*math.pi, 90/180*math.pi))
        self.b4_box = box(frame=self.b4, pos=(0,-50/2, 0), length=25, height=50, width=50)
        
        self.b4_sponge_l= box(frame=self.b4, pos=(0, -(50 + 55/2), 6/2), length=7, height=55, width=6)
        self.b4_sponge_r= box(frame=self.b4, pos=(0, -(50 + 55/2), -6/2), length=7, height=55, width=6)
        self.open_sponges()

        self.b5 = Bone(frame=self.b4, pos=(0, -105, 0))
        self.end = self.b5
        self.last_time = time.time()

        #self.b2.add_target(vector(-100, -10, -50), vector(0, 0, 0), 0.01)

    
    def set_sponge_value(self, angle):
        '''Установить сжатие схвата'''
        if angle < self.sponge_angle_range[0]:
            angle = self.sponge_angle_range[0]

        if angle > self.sponge_angle_range[1]:
            angle = self.sponge_angle_range[1]
            
        self.sponge_angle=angle

        offset = self.max_sponge_move * ((angle - self.sponge_angle_range[0]) / (self.sponge_angle_range[1] - self.sponge_angle_range[0]))
        self.b4_sponge_l.pos=vector(0, -(50 + 55/2), 6/2 + offset)
        self.b4_sponge_r.pos=vector(0, -(50 + 55/2), -6/2 - offset)
        
        if self.cmd_queue is not None:
            self.cmd_queue.put((0, (5, self.sponge_angle)))

    def get_sponge_value(self):
        return self.sponge_angle

    
    def open_sponges(self):
        '''Открыть схват'''
        self.set_sponge_value(85 / 180.0 * math.pi)

    def close_sponges(self):
        '''Закрыть схват'''
        self.set_sponge_value(0)

    def proto_proc(self):
        '''Обработка комманд'''

        proto = HandProtocol(port="COM27", baudrate=128000)

        while 1:
            data = self.cmd_queue.get()

            if data is None:
                return
            
            if data[0] == 0:
                proto.rotate(*data[1])
            else:
                proto.move_hand(data[1])

    def set_save_state(self):
        '''Установить манипулятор в безопасное положение'''
        self.b0.set_angle_x(-0 / 180. * math.pi)
        self.b1.set_angle_z(-00 / 180. * math.pi)
        self.b2.set_angle_y(-90 / 180. * math.pi)
        self.b3.set_angle_z(150 / 180. * math.pi)
        self.b4.set_angle_y(0 / 180. * math.pi)
        self.open_sponges()

        if self.cmd_queue is not None:
            data = (self.b0.get_angle_x(),
                    self.b1.get_angle_z(),
                    self.b2.get_angle_y(),
                    self.b3.get_angle_z(),
                    self.b4.get_angle_y(),
                    self.sponge_angle)

            self.cmd_queue.put((1, data))

    def calk_ik_pos(self, target, count=1):
        '''Установить конец манипулятора в заданную точку'''
        for i in range(count):
            pos = self.end.calk_ik_pos_2(((target, vector(0.0, 0.0, 0.0), 1.0), ))

        #с ориентируем клешню параллельно полу.
        self.b4.rotate_by_normal_y()

        if self.cmd_queue is not None:
            ct = time.time()
            dt = ct - self.last_time

            if dt > 0.05:
                data = [self.b0.get_angle_x(),
                        self.b1.get_angle_z(),
                        self.b2.get_angle_y(),
                        self.b3.get_angle_z(),
                        self.b4.get_angle_y(),
                        self.sponge_angle]
                self.last_time = ct
                self.cmd_queue.put((1, data))
        return pos
    
    def get_angles(self):
        '''Получить углы, сервисная функция'''
        return ((1, self.b0.get_angle_x() / math.pi * 180),
                (2, self.b1.get_angle_z() / math.pi * 180),
                (3, self.b2.get_angle_y() / math.pi * 180),
                (4, self.b3.get_angle_z() / math.pi * 180),
                (5, self.b4.get_angle_y() / math.pi * 180),
                (6, self.sponge_angle / math.pi * 180))
    
    def set_angle(self, index, value):
        '''Установить углы, сервисная функция'''

        value =  value / 180.0 * math.pi
        
        if index == 1:
            self.b0.set_angle_x(value)

            if self.cmd_queue is not None:
                self.cmd_queue.put((0, (0, self.b0.get_angle_x())))

        elif index == 2:
            self.b1.set_angle_z(value)

            if self.cmd_queue is not None:
                self.cmd_queue.put((0, (1, self.b1.get_angle_z())))

        elif index == 3:
            self.b2.set_angle_y(value)

            if self.cmd_queue is not None:
                self.cmd_queue.put((0, (2, self.b2.get_angle_y())))

        elif index == 4:
            self.b3.set_angle_z(value)
            
            if self.cmd_queue is not None:
                self.cmd_queue.put((0, (3, self.b3.get_angle_z())))
                
        elif index == 5:
            self.b4.set_angle_y(value)

            if self.cmd_queue is not None:
                self.cmd_queue.put((0, (4, self.b4.get_angle_y())))

        elif index == 6:
            self.set_sponge_value(value)
    
    def set_angle_range_changed(self, index, min, max):
        '''Установить пределы, сервисная функция'''
        freedom=(min / 180.0 * math.pi, max / 180. * math.pi)
        
        if index == 1:
            self.b0.freedom_x_angle = freedom
        elif index == 2:
            self.b1.freedom_z_angle = freedom
        elif index == 3:
            self.b2.freedom_y_angle = freedom
        elif index == 4:
            self.b3.freedom_z_angle = freedom
        elif index == 5:
            self.b4.freedom_y_angle = freedom
        elif index == 6:
            self.sponge_angle_range = freedom
        
    def get_target_pos(self):
        '''Получить точку конца манипулятора'''
        return self.end.frame_to_world(vector(0,0,0))
    
    def set_hand_angle(self, angle):
        '''Вращать руку'''
        self.b4.set_angle_y(angle)

        if self.cmd_queue is not None:
            self.cmd_queue.put((0, (4, angle)))

    def get_hand_angle(self, angle):
        '''Вращать руку'''
        return self.b4.get_angle_y()

if __name__ == '__main__':
    from PyQt4 import QtGui
    from engine.scene_view import SceneView
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = SceneView()
    h = Hand()
    mainWin.show()
    sys.exit(app.exec_())    
