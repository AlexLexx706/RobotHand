# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from numpy import array as vector
import math


class SphereShape():
    def __init__(self, radius=0.5, segments=10, color=(1.0, 0, 0)):
        self.list_id = glGenLists(1)
        self.radius = radius
        self.segments = segments
        self.color = color

        glNewList(self.list_id, GL_COMPILE)
        glutSolidSphere(self.radius, self.segments, self.segments)
        glEndList()

    def __del__(self):
        glDeleteLists(self.list_id, 1)

    def draw(self):
        glColor(self.color)
        glCallList(self.list_id)


class CylinderShape():
    def __init__(self, radius=0.5, height=10, segments=10,  color=(1.0, 0, 0)):
        self.list_id = glGenLists(1)
        self.radius = radius
        self.height = height
        self.segments = segments
        self.color = color

        glNewList(self.list_id, GL_COMPILE)
        quadric = gluNewQuadric()
        gluQuadricOrientation(quadric, GLU_INSIDE)
        gluDisk(quadric, 0, self.radius, self.segments, 1)
        gluQuadricOrientation(quadric, GLU_OUTSIDE)
        gluCylinder(quadric, self.radius, self.radius, self.height, self.segments, 1)
        glTranslatef(0, 0, self.height);
        gluDisk(quadric, 0, self.radius, self.segments, 1)
        glEndList()

    def __del__(self):
        glDeleteLists(self.list_id, 1)

    def draw(self):
        glColor(self.color)
        glCallList(self.list_id)

class BoxShape():
    def __init__(self, length=10, height=1, width=2, color=(1.0, 0, 0)):
        self.list_id = glGenLists(1)
        self.length=length
        self.height=height
        self.width=width
        self.color=color

        d_x = length / 2.0
        d_y = height / 2.0
        d_z = width / 2.0

        glNewList(self.list_id, GL_COMPILE)
        glBegin(GL_QUADS)			# Start Drawing The Cube
        glNormal3f( 0.0, 1.0, 0.0)		# Top Right Of The Quad (Top)
        glVertex3f(-d_x, d_y, +d_z)		# Top Right Of The Quad (Top)
        glVertex3f(+d_x, d_y, +d_z)		# Top Left Of The Quad (Top)
        glVertex3f(+d_x, d_y, -d_z)		# Bottom Left Of The Quad (Top)
        glVertex3f(-d_x, d_y, -d_z)		# Bottom Right Of The Quad (Top)

        glNormal3f(0.0, -1.0, 0.0)		# Top Right Of The Quad (Top)
        glVertex3f(-d_x, -d_y, +d_z)		# Top Right Of The Quad (Bottom)
        glVertex3f(-d_x, -d_y, -d_z)		# Top Left Of The Quad (Bottom)
        glVertex3f(+d_x, -d_y, -d_z)		# Bottom Left Of The Quad (Bottom)
        glVertex3f(+d_x, -d_y, +d_z)		# Bottom Right Of The Quad (Bottom)

        glNormal3f( 0.0, 0.0, 1.0)		# Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, +d_z)	# Top Right Of The Quad (Front)
        glVertex3f(-d_x, -d_y, +d_z)	# Top Left Of The Quad (Front)
        glVertex3f(+d_x, -d_y, +d_z)	# Bottom Left Of The Quad (Front)
        glVertex3f(+d_x, +d_y, +d_z)	# Bottom Right Of The Quad (Front)

        glNormal3f( 0.0, 0.0, -1.0)		# Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, -d_z)		# Bottom Left Of The Quad (Back)
        glVertex3f(+d_x, +d_y, -d_z)		# Bottom Right Of The Quad (Back)
        glVertex3f(+d_x, -d_y, -d_z)		# Top Right Of The Quad (Back)
        glVertex3f(-d_x, -d_y, -d_z)		# Top Left Of The Quad (Back)

        glNormal3f(-1.0, 0.0, 0.0)		# Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, +d_z)		# Top Right Of The Quad (Left)
        glVertex3f(-d_x, +d_y, -d_z)		# Top Left Of The Quad (Left)
        glVertex3f(-d_x, -d_y, -d_z)		# Bottom Left Of The Quad (Left)
        glVertex3f(-d_x, -d_y, +d_z)		# Bottom Right Of The Quad (Left)

        glNormal3f( 1.0, 0.0, 0.0)		# Top Right Of The Quad (Top)
        glVertex3f(d_x, +d_y, +d_z)	# Top Right Of The Quad (Right)
        glVertex3f(d_x, -d_y, +d_z)	# Top Left Of The Quad (Right)
        glVertex3f(d_x, -d_y, -d_z)	# Bottom Left Of The Quad (Right)
        glVertex3f(d_x, +d_y, -d_z)	# Bottom Right Of The Quad (Right)
        glEnd()				            # Done Drawing The Quad
        glEndList()

    def __del__(self):
        glDeleteLists(self.list_id, 1)

    def draw(self):
        glColor(self.color)
        glCallList(self.list_id)

