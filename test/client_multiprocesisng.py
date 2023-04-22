import multiprocessing
import GamepadAccess
import socket 
from time import sleep
import pickle
import cv2
import vision
import numpy as np
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
    USB_AK = 0
    USB_W =0
    led = 0             #zmiana stanu ledow => Select
    
    def __bytes__(self):
        return

Data = toSend()
pad=GamepadAccess.padObj()

class passThroughClass:
    dane= '0'
passThrough = passThroughClass()

MAX_VEL = 350       #w jednostkach hoverboarda
NORM_VEL = 200
MIN_VEL = 40
NORM_DIR = 100
MAX_DIR = 200
MIN_DIR = 20
rightDeadZone = 0.2

value = (-0.5,0.5)
W, H = 1280, 720

def sockets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print(f"Connecting to:")

    sock.connect((str("USB.local"), int(8765)))

    print("connected", sock.getsockname())
    
    while True:
        pickled = passThrough.dane
        #print(pickled)
        sock.sendall(pickled)
        sleep(0.05)


def padding():
    while True:
        #pad.ShowDebug()
        if pad.button_X == 0:                                   
            if pad.button_B == 0:                               #B  - przycisk "nitro"
                if abs(pad.leftAxis.y * NORM_VEL) < MIN_VEL:
                    Data.hvbSpeed = 0
                else:
                    Data.hvbSpeed = pad.leftAxis.y * NORM_VEL
                if abs(pad.leftAxis.x * NORM_DIR) < MIN_DIR:
                    Data.hvbDir = 0
                else:
                    Data.hvbDir = pad.leftAxis.x *NORM_DIR
            else:
                if abs(pad.leftAxis.y * MAX_VEL) < MIN_VEL:
                    Data.hvbSpeed = 0
                else:
                    Data.hvbSpeed = pad.leftAxis.y * -MAX_VEL
                if abs(pad.leftAxis.x * MAX_DIR) < MIN_DIR:
                    Data.hvbDir = 0
                else:
                    Data.hvbDir = pad.leftAxis.x *MAX_DIR
            Data.HVB_ARM = pad.buttonStart                    
            Data.led = pad.buttonSelect
            Data.USB_AK = 1 if pad.button_TL and pad.button_TR == 1 else 0
            Data.USB_W = pad.button_Y
            Data.USB_L = 1 if pad.button_A == 1 else 0
            # if pad.axisTL > 0 and pad.axisTL<0.95:
            #     Data.USB_A = 30
            #     Data.USB_B = 30
            #     Data.USB_C = 30
            # if pad.axisTL >=0.95:
            #     Data.USB_A = 30
            #     Data.USB_B = 30
            #     Data.USB_C = 30
            Data.stop = 0
        else:   
            print("Stop")
            Data.stop = 1
            Data.hvbDir = 0
            Data.hvbSpeed = 0
            Data.HVB_ARM = 0
            Data.led = 0
            Data.USB_A = 0
            Data.USB_B = 0
            Data.USB_C = 0
            Data.USB_AK = 0 
            Data.USB_L = 0
            Data.USB_W = 0
        passThrough.dane = pickle.dumps(Data)
def meth():
    max=40
    min = 10
    print("dupa")
    # while not False:
    #     if pad.button_A ==1: 
    #         x= pad.rightAxis.x
    #         y= pad.rightAxis.y
    #         motorA = max
    #         motorB=max
    #         motorC=max
    #         if x>0 and y>0:
    #             motorB=min
    #             print("topRight")
    #         if x<0 and y>0:
    #             motorC =min
    #             print("topLeft")
    #         if x<0 and y<0:
    #             if y/x < 0.57735:
    #                 motorC = min
    #                 print("botLeftLeft")
    #             else:
    #                 motorA=min
    #                 print("botLeftRight")
    #         if x>0 and y<0:
    #             if y/x<-0.55735:
    #                 motorA=min
    #                 print("botRightLeft")
    #             else:
    #                 motorB=min
    #                 print("botLeftLeft")
    #         Data.USB_A = motorA
    #         Data.USB_B = motorB
    #         Data.USB_C = motorC
    #         #print(f"motorA:{motorA}, motorB:{motorB}, motorC:{motorC}")
    #     else:
    #             Data.USB_A = 0
    #             Data.USB_B = 0
    #             Data.USB_C = 0
    while not False:  
        x= pad.rightAxis.x
        y= pad.rightAxis.y
        #if abs(x)>0.15 and abs(y)>0.15:
        
        bias = 30
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
        sleep(.1)
        print(f"motorA:{motorA}, motorB:{motorB}, motorC:{motorC}")
        if pad.axisTL >0.5:
            if motorA and motorB and motorC < 50:
                Data.USB_A = motorA
                Data.USB_B = motorC
                Data.USB_C = motorB
        else:
            Data.USB_A = 0
            Data.USB_B = 0
            Data.USB_C = 0

        


def InitializeVideo():
    cap = cv2.VideoCapture("http://usb.local/stream")

    while True:
        value = (pad.rightAxis.x, pad.rightAxis.y)
        _, frame = cap.read()
        new_value = (int((1+value[0])*(W/2)), int((1+value[1])*(H/2)))
        mid_value = (int((W/2+new_value[0])/2), int((H/2+new_value[1])/2))
        frame = cv2.arrowedLine(frame, mid_value, new_value, (0,255,0), int(2))
        frame = cv2.line(frame, (int(W/2-10), int(H/2)), (int(W/2+10), int(H/2)), (255,255,255), int(2))
        frame = cv2.line(frame, (int(W/2), int(H/2-10)), (int(W/2), int(H/2+10)), (255,255,255), int(2))
        cv2.imshow('sas', frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

from multiprocessing import Process


if __name__ == "__main__":  # confirms that the code is under main function
    procs = []
    pad_proc = Process(target=pad.Initialize)  # instantiating without any argument
    padding_proc = Process(target=padding)
    video_proc = Process(target = InitializeVideo)
    procs.append(pad_proc, padding_proc, video_proc)
    pad_proc.start()
    padding_proc.start()
    video_proc.start()

    # complete the processes
    for proc in procs:
        proc.join()

# controllerThread = threading.Thread(target = pad.Initialize)
# controllerThread.start()
# socketsThread = threading.Thread(target=sockets)
# socketsThread.start()
# paddingThread = threading.Thread(target=padding)
# paddingThread.start()
# video = threading.Thread(target=InitializeVideo)
# video.start()
# methThread = threading.Thread(target=meth)
# methThread.start()
    
