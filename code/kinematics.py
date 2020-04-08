import numpy as np
import sys

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
    
    return (t1, t2, t3)
