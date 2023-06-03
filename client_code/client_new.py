from multiprocessing import Process
import GamepadAccess
import socket 
from time import sleep
import pickle
import threading
import cv2
import vision
import numpy as np
import math
import mediapipe as mp
import imutils 
import random
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

Data = toSend()

pad=GamepadAccess.padObj()

class passThroughClass:
    dane= '0'
class passThroughAimClass:
    x=0
    y=0
passThroughControl = passThroughClass()
passThroughAim = passThroughAimClass()

MAX_VEL = 350       #w jednostkach hoverboarda
NORM_VEL = 200
MIN_VEL = 40
NORM_DIR = 100
MAX_DIR = 200
MIN_DIR = 20
rightDeadZone = 0.2

value = (-0.5,0.5)
W, H = 1920, 1080

def sockets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print(f"Connecting to:")

    sock.connect((str("USB.local"), int(8766)))

    print("connected", sock.getsockname())
    
    while True:
        pickled = passThroughControl.dane
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
            if pad.axisTL > 0.5:
                norn = None
            else:
                Data.USB_A = 0
                Data.USB_B = 0
                Data.USB_C = 0
            Data.stop = 0
            Data.USB_AUT = 0
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
            Data.USB_AUT=0
            Data.USB_W = 0
        passThroughControl.dane = pickle.dumps(Data)
def meth(): #algoytm rudolfowy
    while not False:  
        # x= pad.rightAxis.x
        # y=pad.rightAxis.y 
        try:
            x=passThroughAim.x
            y=passThroughAim.y     
            bias = 50
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
                    print("firin in da hole")
                    Data.USB_B = motorC
                    Data.USB_C = motorB
            else:
                Data.USB_A = 0
                Data.USB_B = 0
                Data.USB_C = 0
        except:
            lol= None

        


def stupid_video():
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


# Declaring MediaPipe objects
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils
# IMG_W = 1920
# IMG_H = 1080

# # Processing the input image
# def process_image(img):
#     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(gray_image)
#     # print(results.multi_hand_landmarks)
#     return results

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
# # Drawing landmark connections
# def draw_hand_connections(img, results):
#     if results.multi_hand_landmarks:
#         x= results.multi_hand_landmarks[0].landmark[0].x
#         y= results.multi_hand_landmarks[0].landmark[0].y
#         h, w, c = img.shape
#         cx, cy = int(x* w), int(y * h)
#         passThroughAim.x = map(cx, 0, 1920, -1, 1)
#         passThroughAim.y = map(cy, 1080, 0, -1, 1)
#         # # for handLms in results.multi_hand_landmarks:
        
#         # #     for id, lm in enumerate(handLms.landmark):
                
#         cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
#         return img


# def smart_video():
#     cap = cv2.VideoCapture("http://usb.local/stream")
#     while True:
#         success, image = cap.read()

#         #cv2.imshow("test", image)
#        # image = imutils.resize(image, width=1280, height=500)
#         results = process_image(image)
#         draw_hand_connections(image, results)

#         cv2.imshow("Hand tracker", image)

#         if cv2.waitKey(1) == ord('q'):
#             cap.release()
#             cv2.destroyAllWindows()
def someVideo():
    cap = cv2.VideoCapture("http://usb.local/stream")
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    overlay = np.zeros([1080,1920,3], dtype=np.uint8)

    old_point = None
    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        cv2.imshow("Frame", frame) # video + circle
        # orange
        #low = np.array([0, 169, 164])
        #high = np.array([35, 255, 255])
        low = np.array([28, 80, 130])
        high = np.array([41, 255, 255])
        mask = cv2.inRange(hsv_frame, low, high)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # center
        rad = 1                                                                                                                                                                                                                                                    
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            x=int(M["m10"] / M["m00"])
            y=int(M["m01"] / M["m00"])
            if radius>10:
                passThroughAim.x = map(x, 0, 1920, -1, 1)
                passThroughAim.y = map(y, 0, 1080, -1, 1)
            center = x,y
           # print(x, "  ",y)                                                                                                                           


# if __name__ == "__main__":  # confirms that the code is under main function
#     procs = []
#     pad_proc = Process(target=pad.Initialize)  # instantiating without any argument
#     padding_proc = Process(target=padding)
#     sock_proc = Process(target = sockets)
#     video_proc = Process(target = InitializeVideo)
#     meth_proc = Process(target=meth)
#     procs.append(sock_proc)
#     procs.append(pad_proc)
#     procs.append(padding_proc)
#     procs.append(video_proc)
#     procs.append(meth_proc)
#     pad_proc.start()
#     padding_proc.start()
#     video_proc.start()
#     sock_proc.start()
#     meth_proc.start()


    # complete the processes
    # for proc in procs:
    #     proc.join()

controllerThread = threading.Thread(target = pad.Initialize)
controllerThread.start()
socketsThread = threading.Thread(target=sockets)
socketsThread.start()
paddingThread = threading.Thread(target=padding)
paddingThread.start()
methThread = threading.Thread(target=meth)
methThread.start()
aThread = threading.Thread(target=someVideo)
aThread.start()  

# stupidThread= threading.Thread(target=stupid_video)
# stupidThread.start()

# smartThread= threading.Thread(target=smart_video)
# smartThread.start()