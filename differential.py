# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 10:19:19 2019

@author: rishabh
"""

import controller
class differential:

        controllerLeft = controller.PID(1,1,1)
        controllerRight = controller.PID(1,1,1)

        def diffSpeed(self,throttle, steeringAngle):##+ve steering angle means right ####### -ve steering angle means left
                return {'r': throttle , 'l':throttle }

        def performDual(self,throttle, speedRight, speedLeft, steeringAngle=0):
                speed = self.diffSpeed(throttle, steeringAngle)

                #right wheel:
                rightInput = self.controllerRight.perform(speed['r'] - speedRight )
                #left wheel:
                leftInput = self.controllerLeft.perform(speed['l'] - speedLeft)

                return {'r': rightInput , 'l':leftInput}

        def performRight(self,throttle, speedRight, steeringAngle=0 , kp=1 , kd = 1 , ki=1):
                speed = self.diffSpeed(throttle, steeringAngle)

                #right wheel:
                rightInput = self.controllerRight.perform(speed['r'] - speedRight , kp ,kd, ki )

                return rightInput

        def performLeft(self,throttle, speedLeft, steeringAngle=0):
                speed = self.diffSpeed(throttle, steeringAngle)

                #left wheel:
                leftInput = self.controllerLeft.perform(speed['l'] - speedLeft)
                return leftInput
