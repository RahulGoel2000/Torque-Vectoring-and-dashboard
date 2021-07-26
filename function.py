'''
Created on tuesday 12 Dec 2019
@aurther: rishabh
contains mathematical functions
'''

from time import monotonic_ns , sleep
import traceback

class integration: #assumes that the value remains constant untill it is changed by the user
        preVal = 0
        preArea =0
        preTime = 0

        def __init__(self, pre=0):#pass in the previous integration value if exists, if none leave blank
                self.preArea = round(pre,3)
                self.preTime = monotonic_ns()
                sleep(0.004)
        def integration(self, val):
                currentTime = monotonic_ns()
                area =round( 0.5*(self.preVal + val)*(currentTime - self.preTime)*10**-9 , 3)
                self.preVal = val
                self.preTime = currentTime
                self.preArea +=area
                return self.preArea

        def perform(self , val):
                return self.integration(val)
'''important to pass on the value at t=0
in the class initialization
'''
class differentiation:
        preVal =0
        preTime = 0

        def __init__(self,val = 0 ):#pass in the value of the function at t=0
                self.preVal = val
                self.preTime = monotonic_ns()
                sleep(0.01)

        def diff(self, val):
                currentTime = monotonic_ns()

                slope = round((self.preVal - val)/((currentTime - self.preTime)*10**-9),3)
                self.preVal = val
                self.preTime = currentTime
                return slope

        def perform(self, val):
                try:
                        return - self.diff(val)
                except:
                        #traceback.print_exc()
                        print("DIFFERENTIATION FUNCTION IS FAILING")
                        self.perform(val)

class util:

        def __init__(self):
            self.filter1_val = 0
            self.filter1_fill = []
        def scale(self, var, input, output ):
            return output[0] + (var - input[0])*(output[1]-output[0])/(input[1] - input[0])

        def filter1(self, val, num =5):
            def filter1_process(list , num ):
                variance_sum = 0
                output = []
                for i in range(num-1):
                    variance_sum += list[i+1] - list[i]
                variance_sum /=5.0
                for i in range(num):
                    output.append(list[0] + variance_sum*i)
                return output


            if(len(self.filter1_fill) <= num):
                self.filter1_fill.append(val)
            if(len(self.filter1_fill) == num):
                out = filter1_process(self.filter1_fill, num)
                self.filter1_val = out[0]
                out.pop(0)
                self.filter1_fill = out
