from functions import function
import random
import time
import smbus
bus = smbus.SMBus(1)
func = function()
class e_differential:

    #variable declaration
    KP = None
    KI = None
    KD = None
    integration_right = 0
    integration_left = 0
    diff_right = 0
    diff_left = 0
    input_right_pre = 0
    input_left_pre = 0
    time_pre = 0
    def __init__(self, kp , ki , kd):#class initialization.
        self.KP = kp
        self.KI = ki
        self.KD = kd

    def rpm(self):#returns rpm values in form of dictionary


        speed_rear_right = random.randrange(10 ,50)#(MSB_rear_right*100 + LSB_rear_right)/100.0
        speed_rear_left = random.randrange(10 ,50)#(MSB_rear_left*100 + LSB_rear_left)/100.0
        return {"RR" : speed_rear_right , "RL" : speed_rear_left , "time" : time.monotonic()}

    def throttle(self):
        '''if(bus.read_byte(0x05) == 1):
            MSB_throttle = bus.read_byte(0x05)
        if(bus.read_byte(0x05) == 0):
            LSB_throttle = bus.read_byte(0x05)

        throttle_val = (MSB_throttle*100 + LSB_throttle)

                if(bus.read_byte(0x03) == 1):
                    MSB_rear_right = bus.read_byte(0x03)
                if(bus.read_byte(0x03) == 0):
                    LSB_rear_right = bus.read_byte(0x03)

                if(bus.read_byte(0x04) == 1):
                    MSB_rear_left = bus.read_byte(0x04)
                if(bus.read_byte(0x04) == 0):
                    LSB_rear_left = bus.read_byte(0x04)
        '''
        return 230#throttle_val#returns throttle value
    def differential(self):
        speed = self.rpm()
        throttle = self.throttle()
        input_right = throttle - speed["RR"]
        input_left = throttle - speed["RL"]
        time = speed["time"]
        time_gap = time - self.time_pre
        self.time_pre = time
        self.integration_right = func.integration(self.integration_right, (input_right+self.input_right_pre) , time_gap )
        diff_temp_right = func.differention((input_right-self.input_right_pre) , time_gap)
        self.diff_right = (diff_temp_right - self.diff_right)*0.6 +self.diff_right

        self.integration_left = func.integration(self.integration_left ,(input_left+self.input_left_pre) , time_gap )
        diff_temp_left = func.differention((input_left-self.input_left_pre) , time_gap)
        self.diff_left = (diff_temp_left - self.diff_left)*0.6 +self.diff_left

        self.input_right_pre = input_right
        self.input_left_pre = input_left

        out_right = self.KP*input_right + self.KI*self.integration_right + self.KD*self.diff_right
        out_left = self.KP*input_left + self.KI*self.integration_left + self.KD*self.diff_left
        print(str(input_left) + " " + str(self.integration_left) + " " + str(str(self.diff_left)))
        return {"left":out_left , "right" : out_right}
