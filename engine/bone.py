#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from my_frame import MyFrame
from vector import *
from cylinder import cylinder as arrow


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

        self.x_arrow = arrow(frame=self, pos=(0, 0, 0), axis=(1, 0, 0), length=10, shaftwidth=1, fixedwidth = True, color=(1,0,0))
        self.y_arrow = arrow(frame=self, pos=(0, 0, 0), axis=(0, 1, 0), length=10, shaftwidth=1, fixedwidth = True, color=(0,1,0))
        self.z_arrow = arrow(frame=self, pos=(0, 0, 0), axis=(0, 0, 1), length=10, shaftwidth=1, fixedwidth = True, color=(0,0,1))
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


    def rotate_by_normal(self, plane, base_axis, freedom, global_normal):
        '''Сориентировать звено по проекции плоскости'''
        #1. преобразуем global_normal нормаль в локальную
        if self.frame is not None and isinstance(self.frame, MyFrame):
            normal = self.frame.world_to_frame(vector(0, 0, 0) + global_normal) - self.frame.world_to_frame(vector(0, 0, 0))
        else:
            normal = global_normal

        #2. найдём cross нормалей
        horizont = normal.cross(plane[0].cross(plane[1]))

        #найдём угол горизонта
        if horizont.mag > 0:
            angle = self.get_proj_angle(plane[0], plane[1], horizont)
            self.set_proj_angle(freedom, angle, plane[0], plane[1], base_axis)

    def rotate_by_normal_y(self, global_normal=vector(0, 1, 0)):
        self.rotate_by_normal((vector(0, 0, 1), vector(1, 0, 0)), self.axis.cross(self.up),
                              self.freedom_y_angle, global_normal)



###############################################################################
if __name__ == '__main__':
    from PyQt4 import QtGui
    from scene_view import SceneView
    import sys
    from sphere import sphere
    
    
    app = QtGui.QApplication(sys.argv)
    mainWin = SceneView()
    
    #координаты
    x_arrow = arrow(pos=(0, 0, 0), axis=(1, 0, 0), length=20, shaftwidth=0.5, fixedwidth = True, color=(1,0,0))
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 1, 0), length=20, shaftwidth=0.5, fixedwidth = True, color=(0,1,0))
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 0, 1), length=20, shaftwidth=0.5, fixedwidth = True, color=(0,0,1))

    #создадим руку
    b1 = Bone(freedom_z_angle=(0, 2))
    b2 = Bone(frame=b1, pos=(20, 0, 0),  freedom_z_angle=(0, 2))
    b3 = Bone(frame=b2, pos=(20, 0, 0),  freedom_z_angle=(0, 2))
    b4 = Bone(frame=b3, pos=(20, 0, 0),  freedom_z_angle=(0, 2))
    sp = sphere()
    
    #обработчик
    def on_cursor_move(camera, pos):
        global b4
        pos = camera.get_mouse_pos(pos, ((0,0,1), (0,0,0)))
        b4.calk_ik_pos(pos)
        sp.pos = pos

    mainWin.cursor_move.connect(on_cursor_move)
    mainWin.show()
    sys.exit(app.exec_())    

