import pickle
from time import sleep
from serial import Serial
import socket
import threading

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

class DataHold:
    data = ""

datahold = DataHold()
datahold.data = ""
old_decoded = None
xiaoID = '0'
picoID = '1'

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
        if len(datahold.data)>2:
            #print(datahold.data)
            try:
                #print('pre-sraka')
                decoded = pickle.loads(datahold.data)
                #print('sraka')
                #print(decoded.USB_W)
                serialpico.write(bytes('a' + str(decoded.USB_A), 'utf-8'))
                serialpico.write(bytes('b' + str(decoded.USB_B), 'utf-8'))
                serialpico.write(bytes('c' + str(decoded.USB_C), 'utf-8'))
                if decoded.USB_L == 1 and old_decoded.USB_L == 0:
                    serialpico.write(bytes('l', 'utf-8'))
                if decoded.USB_AK == 1 and old_decoded.USB_AK == 0:
                    serialpico.write(bytes('q', 'utf-8'))
                    #print('ssas')
                if decoded.stop == 1 and old_decoded.stop == 0:
                    serialxiao.write(bytes('s', 'utf-8'))
                    serialpico.write(bytes('s', 'utf-8'))
                if decoded.USB_W == 1 and old_decoded.USB_W == 0:
                    serialpico.write(bytes('w4', 'utf-8'))
                serialxiao.write(bytes('h' + str(decoded.HVB_ARM), 'utf-8'))
                serialxiao.write(bytes('l' + str(decoded.led), 'utf-8'))
                serialxiao.write(bytes('x' + str(decoded.hvbSpeed), 'utf-8'))
                serialxiao.write(bytes('t' + str(decoded.hvbDir), 'utf-8'))
                old_decoded = decoded
               # print(decoded)
            except:
                print("err")
               # print(datahold.data)
                decoded = b''
            

if __name__ == "__main__":
    acm = threading.Thread(target=InitializeACM)
    acm.start()

    port = threading.Thread(target=InitializeSocket, args=[8765])
    port.start()