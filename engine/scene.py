# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


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

class Item():
    center_list_id = None

    def __init__(self, pos=[0.0, 0.0, 0.0], angles=[0.0, 0.0, 0.0], parent=None, shape=None):
        self.angles = angles
        self.pos = pos
        self.show_center = True
        self.shape = shape

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

    def update(self):
        glPushMatrix()
        self.angles[0] += 0.1
        self.angles[1] += 1
        glTranslatef(self.pos[0], self.pos[1], self.pos[2]);
        glRotated(self.angles[0], 1.0, 0.0, 0.0)
        glRotated(self.angles[1], 0.0, 1.0, 0.0)
        glRotated(self.angles[2], 0.0, 0.0, 1.0)

        self.draw()
        glPopMatrix()

    def draw(self):
        if self.show_center:
            glCallList(self.center_list_id)

        if self.shape is not None:
            self.shape.draw()

class Scene():
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for item in self.items:
            item.update()
    
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
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -55.0)

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
        self.scene.add_item(Item(shape=CylinderShape(radius=5, color=(0.0, 0.5, 0.0))))
        self.scene.add_item(Item(pos=[-10,0,0], shape=BoxShape()))

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

        