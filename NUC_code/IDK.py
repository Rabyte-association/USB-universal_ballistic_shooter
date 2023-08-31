import pickle
from time import sleep
from serial import Serial
import socket
import threading
import cv2
import numpy as np
import imutils
import math
class toSend:
    HVB_ARM = 0  #przekaźnik zasilania hvb, zmiana chwilowa => start
    stop = 0        #stop ruchu silnikow chwytaka => X
    hvbSpeed = 0
    hvbDir = 0
    USB_A =0
    USB_B =0 
    USB_C =0
    USB_L =0
    USB_AUT = 0
    USB_AK = 0
    USB_W =0
    led = 0             #zmiana stanu ledow => Select
    
    def __bytes__(self):
        return

class DataHold:
    data = ""
class passThroughAimClass:
    x=0
    y=0
    a=0
    b=0
    c=0
passThroughAim = passThroughAimClass()

datahold = DataHold()
datahold.data = ""
old_decoded = None
xiaoID = '0'
picoID = '2'

def InitializeSocket(PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('usb.local', PORT))
    print(f"elo, {s.getsockname()}")
    while True:
        s.listen()
        conn, addr = s.accept()
        print('Connected by', addr)
        while True:
            try:
                datahold.data = conn.recv(4096)
                #print(datahold.data)
                if datahold.data == b'':
                    break
            except:
                print('server error')
                break
        datahold.data = b''

def InitializeACM(): # xiao do jazdy, pico do strzalow
    serialpico = Serial(port='/dev/ttyACM'+picoID, baudrate=115200, timeout=None)
    serialxiao = Serial(port='/dev/ttyACM'+xiaoID, baudrate=115200, timeout=0.1)
    while True:
        #print("lol")
        if len(datahold.data)>2:
            try:
                decoded = pickle.loads(datahold.data)
                if decoded.USB_L == 1 and old_decoded.USB_L == 0:
                    serialpico.write(bytes('l', 'utf-8'))
                if decoded.USB_AK == 1 and old_decoded.USB_AK == 0:
                    serialpico.write(bytes('q', 'utf-8'))
                if decoded.USB_AUT == 1:
                    serialpico.write(bytes('a' + str(passThroughAim.a), 'utf-8'))
                    serialpico.write(bytes('b' + str(passThroughAim.b), 'utf-8'))
                    serialpico.write(bytes('c' + str(passThroughAim.c), 'utf-8'))
                else:
                    serialpico.write(bytes('a' + str(decoded.USB_A), 'utf-8'))
                    serialpico.write(bytes('b' + str(decoded.USB_B), 'utf-8'))
                    serialpico.write(bytes('c' + str(decoded.USB_C), 'utf-8'))
                  #  print(decoded.USB_A)
                if decoded.stop == 1:
                    serialxiao.write(bytes('s', 'utf-8'))
                    serialpico.write(bytes('s', 'utf-8'))
                if decoded.USB_W == 1 and old_decoded.USB_W == 0:
                    serialpico.write(bytes('w4', 'utf-8'))
                serialxiao.write(bytes('h' + str(decoded.HVB_ARM), 'utf-8'))
                serialxiao.write(bytes('l' + str(decoded.led), 'utf-8'))
                serialxiao.write(bytes('x' + str(decoded.hvbSpeed), 'utf-8'))
                serialxiao.write(bytes('t' + str(decoded.hvbDir), 'utf-8'))
                old_decoded = decoded
               # print(decoded.USB_A)
            except:
                 print("err")
                #print(datahold.data)
            #     decoded = b''
def meth():
    while not False:  
        x=passThroughAim.x
        y=passThroughAim.y     
        bias = 60
        ApreCodedX = 0
        ApreCodedY = 2
        BpreCodedX = -1.732
        BpreCodedY = -1
        CpreCodedX = 1.732
        CpreCodedY = -1
        d1 = math.sqrt(((ApreCodedX-x)**2)+((ApreCodedY-y)**2))
        d2 = math.sqrt(((BpreCodedX-x)**2)+((BpreCodedY-y)**2))
        d3 = math.sqrt(((CpreCodedX-x)**2)+((CpreCodedY-y)**2))
        motorA = bias/d1
        motorB= bias/d2
        motorC= bias/d3
        #  print(f"motorA:{motorA}, motorB:{motorB}, motorC:{motorC}")
        if motorA and motorB and motorC < 50:
            passThroughAim.a = motorA
            passThroughAim.b = motorC
            passThroughAim.c = motorB

        lol= None

# def someVideo():
#     cap = cv2.VideoCapture("http://usb.local/stream")
#     cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
#     overlay = np.zeros([1080,1920,3], dtype=np.uint8)

#     old_point = None
#     while True:
#         _, frame = cap.read()
#         hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#       #  cv2.imshow("Frame", frame) # video + circle
#         # orange
#         #low = np.array([0, 169, 164])
#         #high = np.array([35, 255, 255])
#         low = np.array([28, 80, 130])
#         high = np.array([41, 255, 255])
#         mask = cv2.inRange(hsv_frame, low, high)
#         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         cnts = imutils.grab_contours(cnts)
#         center = None

#         # center
#         try:
#             rad = 1
#             if len(cnts) > 0:
#                 c = max(cnts, key=cv2.contourArea)
#                 ((x, y), radius) = cv2.minEnclosingCircle(c)
#                 M = cv2.moments(c)

#                 x=int(M["m10"] / M["m00"])
#                 y=int(M["m01"] / M["m00"])
#                 if radius>10:
#                     passThroughAim.x = map(x, 0, 1920, -1, 1)
#                     passThroughAim.y = map(y, 0, 1080, -1, 1)
#                     print(passThroughAim.x)
#                 center = x,y    
#                 rad = radius
#         except:
#             nlol=None

if __name__ == "__main__":
    acm = threading.Thread(target=InitializeACM)
    acm.start()
    port = threading.Thread(target=InitializeSocket, args=[8766])
    port.start()
    methThread = threading.Thread(target=meth)
    methThread.start()
    # vidThread = threading.Thread(target=someVideo)
    # vidThread.start()
