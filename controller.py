# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 20:45:30 2019
contains general PID
@author: rishabh
"""
import function
import sensor
sensor = sensor.sensor()
class PID:
        kp, ki, kd = 0 ,0 ,0
        #inte = None
        diff = None
        anti_wind = 0
        preD = 0
        D_tuner = 0.24
        inte = function.integration()
        def __init__(self , p=0,i=0,d=0 ,val = 0, anti_wind = 1023):
                self.kp = p
                self.ki = i
                self.kd = d
                self.anti_wind = anti_wind
                #self.inte = func.integration() #### in future can put in the value so that if the system revives from a crash is starts from the last checkpoint.
                self.diff = function.differentiation(val)
                #self.__init__(p,i,d,val,anti_wind)
        def P(self,val):
                return self.kp*val

        def I(self,val):
               if self.anti_wind >=0:
                       if (self.inte.preArea < self.anti_wind and self.inte.preArea >=0 and val>0) or (self.inte.preArea > 0  and val <0):
                               return self.inte.perform(val)*self.ki
                       else:
                               return self.inte.preArea*self.ki
               else:
                       return self.inte.perform(val)*self.ki
               return self.inte.perform(val)

        def D(self, val):
                d = self.diff.perform(val)
                d = (d-self.preD)*self.D_tuner + self.preD
                self.preD = d
                return d*self.kd

        def perform(self,val,kp=1,ki=1,kd=1):
                return self.P(val)*kp + self.I(val)*ki + self.D(val)*kd


class fuzzy:

        def __init__(self):
            self.addon = 0
            self.D_tuner = 0.24
            self.preD = 0
            self.anti_wind = 1023
            self.inte = function.integration()
            self.diff = function.differentiation(0)
            self.fn = function.util()
        def I(self,val):
               if self.anti_wind >=0:
                       if( self.anti_wind < self.inte.preArea and val > 0) or ( self.inte.preArea < 0 and val < 0):
                               return self.inte.preArea
                       else:
                               return self.inte.perform(val)

        def D(self, val):
               d = self.diff.perform(val)
               self.fn.filter1(d,5)
               self.preD = self.fn.filter1_val
               return self.preD
        def performPD(self, val, p ):
               if (self.addon < 0 and val < 0):
                 self.addon = 0
                 return self.addon
               else:
                 self.addon +=(val*self.D(val)*p)
                 return self.addon
        def perform(self, val, p ,i,d,anti_wind= 1023):
               if ((self.addon <= 0 and val < 0)):
                 self.addon = 0
                 return self.addon
               else:
                 self.addon += (val*p + self.I(val)*i + self.D(val)*d)
                 return self.addon

if __name__ == '__main__':
        import random
        c = PID(p=1,i=1,d=1)
        intg = function.integration()
        for i in range(5):
                print(intg.perform(random.randrange(1,10)))
                sleep(0.01)
