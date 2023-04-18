from inputs import get_gamepad
import math
import threading
from time import sleep

class Axis2:
    x = 0
    y = 0

    def __init__(self, a, b):
        self.x = a
        self.y = b


class Pad():
    MAX_TRIG_VAL =  math.pow(2, 10)
    MAX_JOY_VAL =  math.pow(2, 15)

    leftAxis = Axis2(0, 0)
    rightAxis = Axis2(0, 0)
    axisTL = 0
    axisTR = 0
    button_TL = 0
    button_TR = 0
    button_A = 0
    button_X = 0
    button_Y = 0
    button_B = 0
    buttonSelect = 0
    buttonStart = 0
    button_ThL = 0
    button_ThR = 0
    buttonSelect = 0
    buttonStart = 0
    hatAxis = Axis2(0, 0)
    hatUP = 0

    def ShowDebug(self):
        print('Pad Object: ')
        print('btnA: ' + str(self.button_A))
        print('btnB: ' + str(self.button_B))
        print('btnX: ' + str(self.button_X))
        print('btnY: ' + str(self.button_Y))
        print('btnStart: ' + str(self.buttonStart))
        print('btnSel: ' + str(self.buttonSelect))
        print('btnThL: ' + str(self.button_ThL))
        print('btnThR: ' + str(self.button_ThR))
        print('btnTL: ' + str(self.button_TL))
        print('btnTR: ' + str(self.button_TR))

        print('leftAxis: x: ' + str(self.leftAxis.x) +
              ' y: ' + str(self.leftAxis.y))
        print('rigthAxis: x: ' + str(self.rightAxis.x) +
              ' y: ' + str(self.rightAxis.y))
        print('hat: x: ' + str(self.hatAxis.x) +
              ' y: ' + str(self.hatAxis.y))
        print('triggerL: val: ' + str(self.axisTL))
        print('triggerR: val: ' + str(self.axisTR))
    
    
    def Initialize(self):
            while True:
                events = get_gamepad()
                for event in events:
                    if event.code == 'ABS_Y':
                        # normalize between -1 and 1
                        self.leftAxis.y = round(event.state / self.MAX_JOY_VAL, 3)
                    elif event.code == 'ABS_X':
                        # normalize between -1 and 1
                        self.leftAxis.x = round(event.state / self.MAX_JOY_VAL, 3)
                    elif event.code == 'ABS_RY':
                        self.rightAxis.y =round(event.state/self.MAX_JOY_VAL,3)  # normalize between -1 and 1
                    elif event.code == 'ABS_RX':
                        self.rightAxis.x = round(event.state /self.MAX_JOY_VAL,3)  # normalize between -1 and 1
                    elif event.code == 'ABS_Z':
                        self.axisTL = round(event.state /self.MAX_TRIG_VAL,3)  # normalize between 0 and 1
                    elif event.code == 'ABS_RZ':
                        self.axisTR = round(event.state / self.MAX_TRIG_VAL,3)  # normalize between 0 and 1
                    elif event.code == 'BTN_TL':
                        self.button_TL = event.state
                    elif event.code == 'BTN_TR':
                        self.button_TR = event.state
                    elif event.code == 'BTN_SOUTH':
                        self.button_A = event.state
                    elif event.code == 'BTN_NORTH':
                        self.button_X = event.state  # previously switched with X
                    elif event.code == 'BTN_WEST':
                        self.button_Y = event.state  # previously switched with Y
                    elif event.code == 'BTN_EAST':
                        self.button_B = event.state
                    elif event.code == 'BTN_THUMBL':
                        self.button_ThL = event.state
                    elif event.code == 'BTN_THUMBR':
                        self.button_ThR = event.state
                    elif event.code == 'BTN_SELECT':
                        self.buttonSelect = event.state
                    elif event.code == 'BTN_START':
                        self.buttonStart = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY1':
                       self.hatUP = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY2':
                        self.hatUP = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY3':
                        self.hatAxis.y = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY4':
                        self.hatAxis.y = event.state

