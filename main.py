#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
    
if __name__ == '__main__':
    from hand import Hand
    from visual import * 
    import wx
    import time

    def get_mouse_pos():
        '''Получить положение курсора в пространстве'''
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

    def hand_rotate(evt):
        '''Вращение кисти'''
        value = hand_rotate_slider.GetValue()
        hand.set_hand_angle(value / 180. * math.pi)
        
    def move_sponge(evt):
        '''Сдвиг губок захвата'''
        value = move_sponge_slider.GetValue()
        hand.set_sponge_value(value/180.*math.pi)


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
                    width=L - 2 * d,
                    height=L - 2 * d,
                    forward=-vector(0, 1, 2))

    radio_box = wx.RadioBox(cur_window.panel,
                     pos=(d + L, d),
                     size=(150, 150),
                     choices=[u'плоскость камеры',
                              u'плоскость X',
                              u'плоскость Y',
                              u'плоскость Z',
                              u'плоскость цели'],
                     style=wx.RA_SPECIFY_ROWS)
                   
    p = cur_window.panel # Refers to the full region of the window in which to place widgets
        
    hand_rotate_slider = wx.Slider(p, pos=(d + L, 200), size=(150, 30), minValue=-85, maxValue=90)
    hand_rotate_slider.Bind(wx.EVT_SCROLL, hand_rotate)

    move_sponge_slider = wx.Slider(p, pos=(d + L, 230), size=(150, 30), minValue=0, maxValue=85)
    move_sponge_slider.Bind(wx.EVT_SCROLL, move_sponge)


    #координаты
    x_arrow = arrow(pos=(0, 0, 0), axis=(1, 0, 0), length=20, shaftwidth=0.5, fixedwidth = True, color=color.red)
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 1, 0), length=20, shaftwidth=0.5, fixedwidth = True, color=color.green)
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 0, 1), length=20, shaftwidth=0.5, fixedwidth = True, color=color.blue)

    #создадим руку
    hand = Hand()
    hand.set_save_state()

    #переменные для управления
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
