#!/usr/bin/env python
import math
import sys
import pybullet as p

from simulation import Simulation
import numpy as np
import kinematics
import keyboard 
from LinearSpline import LinearSpline

directory = 'robots/demo/'
if len(sys.argv) > 1:
    directory = sys.argv[1]

sim = Simulation(directory)

params = p.getDebugVisualizerCamera()
p.resetDebugVisualizerCamera(params[10]-4.6, params[8]-4.6, params[9]-4.6, [0, 0.3, 0])

controls = {}
for name in sim.getJoints():
    controls[name] = p.addUserDebugParameter(name, -math.pi, math.pi, 0)

L1 = 27.
L2 = 77.
L3 = 80.3

initX = 27
initY = 17
initZ = -86

def rescale_angle(a):
    a -= np.pi
    return a

def rescale_angles(angles):
    return angles[0]-np.pi, angles[1]-np.pi, angles[2]-np.pi

x = 0
y = 0
z = 0


# FRONT LEFT SPLINES
fl_x_spline = LinearSpline()
# fl_x_spline.add_keypoint(0.5, 0)

fl_y_spline = LinearSpline()
fl_y_spline.add_keypoint(0, 0)
fl_y_spline.add_keypoint(0.125, -30)
fl_y_spline.add_keypoint(0.25, -60)
fl_y_spline.add_keypoint(1, 0)

fl_z_spline = LinearSpline()
fl_z_spline.add_keypoint(0, 0)
fl_z_spline.add_keypoint(0.125, 50)
fl_z_spline.add_keypoint(0.25, 0)
fl_z_spline.add_keypoint(1, 0)

# BACK LEFT SPLINES
bl_x_spline = LinearSpline()

bl_y_spline = fl_y_spline.copy()
bl_y_spline.set_phase_shift(0.25)

bl_z_spline = fl_z_spline.copy()
bl_z_spline.set_phase_shift(0.25)


# BACK RIGHT SPLINES
br_x_spline = LinearSpline()

br_y_spline = fl_y_spline.copy()
br_y_spline.set_phase_shift(0.5)

br_z_spline = fl_z_spline.copy()
br_z_spline.set_phase_shift(0.5)

# FRONG RIGHT SPLINES
fr_x_spline = LinearSpline()

fr_y_spline = fl_y_spline.copy()
fr_y_spline.set_phase_shift(0.75)

fr_z_spline = fl_z_spline.copy()
fr_z_spline.set_phase_shift(0.75)



speed = 3 # (the closer to one, the faster)
while True:
    
    splineTick = (sim.t%speed)/speed
    
    targets = {}
    for name in controls.keys():
        targets[name] = p.readUserDebugParameter(controls[name])

    if keyboard.is_pressed('d'):
        x += 0.05
    if keyboard.is_pressed('q'):
        x -= 0.05
    if keyboard.is_pressed('s'):
        y -= 0.05
    if keyboard.is_pressed('z'):
        y += 0.05
    if keyboard.is_pressed('m'):
        z += 0.05
    if keyboard.is_pressed('p'):
        z -= 0.05
        
    fl_x = fl_x_spline.get_value_at_time(splineTick)
    fl_y = fl_y_spline.get_value_at_time(splineTick)
    fl_z = fl_z_spline.get_value_at_time(splineTick)

    bl_x = bl_x_spline.get_value_at_time(splineTick)
    bl_y = bl_y_spline.get_value_at_time(splineTick)
    bl_z = bl_z_spline.get_value_at_time(splineTick)
    
    br_x = br_x_spline.get_value_at_time(splineTick)
    br_y = br_y_spline.get_value_at_time(splineTick)
    br_z = br_z_spline.get_value_at_time(splineTick)

    fr_x = fr_x_spline.get_value_at_time(splineTick)
    fr_y = fr_y_spline.get_value_at_time(splineTick)
    fr_z = fr_z_spline.get_value_at_time(splineTick)


    t1_fl, t2_fl, t3_fl = rescale_angles(kinematics.ik(initX + fl_x, initY + fl_y, initZ + fl_z, L1, L2, L3))
    t1_bl, t2_bl, t3_bl = rescale_angles(kinematics.ik(initX + bl_x, initY + bl_y, initZ + bl_z, L1, L2, L3))
    t1_fr, t2_fr, t3_fr = rescale_angles(kinematics.ik(fr_x - initX, fr_y + initY, fr_z + initZ, -L1, L2, L3))
    t1_br, t2_br, t3_br = rescale_angles(kinematics.ik(br_x - initX, br_y + initY, br_z + initZ, -L1, L2, L3))

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

