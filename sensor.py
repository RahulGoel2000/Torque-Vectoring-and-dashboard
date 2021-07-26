# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 05:42:38 2019
contains the address , values from the sensor.
########### call val_update() to update variables
@author: rishabh
"""
import smbus
import random
import function
bus = smbus.SMBus(1)
import traceback
class sensor:
        addr_right = 0x06
        addr_left = 0x08
        addr_throttle = 0x07

        rightSpeedVal , leftSpeedVal = 0, 0

        count_pre , count_sum, count = 0,0,0

        fc = function.util()


        def rightSpeed(self):
                MSB_rear_right=0
                LSB_rear_right=0
                try:
                    for i in range(3):
                        val = bus.read_byte(0x06)
                        if(val >> 7 == 1):
                            MSB_rear_right = (val& 0b01111111)
                        elif(val>>6 == 0):
                            LSB_rear_right = val
                        elif(val>>6 == 1):
                            self.count = (val & 0b00111111)
                    if self.count_pre > self.count:
                        self.count_sum += self.count
                    else:
                        self.count_sum += (self.count-self.count_pre)
                    self.count_pre = self.count
                    self.rightSpeedVal = MSB_rear_right*10 + LSB_rear_right

                except:
                        #traceback.print_exc()
                        print("RIGHT WHEEL FAILING")
                        self.rightSpeed()

        def leftSpeed(self):
                MSB_rear_left=0
                LSB_rear_left=0
                try:
                    for i in range(3):
                        val = bus.read_byte(0x08)
                        if(val >> 7 == 1):
                            MSB_rear_left = (val& 0b01111111)
                        elif(val>>6 == 0):
                            LSB_rear_left = val

                    self.leftSpeedVal = MSB_rear_left*10 + LSB_rear_left

                except:
                        #traceback.print_exc()
                        print("LEFT WHEEL FAILING")
                        self.leftSpeed()

        throttleVal, throttleValPre , throttleValRaw = 0,0,0
        slope_throttle_pre =0
        diff_throttle = function.differentiation(0)
        def throttle(self):
                MSB_throttle , LSB_throttle = 0,0

                ##########updating MSB and LSB values for throttle from I2C##################
                try:
                    for i in range(2):
                        val = bus.read_byte(0x07)
                        if(val >> 7 == 0):
                            MSB_throttle = (val)
                        elif(val>>7 == 1):
                            LSB_throttle = (val & 0b01111111)
                ############## combining MSB and LSB #################
                        self.throttleValRaw =(MSB_throttle*100 + LSB_throttle)
                ############# applying level two filter ###############
                        self.fc.filter1(self.throttleValRaw , 5)

                        self.throttleVal = self.fc.scale((self.fc.filter1_val), (212, 858 ),(0,400))
                except:
                        #traceback.print_exc()
                        print("THROTTLE IS FAILING")
                        #self.throttle()

        def update(self):###call this function to update the sensor values.
                self.rightSpeed()
                self.leftSpeed()
                self.throttle()
        def val_update(self):
                try:
                        self.update()
                except:
                        print("SENSOR UPDATE IS FAILING")
                        self.val_update()
