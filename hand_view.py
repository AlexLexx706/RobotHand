# -*- coding: utf-8 -*-
from engine.scene_view import SceneView
from hand import Hand
from engine.sphere import sphere

class HandView(SceneView):
    #движение курсора
 
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
    
    def on_angle_changed(self, index, value):
        print "on_angle_changed index: {} value: {}".format(index, value)

    def on_value_changed(self, index, value):
        print "on_value_changed index: {} value: {}".format(index, value)

        
if __name__ == '__main__':
    from PyQt4 import QtGui
    import sys
    
    app = QtGui.QApplication(sys.argv)
    mainWin = HandView()
    mainWin.show()
    sys.exit(app.exec_())    

        