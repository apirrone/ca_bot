import numpy as np

def dist(pos1, pos2):
    return np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2)


def is_between(value, boundaries):
    return value >= boundaries[0] and value <= boundaries[1]
    

# def rotate(origin, position, angle, axis='x'):
#     if axis == 'x':
#         m = np.array([[1, 0, 0],
#                       [0,  np.cos(angle), -np.sin(angle)],
#                       [0, np.sin(angle), np.cos(angle)]])
#     elif axis == 'y':
#         m = np.array([[np.cos(angle), 0, np.sin(angle)],
#                       [0, 1, 0],
#                       [-np.sin(angle), 0, np.cos(angle)]])
#     elif axis == 'z':
#         m = np.array([[np.cos(angle), -np.sin(angle), 0],
#                       [np.sin(angle),  np.cos(angle), 0],
#                       [0, 0, 1]])
#     else:
#         print("Error, axis ", axis, " does not exist.")
#         return -1


#     # translate to origin
#     position[0] -= origin[0]
#     self.shaftEndPos[0] -= self.pos[0]
#     self.shaftEndPos[1] -= self.pos[1]
#     self.shaftEndPos[2] -= self.pos[2]
    
        
#     # rotate
#     self.shaftEndPos = m.dot(self.shaftEndPos)
