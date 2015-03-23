# -*- coding: utf-8 -*-


class MyFrame(frame):
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
        frame.__init__(self, **kwargs)
    
    def get_matrix(self):
        u'''Возвращает матрицу фрейма'''
        #найдём все фреймы.
        grob_matrix = numpy.identity(4)
        grob_matrix[:3,0] = self.axis
        grob_matrix[:3,1] = self.up
        grob_matrix[:3,2] = cross(self.axis, self.up)
        grob_matrix[:3,3] = self.pos

        cur_frame = self.frame
     
        while cur_frame is not None:
            cur_matrix = numpy.identity(4)
            cur_matrix[:3,0] = cur_frame.axis
            cur_matrix[:3,1] = cur_frame.up
            cur_matrix[:3,2] = cross(cur_frame.axis, cur_frame.up)
            cur_matrix[:3,3] = cur_frame.pos
            grob_matrix = numpy.dot(cur_matrix, grob_matrix)
            
            cur_frame = cur_frame.frame

        return grob_matrix
    
    def frame_to_world(self, frame_pos):
        u'''Преобразует локальные координаты frame_pos в глобальные'''
        return vector(numpy.dot(self.get_matrix(), (frame_pos[0], frame_pos[1], frame_pos[2], 1.0))[:3])
        
    def world_to_frame(self, world_pos):
        u'''Преобразует глобальные координаты world_pos в локальные координаты фрейма'''
        m = self.get_matrix()
        pos = world_pos - m[:3,3]
        return vector(numpy.dot(m.T, (pos[0],pos[1],pos[2], 0.))[:3])
