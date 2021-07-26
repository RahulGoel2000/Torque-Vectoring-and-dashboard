# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 21:15:05 2019

@author: rishabh
"""
from time import sleep
import traceback
from tkinter import *
import threading , differential , sensor, controller , Adafruit_MCP4725
from testingUI import plot
geometry = 1000 , 800
master = Tk()
canvas = Canvas(master = master)
canvas["height"] = geometry[1]
canvas["width"]  = geometry[0]
canvas["bg"] = "black"
canvas.pack()


plotter = plot(master , canvas ,(100,700) , 70)
plotter1 = plot(master , canvas ,(100,700), 70)
plotter2 = plot(master , canvas ,(30,400), 70)




count=0
running =False




controller_left = controller.fuzzy()
controller_right = controller.fuzzy()
sensor = sensor.sensor()

dac_left = Adafruit_MCP4725.MCP4725(address = 0x61)
dac_right = Adafruit_MCP4725.MCP4725(address = 0x60)
lock = threading.Lock()

speed = 0
#0.3 , 0.06 , 0.5
# 0.7, 0.6, 0.6
 #0.4,0.18,0.2
kp,ki,kd = 0.4,0,0.3 ###red
kpr , kir , kdr = 0.45 , 0 ,0.3
k = 0.001
def mapx(p):
    return (p+1)/(2*(p+2))
def x(a):
    if a> 0:
        return a
    else:
        return 0
def vehicle():
        global speed, sensor, differential, motor,dac_left , dac_right, kp ,ki,kd,fuzzy

        ############### updating the sensor values ################
        lock.acquire()
        sensor.val_update()
        lock.release()
        ###################### sensor values updated #######################

        ###################### setting up control loop for speed control####################
        v_left =  int(controller_left.perform((sensor.throttleVal - sensor.leftSpeedVal ) , p = kp,i = ki , d = kd))
        v_right = int(controller_right.perform((sensor.throttleVal - sensor.rightSpeedVal ) , p = kpr,i = kir , d = kdr))

        ########################### setting up values for DAC ################################
        dac_left.set_voltage(int(x(v_left+655)))
        #sleep(0.01)
        dac_right.set_voltage(int(x(v_right+655)))

        ############################ storing data in txt file #################################
        with open("data.txt" , "a") as file:
            file.write(str(sensor.throttleVal) + "  " + str(sensor.rightSpeedVal) + "\n")


        ################ printing desired values onto the terminal ###################
        '''print(v_left, " | ", round((x((v_left+655))/4096)*5,1), " | "  ,
                    round(sensor.leftSpeedVal,1) , " | "
                     ,abs(round(sensor.throttleVal ,1)), " | "
                     ,abs(round(sensor.fc.filter1_val ,1)), " | "
                     , round((sensor.throttleVal- sensor.rightSpeedVal)*kp , 1), " | ",
                     round(controller_left.inte.preArea*ki,1), " | "
                      , round(controller_left.preD*kd,1), " | ",
                       kp, "  ", ki,"  ", kd)'''
        '''print(v_right, " | ", round((x((v_right+655))/4096)*5,1), " | "  ,
                    round(sensor.rightSpeedVal,1) , " | "
                     ,abs(round(sensor.throttleVal ,1)), " | "
                     ,abs(round(sensor.fc.filter1_val ,1)), " | "
                     , round((sensor.throttleVal- sensor.rightSpeedVal)*kp , 1), " | ",
                     round(controller_right.inte.preArea*ki,1), " | "
                      , round(controller_right.preD*kd,1), " | ",
                       kp, "  ", ki,"  ", kd)'''

        print(v_right, " | ",v_left, " | " ,
                    round(sensor.rightSpeedVal,1) , " | ",
                    round(sensor.leftSpeedVal,1) , " | "
                     ,abs(round(sensor.throttleVal ,1)), " | "
                     , kp, " ", ki," ", kd,"    ", kpr, " ", kir," ", kdr)

        plotter.perform(sensor.rightSpeedVal/1.5 , 'blue')
        plotter1.perform(sensor.leftSpeedVal/1.5 , 'red')
        #plotter2.perform((sensor.rightSpeedVal-sensor.leftSpeedVal)/1.5 , 'yellow')

        #sleep(0.005)
        master.update()
        canvas.delete('all')
def r():
        global controller,running
        while 1:
            try:
                vehicle()
                #sleep(0.03)
            except:
                #traceback.print_exc()
                print("error in r()")
                r()


def update():
        global sensor, meter,plot
        while(1):
            plot.value = int(sensor.rightSpeedVal)
            plot.th = (int(sensor.throttleVal))

r()
