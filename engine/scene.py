# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Item():
    def __init__(self):
        self.angles = [0.0, 0.0, 0.0]
        self.pos = [0.0, 0.0, 0.0]

    def update(self):
        glPushMatrix()
        glLoadIdentity();
        glTranslatef(self.pos[0], self.pos[1], self.pos[2]);
        glRotated(self.angles[0], 1.0, 0.0, 0.0)
        glRotated(self.angles[1], 0.0, 1.0, 0.0)
        glRotated(self.angles[2], 0.0, 0.0, 1.0)

        self.draw()
        glPopMatrix()
    
    def draw(self):
        glColor4d(1, 0, 0, 1)
        glutSolidSphere(GLdouble(2), GLint(10), GLint(10))

class Scene():
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def update(self):
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glMatrixMode(GL_MODELVIEW);
        
        # for item in self.items:
            # item.update()
        glClear (GL_COLOR_BUFFER_BIT)
        glColor3f (1.0, 1.0, 1.0)
        glLoadIdentity ()             # clear the matrix
        # viewing transformation
        gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glScalef (1.0, 2.0, 1.0)      # modeling transformation
        glutWireCube (1.0)
        
        glColor(1, 0, 0)
        glutSolidSphere(GLdouble(0.5), GLint(50), GLint(50))

        glFlush ()
    
    def initializeGL(self):
        #lightPos = (5.0, 5.0, 10.0, 1.0)
        #glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)
        #glEnable(GL_DEPTH_TEST)
        #glEnable(GL_NORMALIZE)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel (GL_FLAT)

    def resizeGL(self, width, height):
        #glViewport (0, 0, width, height)
        #glMatrixMode (GL_PROJECTION)
        #glLoadIdentity ()
        #glFrustum (-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
        #glMatrixMode (GL_MODELVIEW)
        
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20)

    def __del__(self):
        self.makeCurrent()

    def initializeGL(self):
        glutInit(sys.argv)
        self.scene = Scene()
        self.scene.initializeGL()
        self.scene.add_item(Item())
        
    def paintGL(self):
        self.scene.update()

    def resizeGL(self, width, height):
        self.scene.resizeGL(width, height)

    def update(self):
        self.updateGL()    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = GLWidget()
    mainWin.show()
    sys.exit(app.exec_())    

        