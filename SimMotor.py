# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 19:13:32 2019
contains class for simulating motor output under various conditions
@author: rishabh
"""
import math
import controller
class rotor:
        #motor characteristics
        resistance = 0.5 #in ohm
        reluctance = 1.65 
        impedence = math.sqrt(resistance**2 + reluctance**2)
        radius = 0.07 # in meter
        mass = 5 # in kg
        inertia = 0.5*mass*(radius**2)
        turn = 400
        friction = 0.061 #N-m per ampere
        forceConst = 10
class motor():  
        
        PID = controller.PID(0.05,1,1) 
        x = 0
        def run(self, throttle):
                self.x = self.PID.P(throttle-self.x ) + self.x
                return self.x
                
