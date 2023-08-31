import pickle
from time import sleep
from serial import Serial
import socket
import threading
import http.server
import socketserver
import threading

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/up':
            print("up")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            httphold.a  = 60
            httphold.b = 23
            httphold.c = 23
            self.wfile.write("Action triggered!".encode())
        elif self.path == '/down':
            print("down")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Action triggered!".encode())
            httphold.a  = 10
            httphold.b = 55
            httphold.c =55
            httphold.l = 1
        elif self.path == '/right':
            print("right")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Action triggered!".encode())
            httphold.a  = 30
            httphold.b = 25
            httphold.c = 50
            httphold.l = 1
        elif self.path == '/left':
            print("left")
            httphold.a  = 30
            httphold.b =50
            httphold.c = 25
            httphold.l =1
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Action triggered!".encode())
        elif self.path == '/estop':
            print("estop")
            httphold.a  = 0
            httphold.b =0
            httphold.c = 0
            httphold.l =0
            httphold.httpARM = 0
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Action triggered!".encode())
        elif self.path == '/switch':
            print("switch")
            httphold.a  = 0
            httphold.b =0
            httphold.c = 0
            httphold.l =0
            if(httphold.httpARM == 0):
                httphold.httpARM = 1
            elif(httphold.httpARM==1):
                httphold.httpARM = 2
            elif(httphold.httpARM == 2):
                httphold.httpARM = 1
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Action triggered!".encode())
        else:
            super().do_GET()


class httpControl:
    httpARM = 0 #0=estop 1=http 2=websockets
    a = 0
    b = 0
    c = 0
    l = 0

class toSend:
    HVB_ARM = 0  #przekaźnik zasilania hvb, zmiana chwilowa => start
    stop = 0        #stop ruchu silnikow chwytaka => 
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
httphold = httpControl()
old_decoded = None
xiaoID = '0'
picoID = '1'

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

def InitializeSocket(PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', PORT))
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
        print(httphold.httpARM)
        if httphold.httpARM == 1:
            serialpico.write(bytes('a'+str(httphold.a), "utf-8"))
            serialpico.write(bytes('b'+str(httphold.b), "utf-8"))
            serialpico.write(bytes('c'+str(httphold.c), "utf-8"))
            serialpico.write(bytes('w'+'4',  'utf-8'))
            if(httphold.l==1):
                serialpico.write(bytes('l', 'utf-8'))
                httphold.l = 0
        elif httphold.httpARM ==2:
            if len(datahold.data)>2:
                try:
                    decoded = pickle.loads(datahold.data)
                    serialpico.write(bytes('a' + str(decoded.USB_A), 'utf-8'))
                    serialpico.write(bytes('b' + str(decoded.USB_B), 'utf-8'))
                    serialpico.write(bytes('c' + str(decoded.USB_C), 'utf-8'))
                    if decoded.USB_L == 1 and old_decoded.USB_L == 0:
                        serialpico.write(bytes('l', 'utf-8'))
                    if decoded.USB_AK == 1 and old_decoded.USB_AK == 0:
                        serialpico.write(bytes('q', 'utf-8'))
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
                except:
                    print("err")
                    decoded = b''
        elif httphold.httpARM == 0:
            serialpico.write(bytes('a' + '0', 'utf-8'))
            serialpico.write(bytes('b' + '0', 'utf-8'))
            serialpico.write(bytes('c' + '0', 'utf-8'))
            serialpico.write(bytes('w' + '0', 'utf-8'))
            serialpico.write(bytes('s', 'utf-8'))
            serialxiao.write(bytes('h' + '0', 'utf-8'))
            serialxiao.write(bytes('l' + '0', 'utf-8'))
            serialxiao.write(bytes('x' + '0', 'utf-8'))
            serialxiao.write(bytes('t' + '0', 'utf-8'))




if __name__ == "__main__":
    acm = threading.Thread(target=InitializeACM)
    acm.start()
    port = threading.Thread(target=InitializeSocket, args=[8766])
    port.start()
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
