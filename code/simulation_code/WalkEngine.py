import numpy as np
from LinearSpline import LinearSpline


class Leg:
    def __init__(self, phase_shift=0, x_spline=None, y_spline=None, z_spline=None):
        
        self.phase_shift = phase_shift
        self.custom = False
        
        if x_spline == None:
            self.x_spline = LinearSpline()
        else:
            self.x_spline = x_spline
            self.custom = True
            
        if y_spline == None:
            self.y_spline = LinearSpline()
        else:
            self.y_spline = y_spline
            self.custom = True

        if z_spline == None:
            self.z_spline = LinearSpline()
        else:
            self.z_spline = z_spline
            self.custom = True

            
    def getPosAtTime(self, t, dir=None):

        x = 0
        y = 0
        z = 0
        
        if not self.custom:
            if dir != None:

                self.x_spline.add_keypoint(0.125, dir[0]/2)
                self.x_spline.add_keypoint(0.25, dir[0])
                self.x_spline.set_phase_shift(self.phase_shift)
                
                self.y_spline.add_keypoint(0.125, dir[1]/2)
                self.y_spline.add_keypoint(0.25, dir[1])
                self.y_spline.set_phase_shift(self.phase_shift)
                    
                if dir[0] != 0 or dir[1] != 0:
                    # self.z_spline.add_keypoint(0, 0)
                    self.z_spline.add_keypoint(0.125, max(abs(dir[0]), abs(dir[1])))
                    self.z_spline.add_keypoint(0.25, 0)
                    # self.z_spline.add_keypoint(1, 0)
                    self.z_spline.set_phase_shift(self.phase_shift)
                else:
                    self.z_spline = LinearSpline()
                    
        x = self.x_spline.get_value_at_time(t)
        y = self.y_spline.get_value_at_time(t)
        z = self.z_spline.get_value_at_time(t)

            
        return x, y, z
        
class WalkEngine:
    def __init__(self):

        self.dir = [0, 0]
        self.global_phase_shift = 0
        # FRONT LEFT SPLINES
        fl_x_spline = LinearSpline()

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
        
        self.fl = Leg()
        self.bl = Leg(phase_shift=0.5)
        self.br = Leg()
        self.fr = Leg(phase_shift=0.5)

    def changeDir(self, dir, currentTick):
        if self.dir == [0, 0] and dir != [0, 0]:
            self.global_phase_shift = currentTick

        # if dir == [0, 0] and self.dir != [0, 0]:
        #     self.global_phase_shift = currentTick
            # self.fl.finishingStep = True
            # self.fr.finishingStep = True
            # self.bl.finishingStep = True
            # self.br.finishingStep = True

        
        self.dir = dir
        
    def getFLPos(self, t):
        return self.fl.getPosAtTime((t-self.global_phase_shift)%1, dir=self.dir)

    
    def getFRPos(self, t):
        return self.fr.getPosAtTime((t-self.global_phase_shift)%1, dir=self.dir)

    
    def getBLPos(self, t):
        return self.bl.getPosAtTime((t-self.global_phase_shift)%1, dir=self.dir)

    
    def getBRPos(self, t):
        return self.br.getPosAtTime((t-self.global_phase_shift)%1, dir=self.dir)
        
    



