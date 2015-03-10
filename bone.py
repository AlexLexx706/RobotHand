#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from __future__ import division
from visual import * 
from my_frame import MyFrame


class Bone(MyFrame):
    def __init__(self, show_center=True, freedom_x_angle=None, freedom_y_angle=None, freedom_z_angle=None,
                freedom_x_move=None, freedom_y_move=None, freedom_z_move=None, **kwargs):
        '''Обьект кость, с помощью кости можно решать задачу инверсной кинематики
              frame - предок
              pos - позиция локальные координаты
              len - длинна видимого обьекта кости
              freedom_x_angle, freedom_y_angle, freedom_z_angle - ограничения вращения,
                None или (start_angle, end_angle) - углы в радианах
              freedom_x_move, freedom_y_move, freedom_z_move - ограничения перемещения, none или (start_pos, end_pos)
        '''
        MyFrame.__init__(self, **kwargs)
        self.targets = []
        self.freedom_x_angle=freedom_x_angle
        self.freedom_y_angle=freedom_y_angle
        self.freedom_z_angle=freedom_z_angle

        self.freedom_x_move=freedom_x_move
        self.freedom_y_move=freedom_y_move
        self.freedom_z_move=freedom_z_move

        self.x_arrow = arrow(frame=self, pos=(0, 0, 0), axis=(1, 0, 0), length=10, shaftwidth=1, fixedwidth = True, color=color.red)
        self.y_arrow = arrow(frame=self, pos=(0, 0, 0), axis=(0, 1, 0), length=10, shaftwidth=1, fixedwidth = True, color=color.green)
        self.z_arrow = arrow(frame=self, pos=(0, 0, 0), axis=(0, 0, 1), length=10, shaftwidth=1, fixedwidth = True, color=color.blue)
        self.set_visible_center(show_center)
    
    def add_target(self, glob_pos, pos, weight):
        self.targets.append((glob_pos, pos, weight))

    def set_visible_center(self, v):
        self.x_arrow.visible = v
        self.y_arrow.visible = v
        self.z_arrow.visible = v

    def is_center_visible(self):
        return self.z_arrow.visible

    def get_proj_angle(self, axis, up, vec):
        '''возвращает угол проекции vec на плоскость (axis, up), угол отсчитывается от axis'''
        vec_proj = axis * axis.dot(vec) +  up * up.dot(vec)
        angle = axis.diff_angle(vec_proj)

        if up.dot(vec) < 0:
            return -angle
        return angle

    def set_proj_angle(self, freedom, angle, axis, up, vec):
        if freedom is not None:
            '''Выстовить угол проекции вектора на плоскость axis, up с учётом проидолов'''
            if angle < freedom[0]:
                angle = freedom[0]

            if angle > freedom[1]:
                angle = freedom[1]

        #установим угол
        offset_angle = angle - self.get_proj_angle(axis, up, vec)
        self.rotate(angle=offset_angle, axis=axis.cross(up))

    def get_angle_x(self):
        return self.get_proj_angle(vector(0,1,0), vector(0,0,1), self.up)

    def set_angle_x(self, angle):
        self.set_proj_angle(self.freedom_x_angle, angle, vector(0,1,0), vector(0,0,1), self.up)

    def get_angle_y(self):
        return self. get_proj_angle(vector(0,0,1), vector(1,0,0), self.axis.cross(self.up))

    def set_angle_y(self, angle):
        self.set_proj_angle(self.freedom_y_angle, angle, vector(0,0,1), vector(1,0,0), self.axis.cross(self.up))

    def get_angle_z(self):
        return self. get_proj_angle(vector(1,0,0), vector(0,1,0), self.axis)

    def set_angle_z(self, angle):
        self.set_proj_angle(self.freedom_z_angle, angle, vector(1,0,0), vector(0,1,0), self.axis)

    def calk_ik_on_plane(self, plane, base_axis, freedom, target, end):
        '''Рассчёт кинематики для оси'''
        if end.mag == 0:
            return

        axis, up = plane

        #делаем проекцию end на плоскость
        pos_proj = axis * axis.dot(end) + up * up.dot(end)

        #проверяем возможность поворота.
        if pos_proj.mag > 0.001:
            #делаем проекцию target на плоскость
            target_proj = axis * axis.dot(target) +  up * up.dot(target)

            #найдём угол между векторами.
            offset_angle = target_proj.diff_angle(pos_proj)
            rotate_axis = axis.cross(up)

            #определим знак угла.
            if target_proj.dot(rotate_axis.cross(pos_proj)) < 0:
                offset_angle = -offset_angle

            #текущий угол поворота в плоскости
            cur_angle = self.get_proj_angle(axis, up, base_axis)
            dest_angle = cur_angle + offset_angle

            #меньше минимума
            if dest_angle < freedom[0]:
                offset_angle = freedom[0] - cur_angle
            #больше максимума
            elif dest_angle > freedom[1]:
                offset_angle = freedom[1] - cur_angle

            self.rotate(angle=offset_angle, axis=rotate_axis)
            
    def calk_ik_on_plane_2(self, plane, base_axis, freedom, targets):
        '''Рассчёт кинематики для оси'''
        offset_angle = 0
        
        for target, end, weight in targets:
            offset_angle += self.calk_ik_offset_angle(plane, base_axis, freedom, target, end) * weight

        axis, up = plane
        #текущий угол поворота в плоскости
        cur_angle = self.get_proj_angle(axis, up, base_axis)
        dest_angle = cur_angle + offset_angle

        #меньше минимума
        if dest_angle < freedom[0]:
            offset_angle = freedom[0] - cur_angle
        #больше максимума
        elif dest_angle > freedom[1]:
            offset_angle = freedom[1] - cur_angle

        if offset_angle != 0.0:
            rotate_axis = axis.cross(up)
            self.rotate(angle=offset_angle, axis=rotate_axis)


    def calk_ik_offset_angle(self, plane, base_axis, freedom, target, end):
        '''Рассчёт рассчёт угла смещения для IK'''
        if end.mag == 0:
            return 0.0

        axis, up = plane

        #делаем проекцию end на плоскость
        pos_proj = axis * axis.dot(end) + up * up.dot(end)

        #проверяем возможность поворота.
        if pos_proj.mag > 0.001:
            #делаем проекцию target на плоскость
            target_proj = axis * axis.dot(target) +  up * up.dot(target)

            #найдём угол между векторами.
            offset_angle = target_proj.diff_angle(pos_proj)
            rotate_axis = axis.cross(up)

            #определим знак угла.
            if target_proj.dot(rotate_axis.cross(pos_proj)) < 0:
                offset_angle = -offset_angle
            return offset_angle
        return 0.0
    
    def calk_ik_pos_2(self, targets):
        '''Рассчёт инверсной кинематики'''
        #1. переведём в локальную систему координат
        cur_targets = []

        glob_targets = []
        for glob_target, end, weight in targets:
            glob_targets.append(glob_target)
            cur_targets.append((self.world_to_frame(glob_target), end, weight))
        
        for glob_target, end, weight in self.targets:
            glob_targets.append(glob_target)
            cur_targets.append((self.world_to_frame(glob_target), end, weight))

        #вращение по z
        if self.freedom_z_angle is not None:
            self.calk_ik_on_plane_2((vector(1, 0, 0), vector(0, 1, 0)), self.axis, self.freedom_z_angle, cur_targets)

        #вращение по y
        if self.freedom_y_angle is not None:
            self.calk_ik_on_plane_2((vector(0, 0, 1), vector(1, 0, 0)), self.axis.cross(self.up), self.freedom_y_angle, cur_targets)

        #вращение по x
        if self.freedom_x_angle is not None:
            self.calk_ik_on_plane_2((vector(0, 1, 0), vector(0, 0, 1)), self.up, self.freedom_x_angle, cur_targets)

        #рассчитаем кинематику для родителя
        if self.frame is not None and isinstance(self.frame, MyFrame):
            data = [(g, self.frame.world_to_frame(self.frame_to_world(t[1])), t[2]) for g, t in zip(glob_targets, cur_targets)]
            self.frame.calk_ik_pos_2(data)

        return self.frame_to_world(end)
            
    def calk_ik_pos(self, glob_target, end=vector(0, 0, 0)):
        '''Рассчёт инверсной кинематики'''
        #print "calk_ik_pos(calk_ik_pos:{})".format(glob_target)

        #1. переведём в локальную систему координат
        target = self.world_to_frame(glob_target)

        #вращение по z
        if self.freedom_z_angle is not None:
            self.calk_ik_on_plane((vector(1, 0, 0), vector(0, 1, 0)), self.axis, self.freedom_z_angle, target, end)

        #вращение по y
        if self.freedom_y_angle is not None:
            self.calk_ik_on_plane((vector(0, 0, 1), vector(1, 0, 0)), self.axis.cross(self.up), self.freedom_y_angle, target, end)

        #вращение по x
        if self.freedom_x_angle is not None:
            self.calk_ik_on_plane((vector(0, 1, 0), vector(0, 0, 1)), self.up, self.freedom_x_angle, target, end)

        #рассчитаем инематику для родителя
        if self.frame is not None and isinstance(self.frame, MyFrame):
            self.frame.calk_ik_pos(glob_target, self.frame.world_to_frame(self.frame_to_world(end)))
        
        return self.frame_to_world(end)

###############################################################################
if __name__ == '__main__':
    import wx
    import multiprocessing

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
    b1 = Bone(freedom_z_angle=(0, 2))
    b2 = Bone(frame=b1, pos=(20, 0, 0),  freedom_z_angle=(0, 2))
    b3 = Bone(frame=b2, pos=(20, 0, 0),  freedom_z_angle=(0, 2))
    b4 = Bone(frame=b3, pos=(20, 0, 0),  freedom_z_angle=(0, 2))

    move_camera = False
    mouse_down = False
    camera_pos = None

    scene.autoscale = 0
    key_masks = {}
    selected_obj = None
    selected_obj_color = None

    def mousedown(event):
        global move_camera
        global camera_pos
        global mouse_down

        mouse_down = True

        if event.shift:
            move_camera = True
            camera_pos = event.pos

    def mouseup():
        global move_camera
        global mouse_down
        move_camera = False
        mouse_down = False

    def mousemove(event):
        global move_camera
        global mouse_down

        #выбрали обьект
        if mouse_down:
            if not move_camera:
                b4.calk_ik_pos(get_mouse_pos())
            else:
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
        #обновление состояний.
