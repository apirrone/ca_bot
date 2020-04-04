from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import numpy as np
import kinematics
import utils
import math

import backtrace
backtrace.hook(
    reverse=False,
    align=True,
    strip_path=True,
    enable_on_envvar_only=False,
    on_tty=False,
    conservative=False,
    styles={})

import keyboard 

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def deg_to_rad(angle):
    return angle/180*np.pi

def rad_to_deg(angle):
    return angle*180/np.pi


def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(700,700)
    glutCreateWindow(b"Visu")

    glClearColor(1.,1.,1.,1.)
    glShadeModel(GL_SMOOTH)
    
    # glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    lightZeroPosition = [10.,4.,10.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    
    glEnable(GL_LIGHT0)
    
    glutDisplayFunc(display)
    
    glMatrixMode(GL_PROJECTION)
    
    gluPerspective(70., 1. ,1. ,40.)
    
    glMatrixMode(GL_MODELVIEW)
    
    gluLookAt(8, 5, 5,
              0, 0, 0,
              0, 0, 1)
    
    glPushMatrix()
    glutMainLoop()
    
    glutSwapBuffers()
    glutPostRedisplay()
    return

def displayArrow(vec, color):
    glPushMatrix()
    
    glDisable(GL_LIGHTING)
    glLineWidth(6)
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_LINES)
    glVertex3f(vec[0], vec[1], vec[2])
    glVertex3f(vec[3], vec[4], vec[5])
    glEnd()

    glEnable(GL_LIGHTING)

    glPopMatrix()
    

def displayAxis(center):
    glPushMatrix()

    # RED
    glDisable(GL_LIGHTING)
    glLineWidth(6)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1., 0, 0)# X
    glEnd()

    # GREEN
    glLineWidth(6)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0., 1, 0)# Y
    glEnd()

    # BLUE
    glLineWidth(6)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0., 0, 1)# Z
    glEnd()

    glEnable(GL_LIGHTING)

    glPopMatrix()

def displayCylinder(pos, radius, height, color):
    glPushMatrix()

    glTranslatef(pos[0], pos[1], pos[2])
    cylinder = gluNewQuadric()
    gluQuadricNormals(cylinder, GLU_SMOOTH)
    glColor3ub(color[0], color[1], color[2])
    gluCylinder(cylinder, radius, radius, height, 24, 24)
    
    glPopMatrix()



    
def displayLeg(t1, t2, t3, L1, L2, L3):

    P1, P2, P3 = kinematics.fk(t1, t2, t3, L1, L2, L3)
    
    
    vec1 = [0, 0, 0] + P1
    vec2 = P1 + P2
    vec3 = P2 + P3
    displayArrow(vec1, [1, 0, 1])
    displayArrow(vec2, [1, 0, 1])
    displayArrow(vec3, [1, 0, 1])
    
    # vec2 = vec1[3:] + [vec1[3:][0], vec1[3:][1]+L2, vec1[3:][2]]
    # displayArrow(vec2, [1, 0, 1])
    
    # vec3 = vec2[3:] + [vec2[3:][0], vec2[3:][1], vec2[3:][2]-L3]
    # displayArrow(vec3, [1, 0, 1])
    
    
L1 = 2.5
L2 = 3
L3 = 2

incr_step = 0.0005

def incr_teta(t, t_boundaries, t_dir):
    if t + t_dir*incr_step < t_boundaries[0] or t + t_dir*incr_step > t_boundaries[1]:
        t_dir = -t_dir

    t += t_dir*incr_step
    return t, t_dir


t1_boundaries = [0, np.pi]
t2_boundaries = [np.pi/2, 3*np.pi/2]
t3_boundaries = [0, np.pi]

t1 = np.pi/2
t1_dir = 1
t2 = np.pi/2+0.001
t2_dir = 1
t3 = t3_boundaries[0]+0.0001
t3_dir = -1

def display():
    global t1, t1_dir, t1_boundaries
    global t2, t2_dir, t2_boundaries
    global t3, t3_dir, t3_boundaries

    # t1, t1_dir = incr_teta(t1, t1_boundaries, t1_dir)
    t2, t2_dir = incr_teta(t2, t2_boundaries, t2_dir)
    # t3, t3_dir = incr_teta(t3, t3_boundaries, t3_dir)
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    displayAxis([0, 0, 0])

    displayLeg(t1, t2, t3, L1, L2, L3)
    
    # vec = [0., 0., 0., 1., 1., 0]
    # displayArrow(vec, [1, 0, 1])
    
        
    glutSwapBuffers()
    glutPostRedisplay()    


init()

