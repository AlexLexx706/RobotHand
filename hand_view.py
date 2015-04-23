# -*- coding: utf-8 -*-
from engine.scene_view import SceneView
from hand import Hand
from engine.sphere import sphere
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import math

class HandView(SceneView):
    #движение курсора
    angles_changed = pyqtSignal(object)
    
    def __init__(self, parent=None):
        SceneView.__init__(self, parent)
        self.cursor_move.connect(self.on_cursor_move)
        self.hand = Hand()
        self.hand.set_save_state()
        self.sphere = sphere(radius=10)
    
    def on_cursor_move(self, camera, pos):
        pos = camera.get_point_on_plain(pos, camera.get_plain())
        self.sphere.pos = pos
        self.hand.calk_ik_pos(pos)
        
        #обновим слайдеры
        angles = ((1, self.hand.b0.get_angle_x() / math.pi * 180),
                  (2, self.hand.b1.get_angle_z() / math.pi * 180),
                  (3, self.hand.b2.get_angle_y() / math.pi * 180),
                  (4, self.hand.b3.get_angle_z() / math.pi * 180),
                  (5, self.hand.b4.get_angle_y() / math.pi * 180))
        
        self.angles_changed.emit(angles)

    
    def on_angle_changed(self, index, value):
        value =  value / 180.0 * math.pi
        if index == 1:
            self.hand.b0.set_angle_x(value)
        elif index == 2:
            self.hand.b1.set_angle_z(value)
        elif index == 3:
            self.hand.b2.set_angle_y(value)
        elif index == 4:
            self.hand.b3.set_angle_z(value)
        elif index == 5:
            self.hand.b4.set_angle_y(value)
            

    def on_value_changed(self, index, value):
        pass
    
    def on_angle_range_changed(self, index, min, max):
        freedom=(min / 180.0 * math.pi, max / 180. * math.pi)
        
        if index == 1:
            self.hand.b0.freedom_x_angle = freedom
        elif index == 2:
            self.hand.b1.freedom_z_angle = freedom
        elif index == 3:
            self.hand.b2.freedom_y_angle = freedom
        elif index == 4:
            self.hand.b3.freedom_z_angle = freedom
        elif index == 5:
            self.hand.b4.freedom_y_angle = freedom
        
if __name__ == '__main__':
    from PyQt4 import QtGui
    import sys
    
    app = QtGui.QApplication(sys.argv)
    mainWin = HandView()
    mainWin.show()
    sys.exit(app.exec_())    

        