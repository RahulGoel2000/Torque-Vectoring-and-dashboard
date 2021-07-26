import RPi.GPIO as GPIO
from time import monotonic_ns , sleep
import threading
# from main import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.IN , pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN , pull_up_down = GPIO.PUD_DOWN)
count=0

start_time = monotonic_ns()
rpmpre = 0
l = []
def elapse_time(channel):
    global start_time , rpmpre ,l
    # print("Its running")
    global count
    print(count)
    count+=1
    o = []
    elapse =0
    rpm = 0
    time = monotonic_ns()
    elapse = time - start_time
    start_time = time
    rpm = (60/(elapse*(10**-9)*24.0))
    # print(round(rpm,1))
    rpmpre = rpm
    if(len(l) < 5):
        l.append(rpm)
    if(len(l) >=5):
        o = process(l)
        #print(o[0])
        o.pop(0)
        l = o
def process(x):
    d = 0
    r = []
    for i in range(4):
        d += x[i+1]-x[i]
        d = d/5.0
    for i in range(5):
        r.append(x[0] + d*i)
    return r
def run():
    GPIO.add_event_detect(18, GPIO.FALLING, callback = elapse_time )

    while(1):

        sleep(1)
run()

# if __name__=='__main__':
#     t1=threading.Thread(target=r)
#     t2=threading.Thread(target=run)
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
