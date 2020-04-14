#!/usr/bin/env python
import math
import sys
import pybullet as p

from simulation import Simulation
import numpy as np
import kinematics

from WalkEngine import WalkEngine

directory = 'robots/demo/'
if len(sys.argv) > 1:
    directory = sys.argv[1]

sim = Simulation(directory)

params = p.getDebugVisualizerCamera()
p.resetDebugVisualizerCamera(params[10]-4.5, params[8]-4.5, params[9]-4.5, [0, 0.2, 0])

controls = {}
for name in sim.getJoints():
    controls[name] = p.addUserDebugParameter(name, -math.pi, math.pi, 0)


z_key = 122
s_key = 115
q_key = 113
d_key = 100
a_key = 97
e_key = 101
p_key = 112
m_key = 109

    
L1 = 27.
L2 = 77.
L3 = 80.3

# initX = 27
initX = 27
initY = 40
initZ = -110

def rescale_angle(a):
    a -= np.pi
    return a

def rescale_angles(angles):
    return angles[0]-np.pi, angles[1]-np.pi, angles[2]-np.pi

def handleKeys():
    global deltaMax_x, deltaMax_y, goingRight, goingFront, deltaMax_x_offset, deltaMax_y_offset, deltaMax_z_offset
    keys = p.getKeyboardEvents()
    for k, v in keys.items():
        if (k == q_key and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_x = maxAcc*sim.dt
            goingRight = True
        if (k == q_key and (v & p.KEY_WAS_RELEASED)):
            deltaMax_x = -maxAcc*sim.dt
        
        if (k == d_key and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_x = -maxAcc*sim.dt
            goingRight = False
        if (k == d_key and (v & p.KEY_WAS_RELEASED)):
            deltaMax_x = maxAcc*sim.dt

        if (k == z_key and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_y = -maxAcc*sim.dt
            goingFront = True
        if (k == z_key and (v & p.KEY_WAS_RELEASED)):
            deltaMax_y = maxAcc*sim.dt
            
        if (k == s_key and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_y = maxAcc*sim.dt
            goingFront = False            
        if (k == s_key and (v & p.KEY_WAS_RELEASED)):
            deltaMax_y = -maxAcc*sim.dt

            
            
        if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_x_offset = -maxAcc*sim.dt
        if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_x_offset = 0

        if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_x_offset = maxAcc*sim.dt

        if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_x_offset = 0

        if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_y_offset = maxAcc*sim.dt

        if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_y_offset = 0
            
        if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_y_offset = -maxAcc*sim.dt
        
        if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_y_offset = 0

        if (k == p_key and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_z_offset = -maxAcc*sim.dt

        if (k == p_key and (v & p.KEY_WAS_RELEASED)):
            deltaMax_z_offset = 0

        if (k == m_key and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_z_offset = maxAcc*sim.dt

        if (k == m_key and (v & p.KEY_WAS_RELEASED)):
            deltaMax_z_offset = 0

            
x = 0
y = 0
z = 0

x_offset = 0
y_offset = 0 # -70 for reverse
z_offset = 0


deltaMax_x_offset = 0
deltaMax_y_offset = 0
deltaMax_z_offset = 0

maxStepSize_x = 30
maxStepSize_y = 60
maxAcc = 30
walkEngine = WalkEngine()

deltaMax_x = 0
deltaMax_y = 0
goingFront = False
goingRight = False

speed = 1 # (the closer to 0, the faster)
while True:
    
    splineTick = (sim.t%speed)/speed
    
    targets = {}
    for name in controls.keys():
        targets[name] = p.readUserDebugParameter(controls[name])
        

        handleKeys()

    if goingRight:
        x = max(0, min(x + deltaMax_x, maxStepSize_x))
        x_offset =  min(0, max(-17, x_offset-deltaMax_x))
        y_offset =  min(0, max(-38, y_offset-deltaMax_x))

    else:
        x = min(0, max(-maxStepSize_x, x + deltaMax_x))
        x_offset = max(0, min(x_offset - deltaMax_x, 17))
        y_offset =  min(0, max(-38, y_offset+deltaMax_x))
            
    if goingFront:
        y = min(0, max(-maxStepSize_y, y + deltaMax_y))
        # y_offset = max(0, min(y_offset - deltaMax_y, 20))
    else:
        y = max(0, min(y + deltaMax_y, maxStepSize_y))
        y_offset = min(0, max(y_offset - (deltaMax_y*2), -70))


    print(x_offset, y_offset, z_offset)
        
    x_offset = x_offset + deltaMax_x_offset
    y_offset = y_offset + deltaMax_y_offset
    z_offset = z_offset + deltaMax_z_offset

    walkEngine.changeDir([x, y], splineTick)


    fl_x, fl_y, fl_z = walkEngine.getFLPos(splineTick)
    fr_x, fr_y, fr_z = walkEngine.getFRPos(splineTick)
    br_x, br_y, br_z = walkEngine.getBRPos(splineTick)
    bl_x, bl_y, bl_z = walkEngine.getBLPos(splineTick)

    t1_fl, t2_fl, t3_fl = rescale_angles(kinematics.ik(initX + fl_x + x_offset, initY + fl_y + y_offset, initZ + fl_z + z_offset, L1, L2, L3))
    t1_bl, t2_bl, t3_bl = rescale_angles(kinematics.ik(initX + bl_x + x_offset, initY + bl_y + y_offset, initZ + bl_z + z_offset, L1, L2, L3))
    t1_fr, t2_fr, t3_fr = rescale_angles(kinematics.ik((x_offset + fr_x) - initX, y_offset + fr_y + initY, z_offset + fr_z + initZ, -L1, L2, L3))
    t1_br, t2_br, t3_br = rescale_angles(kinematics.ik((x_offset + br_x) - initX, y_offset + br_y + initY, z_offset + br_z + initZ, -L1, L2, L3))

    targets["front_left_shoulder"] = t1_fl + np.pi/2
    targets["front_left_thigh"] = t2_fl + np.pi/2
    targets["front_left_leg"] = t3_fl + np.pi/2
    
    targets["back_left_shoulder"] = -(t1_bl + np.pi/2)
    targets["back_left_thigh"] = t2_bl + np.pi/2
    targets["back_left_leg"] = t3_bl + np.pi/2
    
    targets["front_right_shoulder"] = t1_fr + np.pi/2
    targets["front_right_thigh"] = -(t2_fr + np.pi/2)
    targets["front_right_leg"] = -(t3_fr + np.pi/2)
    
    targets["back_right_shoulder"] = -(t1_br + np.pi/2)
    targets["back_right_thigh"] = -(t2_br + np.pi/2)
    targets["back_right_leg"] = -(t3_br + np.pi/2)

    sim.setJoints(targets)
    sim.tick()

