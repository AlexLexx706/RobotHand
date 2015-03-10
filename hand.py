#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from visual import * 
from bone import Bone
from threading import Thread
from Queue import Queue
import time


class Hand:
    '''Рука'''
    def __init__(self):
        self.cmd_queue = None
        self.cmd_queue = Queue()
        Thread(target=self.proto_proc).start()

        self.base = Bone()
        self.base_box = box(pos=(95/2, 25, 0), length=95, height=75, width=75)
        self.base_table = box(pos=(0, -218-5, 0), length=200, height=10, width=200)
        

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
        
        self.b4 = Bone(frame=self.b3, pos=(0, -85, 0), freedom_y_angle=(-math.pi/2, math.pi/2))
        self.b4_box = box(frame=self.b4, pos=(0,-50/2, 0), length=25, height=50, width=50)
        
        self.b4_sponge_l= box(frame=self.b4, pos=(0, -(50 + 55/2), 6/2), length=7, height=55, width=6)
        self.b4_sponge_r= box(frame=self.b4, pos=(0, -(50 + 55/2), -6/2), length=7, height=55, width=6)
        self.open_sponges()
        time.sleep(3)
        self.close_sponges()

        self.b5 = Bone(frame=self.b4, pos=(0, -105, 0))
        self.end = self.b5
        self.last_time = time.time()

        self.b2.add_target(vector(-100, -10, -50), vector(0, 0, 0), 0.01)
        self.sponge_angle=0.0
    
    def open_sponges(self):
        self.b4_sponge_l.pos=vector(0, -(50 + 55/2), 6/2 + 55/2)
        self.b4_sponge_r.pos=vector(0, -(50 + 55/2), -6/2 - 55/2)
        self.sponge_angle = 80/180*math.pi
        
        if self.cmd_queue is not None:
            self.cmd_queue.put(self.sponge_angle)

    def close_sponges(self):
        self.b4_sponge_l.pos=vector(0, -(50 + 55/2), 6/2)
        self.b4_sponge_r.pos=vector(0, -(50 + 55/2), -6/2)
        self.sponge_angle = 0.0

        if self.cmd_queue is not None:
            self.cmd_queue.put(self.sponge_angle)

    def proto_proc(self):
        from hand_protocol import HandProtocol

        proto = HandProtocol(port="COM27", baudrate=128000)

        while 1:
            data = self.cmd_queue.get()

            if data is None:
                return
            if isinstance(data, list):
                proto.move_hand(data)
            else:
                proto.rotate(5, data)

    def set_save_state(self):
        self.b0.set_angle_x(-0 / 180. * math.pi)
        self.b1.set_angle_z(-00 / 180. * math.pi)
        self.b2.set_angle_y(-90 / 180. * math.pi)
        self.b3.set_angle_z(150 / 180. * math.pi)

        if self.cmd_queue is not None:
            data = [self.b0.get_angle_x(),
                    self.b1.get_angle_z(),
                    self.b2.get_angle_y(),
                    self.b3.get_angle_z(),
                    self.b4.get_angle_y(),
                    self.sponge_angle]

            self.cmd_queue.put(data)

    def calk_ik_pos(self, target):
        self.end.calk_ik_pos_2(((target, vector(0.0, 0.0, 0.0), 1.0), ))
        print self.b0.get_angle_x() / math.pi * 180.0

        if self.cmd_queue is not None:
            ct = time.time()
            dt = ct - self.last_time

            if dt > 0.1:
                data = [self.b0.get_angle_x(),
                        self.b1.get_angle_z(),
                        self.b2.get_angle_y(),
                        self.b3.get_angle_z(),
                        self.b4.get_angle_y(),
                        self.sponge_angle]
                self.last_time = ct
                self.cmd_queue.put(data)
    
    def get_target_pos(self):
        return self.end.frame_to_world(vector(0,0,0))

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
        elif choice == 3: 
            return scene.mouse.project(normal=(0, 0, 1), point=(0, 0, 0))
        else:
            return scene.mouse.project(normal=scene.forward, point=target_pos)
            
            
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
                              u'плоскость Z',
                              u'плоскость цели'],
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
    target_pos = vector(0,0,0)

    scene.autoscale = 0
    key_masks = {}
    selected_obj = None
    selected_obj_color = None
    

    def mousedown(event):
        global move_camera
        global camera_pos
        global move_hand
        global target_pos

        mouse_down = True

        if event.shift:
            move_camera = True
            camera_pos = event.pos
        else:
            move_hand = True
            target_pos = hand.get_target_pos()

    def mouseup():
        global move_camera
        global move_hand
        move_camera = False
        move_hand = False

    def mousemove(event):
        global move_camera
        global move_hand

        #выбрали обьект
        if move_camera:
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
        #print evt.key
        
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
