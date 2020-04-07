#!/usr/bin/env python
import math
import sys
import pybullet as p
from simulation import Simulation
import numpy as np
import kinematics
import keyboard 

directory = 'robots/demo/'
if len(sys.argv) > 1:
    directory = sys.argv[1]

sim = Simulation(directory)

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

x = 0
y = 0
z = 0

while True:
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

    t1, t2, t3 = kinematics.ik(initX + x, initY + y, initZ + z, L1, L2, L3)
    t12, t22, t32 = kinematics.ik(x - initX, y + initY, z + initZ, -L1, L2, L3)

    t1 = rescale_angle(t1)
    t2 = rescale_angle(t2)
    t3 = rescale_angle(t3)
    
    t12 = rescale_angle(t12)
    t22 = rescale_angle(t22)
    t32 = rescale_angle(t32)    
    
    targets["front_left_shoulder"] = t1 + np.pi/2
    targets["front_left_thigh"] = t2 + np.pi/2
    targets["front_left_leg"] = t3 + np.pi/2
    
    targets["back_left_shoulder"] = -(t1 + np.pi/2)
    targets["back_left_thigh"] = t2 + np.pi/2
    targets["back_left_leg"] = t3 + np.pi/2

    
    targets["front_right_shoulder"] = t12 + np.pi/2
    targets["front_right_thigh"] = -(t22 + np.pi/2)
    targets["front_right_leg"] = -(t32 + np.pi/2)
    
    targets["back_right_shoulder"] = -(t12 + np.pi/2)
    targets["back_right_thigh"] = -(t22 + np.pi/2)
    targets["back_right_leg"] = -(t32 + np.pi/2)

    sim.setJoints(targets)
    sim.tick()

