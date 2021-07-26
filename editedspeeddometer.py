import pygame
import math
import random
from time import sleep
from time import monotonic
import time
import datetime
import csv
myFile = open('123.csv', 'a+')

rightSpeedVal , leftSpeedVal = 0, 0

count_pre , count_sum, count = 0,0,0

pygame.init()
size = 800,410
start= monotonic()
speed = 10
speedMax = 40
currentList = [] #max number of values that will be plotted
countLeft = 0
countRight =0
count = 0
val = 0
currentMaxlist = 20
leftTurn = False
rightTurn = False
screen = pygame.display.set_mode(size)
run = True
fontDistance = pygame.font.Font(pygame.font.get_default_font(),50)
fontTime = pygame.font.Font(pygame.font.get_default_font(), 36)
fontSpeed = pygame.font.Font(pygame.font.get_default_font(),90)

def filler(val):##for filling up values into the currentList
    global currentList
    if(len(currentList) >= currentMaxlist):
        currentList.pop(0)
    currentList.append(val)
    sleep(0.05)
def listPlotter(surface , input):
    global currentMaxlist
    currentPostion = (600 , 70)
    def quadInterpol(a,b,c , x):
        x1 = a[0]
        x2 = b[0]
        x3 = c[0]
        y1 = a[1]
        y2 = b[1]
        y3 = c[1]
        return int((((x-x2)*(x-x3))/((x1-x2)*(x1-x3)))*y1 +
    (((x-x1)*(x-x3))/((x2-x1)*(x2-x3)))*y2 +
    (((x-x1)*(x-x2))/((x3-x1)*(x3-x2)))*y3)
    col=0
    for i in range(currentMaxlist-3):
        a = (currentPostion[0] + i*10     , currentPostion[1]-5*input[i])
        b = (currentPostion[0] + (i+1)*10 , currentPostion[1]-5*input[i+1])
        c = (currentPostion[0] + (i+2)*10 , currentPostion[1]-5*input[i+2])
        for j in range(i*10,i*10+10,1):
            pygame.draw.circle(surface, (int(255*col/175),0,0),
                               (currentPostion[0]+j,quadInterpol(a,b,c,currentPostion[0] + j)),1)
            col+=1

def plotter(surface,val=0):
    global currentList
    global count
    filler(val)
    if count < currentMaxlist-1:
            count+=1
            return
    else:
        listPlotter(surface , currentList)


def clock(surface):
    global start

    sec = int(monotonic() - start)
    time =  str(int(sec/60)) + " : " + str(sec%60)
    textTime = fontTime.render( time, 1,(255,255,255))
    surface.blit(textTime , (370,360))
    return time
    
def distance(surface, distance):
    textDistance = fontDistance.render(str(round(distance,2)) , 1 , (255,255,255))
    surface.blit(textDistance , (360 , 280))

def speedDial(surface,speed):
    global speedMax

    line = pygame.draw.line
    center = 400, 205
    radius = 133
    gap = 12
    if speed == 0 :#|| speed == speedMax:
        return 0
    def colorInterpol(speed):
        global speedMax
        if speed > speedMax:
            speed = speedMax
        color1 = (0,0,0)
        color2 = (230,0,0)
        rg = color2[0] - color1[0]
        gg = color2[1] - color1[1]
        bg = color2[2] - color1[2]
        ans = ( color1[0] + int(rg*speed/speedMax), color1[1] + int(gg*speed/speedMax), color1[2] + int(bg*speed/speedMax))
        return ans
    def radialPoint(teta , center , radius):
        return center[0] + int(radius*math.cos(math.pi - teta*math.pi/180.0)) ,center[1] - int(radius*math.sin(math.pi -teta*math.pi/180.0))

    val =360
    for i in range(speed*10):
        d = speed*220/speedMax
        if i < speed*10 -1:
            line(surface,(int(251*i/2/val)%255,int(255-251*i/2/val)%255,int(255-251*i/val)%255) ,
                 radialPoint(-39.8 + i*d/(speed*10),center ,radius),
                 radialPoint(-39.8 + i*d/(speed*10),center ,radius+gap),4 )
        else:
             for j in range(20):
                pygame.draw.circle(surface , (int(255*j/20) , 0,0),radialPoint(-39.8 + i*d/(speed*10) , center , 60+3*j),2)

    textSpeed = fontSpeed.render(str(speed), 1 , (255,255,255))
    surface.blit(textSpeed, (358 , 140))


def main():
  
        d1=0

        global countRight
        global countLeft
        global run
        global speed, val
        bg = pygame.image.load("speedometer5.jpg")
        rightArrow = pygame.image.load("rightarrow.jpg")
        leftArrow = pygame.image.load("leftarrow.jpg")
        headlights=pygame.image.load("headlights.png")
        t1=time.time_ns()
        c=0
        
        while run:

            val = speed
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False
            keys = pygame.key.get_pressed()
            leftTurn = False
            rightTurn = False
            if keys[pygame.K_UP]:
                speed +=2
            if keys[pygame.K_DOWN]:
                speed -=2
            if keys[pygame.K_LEFT]:
                leftTurn = True
            screen.blit(leftArrow ,(212,0))
            if keys[pygame.K_RIGHT]: 
                rightTurn = True
            screen.blit(bg,(0,0))
            if leftTurn is True:
                if(countLeft%8 ==0):
                     screen.blit(leftArrow ,(212 ,0))
                     countLeft +=1
            if rightTurn is True:
                if(countRight%8 ==0):
                     screen.blit(rightArrow ,(438, 0))
                countRight +=1
            time2=clock(screen)
            t2=time.time_ns()
            second_elepsed=(t2-t1)/10**9/3600/2
            # differene=second_elepsed.total_seconds()
            # hour=second_elepsed/3600
            d1=d1+val*second_elepsed
            print(val,d1,second_elepsed)
            distance(screen,d1)
            plotter(screen,val)
            speedDial(screen,val)
            pygame.time.delay(50)
            pygame.display.update()
            c+=1
            if c==5:
                t1=time.time_ns()
                c=0
        pygame.display.quit()
        return 1





if __name__ == '__main__':

        main()
