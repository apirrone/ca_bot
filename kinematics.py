import numpy as np
import utils
import os
import sys
import math


def fk(t1, t2, t3, L1, L2, L3):
    # ==================
    # P1
    P1 = [L1*np.sin(t1), 0, L1*np.cos(t1)]
    # ==================

    # ======================
    # P2 
    L2projY = L2*np.sin(t2)
    L2projZ = L2*np.cos(t2)
    L12 = np.sqrt(L1**2 + L2projZ**2)

    delta = np.arccos(L1/L12)

    if t2 > np.pi/2 and t2 < 3*np.pi/2:
        gamma = t1 + delta
    else:
        gamma = t1 - delta
        
    P2x = L12*np.sin(gamma)
    P2y = L2projY
    P2z = L12*np.cos(gamma)
    
    P2 = [P2x, P2y, P2z]
    # ======================

    # ========================
    # P3
    w = np.sqrt(L2**2 + L3**2 + 2*L2*L3*np.cos(t3))
    delta = np.arccos((-(L3)**2 + w**2 + L2**2)/(2*w*L2))

    # if t2 < np.pi and t3 > 0 and t3 < np.pi:
    #     gamma = t2 - delta
    # elif t2 < np.pi and t3 > np.pi:
    #     gamma = t2 + delta
    # elif t2 > np.pi and t3 > 0 and t3 < np.pi:
    #     gamma = delta + (t2-np.pi)
    # elif t2 > np.pi and t3 > np.pi:
    #     gamma = (t2-np.pi) - delta
    # else:
    #     print("gamma ?????????")
    #     return -1

    gamma = t2 + delta

    L13 = w*np.cos(gamma)
    m = np.sqrt(L1**2 + L13**2)

    delta2 = np.arccos((-(L13)**2 + L1**2 + m**2)/(2*L1*m))

    # if t1 < np.pi and t2 > np.pi/2 and t2 < 3*np.pi/2:
    #     gamma2 = t1 - delta2
    # elif t1 < np.pi and (t2 > 3*np.pi/2 or t2 < np.pi/2):
    #     gamma2 = t1 + delta2
    # elif t1 > np.pi and t2 > np.pi/2 and t2 < 3*np.pi/2 :
    #     gamma2 = (t1-np.pi) + delta2
    # elif t1 > np.pi and (t2 > 3*np.pi/2 or t2 < np.pi/2):
    #     gamma2 = (t1-np.pi) - delta2
    # else:
    #     print("gamma2 ?????????")
    #     return -1
    
    gamma2 = t1 + delta2
    
    P3x = m*np.sin(gamma2)

    P3y = w*np.sin(gamma)
    
    P3z = m*np.cos(gamma2)

    P3 = [P3x, P3y, P3z]
    # ========================
    
    return P1, P2, P3

    
# def ik(x, y, z, L1, L2, L3):

#     t1 = np.pi/2 # TMP

    
#     m = np.sqrt(y**2 + z**2)
#     delta = np.arccos((-L3**2 + m**2 + L2**2)/(2*m*L2))
#     gamma = np.arcsin(y/m)
#     t2 = gamma + delta

#     t3 = np.arccos((-m**2 + L2**2 + L3**2)/(2*L2*L3))

#     return t1, t2, t3

def ik(x, y, z, L1, L2, L3):

    n = np.sqrt(z**2 + x**2)
    h = np.sqrt(n**2 - L1**2)

    delta2 = np.arccos((-h**2 + n**2 + L1**2)/(2*n*L1))
    gamma2 = np.arcsin(x/n)
    t1 = gamma2 + delta2

    
    m = np.sqrt(y**2 + h**2)
    delta = np.arccos((-L3**2 + m**2 + L2**2)/(2*m*L2))
    gamma = np.arcsin(y/m)

    t2 = gamma + delta

    t3 = np.arccos((-m**2 + L2**2 + L3**2)/(2*L2*L3))
    
    return t1, t2, t3
    
    
