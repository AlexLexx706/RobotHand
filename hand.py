#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from visual import * 
from bone import Bone
from hand_protocol import HandProtocol
from threading import Thread
from Queue import Queue
import time


class Hand:
    '''Рука'''
    def __init__(self):
        self.base = Bone()
        self.base_box = box(pos=(59.60 /2.0, 63 /2, 0), length=59.60, height=63, width=35)
        self.base_box = box(pos=(0, -(193+5), 0), length=400, height=10, width=400)
        
        self.b0 = Bone(frame=self.base, pos=(0, 25.50, 0), freedom_x_angle=(-math.pi / 2, math.pi / 2))
        self.b0_celinder = cylinder(frame=self.b0, pos=(0, 0, 0), axis=(-19.10,0,0), radius=9.50 / 2)
        self.b0_box = box(frame=self.b0, pos=(-29.10, 10, 0), length=20, height=40, width=40)

        self.b1 = Bone(frame=self.b0, pos=(-29.10, 0, 0), freedom_z_angle=(-math.pi, 0))
        self.b1_celinder = cylinder(frame=self.b1, pos=(0, 0, -35.20), axis=(0,0, 65.20), radius=9.50 / 2)
        self.b1_box = box(frame=self.b1, pos=(0, -78.78, -10), length=20, height=40, width=40)
        
        self.b2 = Bone(frame=self.b1, pos=(0, -94.78, 0), freedom_y_angle=(-math.pi, 0))
        self.b2_celinder = cylinder(frame=self.b2, pos=(0, -10.50, 0), axis=(0, 69.50, 0), radius=9.50 / 2)
        self.b2_celinder_2 = cylinder(frame=self.b2, pos=(0, -45.50, -30.50), axis=(0, 0, 67.90), radius=9.50 / 2)
        
        self.b3 = Bone(frame=self.b2, pos=(0, -45.50, 0), freedom_z_angle=(0, math.pi * 0.8))
        self.b3_box = box(frame=self.b3, pos=(0, -10, 0), length=20, height=40, width=40)
        self.b3_box_2 = box(frame=self.b3, pos=(0, -76, 5.25), length=12, height=22, width=22.50)
        
        
        self.b4 = Bone(frame=self.b3, pos=(0, -87, 0), freedom_y_angle=(0, math.pi))
        self.b4_box = box(frame=self.b4, pos=(0, -10, 0), length=10, height=20, width=10)
        
        self.b5 = Bone(frame=self.b4, pos=(0, -27, 0))
        
        self.end = self.b5
        self.last_time = time.time()

        self.cmd_queue = None
        #self.cmd_queue = Queue()
        #Thread(target=self.proto_proc).start()

    def proto_proc(self):
        proto = HandProtocol(port="COM27", baudrate=128000)

        while 1:
            data = self.cmd_queue.get()

            if data is None:
                return
            proto.move_hand(data)

    def set_save_state(self):
        self.b0.set_angle_x(-60 / 180. * math.pi)
        self.b1.set_angle_z(-60 / 180. * math.pi)
        self.b2.set_angle_y(-90 / 180. * math.pi)
        self.b3.set_angle_z(90 / 180. * math.pi)

        if self.cmd_queue is not None:
            data = (self.b0.get_angle_x(),
                    self.b1.get_angle_z(),
                    self.b2.get_angle_y(),
                    self.b3.get_angle_z())

            self.cmd_queue.put(data)

    def calk_ik_pos(self, target):
        self.end.calk_ik_pos(target)


        if self.cmd_queue is not None:
            ct = time.time()
            dt = ct - self.last_time

            if dt > 0.1:
                data = (self.b0.get_angle_x(),
                        self.b1.get_angle_z(),
                        self.b2.get_angle_y(),
                        self.b3.get_angle_z())
                self.last_time = ct
                self.cmd_queue.put(data)

###############################################################################
if __name__ == '__main__':
    import wx

    def get_mouse_pos():
        choice = radio_box.GetSelection()

        #0 - плоскость камеры
        if choice == 0:
            return scene.mouse.pos
        #плоскость X
        elif choice == 1:
            return scene.mouse.project(normal=(1, 0, 0), point=(0, 0, 0))
        #плоскость Y
        elif choice == 2:
            return scene.mouse.project(normal=(0, 1, 0), point=(0, 0, 0))
        #плоскость Z
        return scene.mouse.project(normal=(0, 0, 1), point=(0, 0, 0))

    L = 600
    d = 20
    
    #создадим окно
    cur_window = window(width=2 * (L + window.dwidth),
                        height=L + window.dheight + window.menuheight,
                        menus=True, title='Widgets')

    #создадим окно
    scene = display(window=cur_window,
                    x=d,
                    y=d,
                    width= L - 2 * d,
                    height=L - 2 * d,
                    forward=-vector(0, 1, 2))

    radio_box = wx.RadioBox(cur_window.panel,
                     pos=(d + L, d),
                     size=(150, L- 2 * d),
                     choices=[u'плоскость камеры',
                              u'плоскость X',
                              u'плоскость Y',
                              u'плоскость Z'],
                     style=wx.RA_SPECIFY_ROWS)

    #координаты
    x_arrow = arrow(pos=(0, 0, 0), axis=(1, 0, 0), length=20, shaftwidth=0.5, fixedwidth = True, color=color.red)
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 1, 0), length=20, shaftwidth=0.5, fixedwidth = True, color=color.green)
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 0, 1), length=20, shaftwidth=0.5, fixedwidth = True, color=color.blue)

    #создадим руку
    hand = Hand()
    hand.set_save_state()

    move_camera = False
    mouse_down = False
    camera_pos = None
    move_hand = False

    scene.autoscale = 0
    key_masks = {}
    selected_obj = None
    selected_obj_color = None

    def mousedown(event):
        global move_camera
        global camera_pos
        global move_hand

        mouse_down = True

        if event.shift:
            move_camera = True
            camera_pos = event.pos
        else:
            move_hand = True
            hand.calk_ik_pos(get_mouse_pos())

    def mouseup():
        global move_camera
        global move_hand
        move_camera = False
        move_hand = False

    def mousemove(event):
        global move_camera
        global move_hand

        #выбрали обьект
        if move_hand:
            #hand.calk_ik_pos(get_mouse_pos())
            pass
        elif move_camera:
            global camera_pos
            dv = event.pos - camera_pos
            scene.center = scene.center - dv
            camera_pos = event.pos

    def key_down_hendler(evt):
        global key_masks
        key_masks[evt.key] = True

    def key_up_hendler(evt):
        global key_masks
        key_masks[evt.key] = False
        print evt.key
        
    scene.bind('keydown', key_down_hendler)
    scene.bind('keyup', key_up_hendler)
    
    scene.bind('mousedown', mousedown)
    scene.bind('mouseup', mouseup)
    scene.bind('mousemove', mousemove)
    
    while True:
        rate(30)

        if move_hand:
            hand.calk_ik_pos(get_mouse_pos())
        #обновление состояний.