class Frame():
    center_list_id = None

    def __init__(self, parent=None, pos=[0.0, 0.0, 0.0], angles=[0.0, 0.0, 0.0], shapes=[]):
        self.angles = angles
        self.pos = pos
        self.show_center = True
        self.shapes = shapes
        self.parent = parent
        self.childs = []
        self.update_matrix()

        #инициализация центра.
        if self.center_list_id is None:
            self.center_list_id = glGenLists(1)

            glNewList(self.center_list_id, GL_COMPILE)
            glBegin(GL_LINES)
            glColor4d(1, 0, 0, 1)
            glVertex3f(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
            glVertex3f(GLfloat(1.0), GLfloat(0.0), GLfloat(0.0))

            glColor4d(0, 1, 0, 1)
            glVertex3f(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
            glVertex3f(GLfloat(0.0), GLfloat(1.0), GLfloat(0.0))

            glColor4d(0, 1, 0, 1)
            glVertex3f(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
            glVertex3f(GLfloat(0.0), GLfloat(0.0), GLfloat(1.0))
            glEnd()
            glEndList()

    def set_pos(self, pos):
        if pos != self.pos:
            self.pos = pos
            self.update_matrix()

    def get_pos(self):
        return self.pos

    def set_angles(self, angles):
        if self.angles != angles:
            self.angles = angles
            self.update_matrix()

    def get_angles(self):
        return self.angles

    def set_glob_pos(self, pos):
        if self.parent is None:
            self.set_pos(pos)
        else:
            m = self.parent.matrix
            v = pos - m[3][:3]
            self.set_pos(m.transpose().dot(vector([v[0], v[1], v[2], 0]))[:3])

    def get_glob_pos(self):
        return self.matrix[3][:3]

    def get_glob_angle(self):
        return (-math.arctan2(self.matrix[2][1], self.matrix[2][2]),
                math.arcsin(self.matrix[2][0]),
                -math.arctan2(self.matrix[1][0], self.matrix[0][0]))

    def set_glob_angle(self, angles):
        self.set_angles(angles)

    def update_matrix(self):
        glPushMatrix()

        if self.parent:
            glLoadMatrixd(self.parent.matrix)
            glTranslatef(self.pos[0], self.pos[1], self.pos[2])
            glRotated(self.angles[0], 1.0, 0.0, 0.0)
            glRotated(self.angles[1], 0.0, 1.0, 0.0)
            glRotated(self.angles[2], 0.0, 0.0, 1.0)
            self.matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        else:
            glLoadIdentity()
            glTranslatef(self.pos[0], self.pos[1], self.pos[2])
            glRotated(self.angles[0], 1.0, 0.0, 0.0)
            glRotated(self.angles[1], 0.0, 1.0, 0.0)
            glRotated(self.angles[2], 0.0, 0.0, 1.0)
            self.matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        #обновка у чилдренов
        for ch in self.childs:
            ch.update_matrix()

        glPopMatrix()

    def make_alone(self):
        if self.parent is None:
            return

        angle = self.get_glob_angle()
        pos = self.get_glob_pos()
        self.parent.childs.remove(self)
        self.parent = None
        self.set_pos(pos)
        self.set_alone(angle)

    def add_child(self, child):
        if child not in self.childs:
            child.make_alone()
            self.childs.append(child)
            child.parent = self

    def update(self):
        self.angles[1] += 1
        self.update_matrix()
        glPushMatrix()
        glLoadMatrixf(self.matrix)
        self.draw()
        glPopMatrix()


    def draw(self):
        if self.show_center:
            glCallList(self.center_list_id)

        for shape in self.shapes:
            shape.draw()

class Scene():
    def __init__(self):
        self.frames = []
    
    def add_frame(self, frame):
        self.frames.append(frame)
    
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for frame in self.frames:
            frame.update()

    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_COLOR_MATERIAL)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, width, height):
        side = min(width, height)

        if side < 0:
            return

        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 1000.0)
        glTranslated(0.0, -10.0, -100.0)
        glRotate(20, 1, 0, 0)


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(20)

    def sizeHint(self):
        return QtCore.QSize(1024, 768)

    def __del__(self):
        self.makeCurrent()

    def initializeGL(self):
        glutInit(sys.argv)
        self.scene = Scene()
        self.scene.initializeGL()
        frame_1 = Frame(pos=[0,0,0], shapes=[BoxShape(),])
        self.scene.add_frame(frame_1)

        self.scene.add_frame(Frame(parent=frame_1, pos=[10, 0, -20], angles=[0, 0.0, 0.0],
                                 shapes=[CylinderShape(radius=5, color=(0.0, 0.5, 0.0)),] ))

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

        