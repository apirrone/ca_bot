import numpy as np
import utils
import os
import sys
import math


def fk(t1, t2, t3, L1, L2, L3):

    P1 = [L1*np.sin(t1), 0, L1*np.cos(t1)]

    L02 = np.sqrt(L1**2 + (L2*np.cos(t2))**2)
    alpha = t1 - np.arccos(L1/L02)
    P2x = L02*np.sin(alpha)
    P2y = L2*np.sin(t2)
    P2z = L02*np.cos(alpha)
    
    P2 = [P2x, P2y, P2z]



    L13 = np.sqrt(L2**2 + L3**2 + 2*L3*L2*np.cos(t3))
    # print(-(L3)**2 + L13**2 + L2**2/(2*L2*L13))
    delta = np.arccos((-(L3)**2 + L13**2 + L2**2)/(2*L2*L13))
    # print(delta)
    gamma = t2 - delta
    L03 = np.sqrt(L1**2 + (L13*np.cos(gamma))**2)
    delta2 = np.arccos((-(L13*np.cos(gamma))**2 + L03**2 + L1**2)/(2*L03*L1))
    gamma2 = t1 - delta2
    P3x = L03*np.sin(gamma2)
    P3y = L13*np.sin(gamma)
    P3z = L03*np.cos(gamma2)

    P3 = [P3x, P3y, P3z]
    
    return P1, P2, P3

    
