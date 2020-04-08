import numpy as np
import collections

class LinearSpline:
    def __init__(self):
        self.keypoints = {0:0, 1:0}
        self.phase_shift = 0
        
    def add_keypoint(self, time, value):
        if time >= 0 and time <= 1:
            self.keypoints[time] = value
            self.keypoints = collections.OrderedDict(sorted(self.keypoints.items()))
        else:
            print("Invalid value '", time, "' for 'time' parameter. Must be between 0 and 1")
            exit()
            
    def get_value_at_time(self, time):
        if len(self.keypoints) > 1:
            if time >= 0 and time <= 1:

                time = (time+self.phase_shift)%1
                
                if time in self.keypoints:
                    return self.keypoints[time]
                
                point1 = None
                point2 = None
                
                point1 = (0, self.keypoints[0])
                for k, v in self.keypoints.items():

                    point2 = (k, v)
                    
                    if k >= time:
                        break
                    
                    point1 = (k, v)
                a = (point2[1] - point1[1]) / (point2[0] - point1[0])
                b = point2[1] - a*point2[0]

                return a*time + b

            else:
                print("Invalid value '", time, "' for 'time' parameter. Must be between 0 and 1")
                exit()
        else:
            print("There must be at least 2 keypoints")
            exit()

    def set_phase_shift(self, phase_shift):
        self.phase_shift = phase_shift

    def copy(self):
        copy = LinearSpline()
        copy.keypoints = self.keypoints.copy()
        copy.phase_shift = self.phase_shift
        
        return copy
        
        
        
    
