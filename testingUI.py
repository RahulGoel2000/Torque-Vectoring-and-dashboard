# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 05:33:06 2019

@author: rishabh
"""

from tkinter import *
from time import sleep


class UI_screen():
    max_fill = None

    def __init__(self):
        self.master = Tk()
        self.master.geometry('800x410')


class bar:
    def __init__(self, master, canvas, pos, width):
        self.master = master
        self.canvas = canvas
        self.position = pos
        self.width = width

    def line(self, x, y, col):
        # self.canvas.create_oval(x-1 , y-1 ,x+1 , y+1,width = 1, outline = "white" ,fill = "white")
        self.canvas.create_line((x, y), fill=col)

    def point(self, x, y, col):
        self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, width=1, outline=col, fill=col)

    def rect(self, x, y, col):
        self.canvas.create_rectangle(x, y, outline=col, fill=col)

    def perform(self, val, col):
        bottom = self.position[0] + self.width, self.position[1]
        top = self.position[0], self.position[1] - val
        self.rect(top, bottom, col)


''' to use this class, pass in the root, canvas and the postion of origin '''


class plot:
    import random

    def __init__(self, master, canvas, pos, maxi):
        self.position, self.canvas = pos, canvas

        '''self.canvas = Canvas(master = master)
		self.canvas["height"] = geometry[1]
		self.canvas["width"]  = geometry[0]
		self.canvas["bg"] = "black"
		self.canvas.pack()'''
        self.math = mat()

        ############ variable declaration#################
        self.value_list = []
        self.max_fill = maxi

    # self.point(25,25)

    def line(self, x, y, z, a, col):
        # self.canvas.create_oval(x-1 , y-1 ,x+1 , y+1,width = 1, outline = "white" ,fill = "white")
        self.canvas.create_line(x, y, z, a, smooth="true", fill=col)

    def valueInput(self, val):
        self.value_list.append(val)
        ret = False
        if len(self.value_list) > self.max_fill:
            self.value_list.pop(0)
            ret = True
        return ret

    def perform(self, val, txt):
        # self.canvas.delete('all')
        # self.valueInput(val)
        if self.valueInput(val):
            for i in range(0, self.max_fill - 3, 3):
                a = (self.position[0] + i * 5, self.position[1] - 5 * self.value_list[i])
                b = (self.position[0] + (i + 1) * 5, self.position[1] - 5 * self.value_list[i + 1])
                c = (self.position[0] + (i + 2) * 5, self.position[1] - 5 * self.value_list[i + 2])
                d = (self.position[0] + (i + 3) * 5, self.position[1] - 5 * self.value_list[i + 3])
                self.line(a, b, c, d, txt)

                '''for j in range(i*10,i*10+10 ,1):
                                        self.line((self.position[0]+j,self.math.quadInterpolation(a,b,c,self.position[0] + j)) ,
                                                   (self.position[0]+j+1,self.math.quadInterpolation(a,b,c,self.position[0] + j+1)) ,
                                                   txt)'''

        else:
            self.valueInput(val)


class mat:
    def quadInterpolation(self, a, b, c, x):
        x1, x2, x3 = a[0], b[0], c[0]
        y1, y2, y3 = a[1], b[1], c[1]
        y1 = a[1]
        y2 = b[1]
        y3 = c[1]
        return int((((x - x2) * (x - x3)) / ((x1 - x2) * (x1 - x3))) * y1 +
                   (((x - x1) * (x - x3)) / ((x2 - x1) * (x2 - x3))) * y2 +
                   (((x - x1) * (x - x2)) / ((x3 - x1) * (x3 - x2))) * y3)


if __name__ == '__main__':
    import random, math
    from time import sleep, monotonic
    import threading

    geometry = 1800, 1000
    master = Tk()
    canvas = Canvas(master=master)
    canvas["height"] = geometry[1]
    canvas["width"] = geometry[0]
    canvas["bg"] = "black"
    canvas.pack()

    start = monotonic()
    plotter = plot(master, canvas, (0, 200), 2 * 180)
    plotter1 = plot(master, canvas, (0, 200), 2 * 180)
    plotter2 = plot(master, canvas, (0, 200), 180)
    plotter3 = plot(master, canvas, (0, 200), 180)
    master.update()

    while 1:
        plotter.perform(10 * math.sin(monotonic() * 20), 'blue')
        plotter1.perform(10 * math.cos(monotonic() * 20), 'red')
        # plotter2.perform(10*math.tan(monotonic()*20) , 'yellow')
        # plotter3.perform(10*math.cos(math.pi/4- monotonic()*20) , 'white')

        # sleep(0.005)
        master.update()
        canvas.delete('all')
        if (monotonic() - start > 2):
            master.quit()

    '''bar0 = bar(master ,canvas , (50 , 200) , 50)
        bar1 = bar(master ,canvas , (100 , 200) , 10)
        while 1:
               bar0.perform(100*math.sin(monotonic()*3) , 'blue')
               bar1.perform(100*math.sin(monotonic()*2) , 'yellow')
               master.update()
               canvas.delete('all')'''
    print("yy")
    master.mainloop()
    master.destroy()
