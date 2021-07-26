# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 08:15:27 2019

@author: rishabh
"""

import pygame as pg

class setup:
        display_size = 800,540
        screen = None
        def __init__(self):
                pg.init()
                self.screen = pg.display.set_mode(self.display_size)

class function:
        val_list = []
        val_list_max = 30
        
        counter = 0
        def filler(self, val):
                if len(self.val_list) >= self.val_list_max:
                        self.val_list.pop(0)
                self.val_list.append(val)
                
                
        def quadInterpol(self,a,b,c, x):
                
                x1, x2, x3 = a[0], b[0], c[0]
                y1, y2, y3 = a[1], b[1], c[1]
               
                return int((((x-x2)*(x-x3))/((x1-x2)*(x1-x3)))*y1 +
                            (((x-x1)*(x-x3))/((x2-x1)*(x2-x3)))*y2 +
                            (((x-x1)*(x-x2))/((x3-x1)*(x3-x2)))*y3)
                
        def graph(self, surface, input,graphPosition,scale):
            col=0
            for i in range(self.val_list_max-3):
                a = (graphPosition[0] + i*10     , graphPosition[1]-scale*input[i])
                b = (graphPosition[0] + (i+1)*10 , graphPosition[1]-scale*input[i+1])
                c = (graphPosition[0] + (i+2)*10 , graphPosition[1]-scale*input[i+2])
                for j in range(i*10,i*10+10,1):
                           # pg.draw.circle(surface, (int(255*col/175),0,0),
                                           #(graphPosition[0]+j,self.quadInterpol(a,b,c,(graphPosition[0] + j))),1)
                            pg.draw.line(surface, (int(255*col/((self.val_list_max-3)*10.5)),0,0), (graphPosition[0]+j,self.quadInterpol(a,b,c,(graphPosition[0] + j))),
                                         (graphPosition[0]+j,self.quadInterpol(a,b,c,(graphPosition[0] + j+1))),  2)
                            
                            col+=1
            return
            
        def plot(self,surface, value, graphPosition,scale):
                 self.filler(value)
                 if self.counter < self.val_list_max:
                         self.counter+=1
                         return
                 else:
                         self.graph(surface, self.val_list , graphPosition,scale)
                         
                 
                 
class run:
        fc = function()
        setup = setup()
        
        
        running = True
        value=0
        th =0
        def perform(self, graphPosition,scale):
                while self.running:
                        for event in pg.event.get():
                                if event.type == pg.QUIT:
                                    self.running = False
                        self.setup.screen.fill((0,0,0))
                        self.fc.plot(self.setup.screen, self.value, graphPosition, scale)
                        pg.draw.line(self.setup.screen , (255,0,0), (100 , graphPosition[1] - scale*self.th) , (300 , graphPosition[1] - scale*self.th), 2)
                        #print(self.value)
                        pg.time.delay(50)
                        pg.display.update()
                pg.display.quit()