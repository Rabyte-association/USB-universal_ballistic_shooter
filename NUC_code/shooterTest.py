import serial
print("Skrypt testowania projektu USB \nWszystkie wartości podawane są w stopniach prędkości")
acmId = input("jaki ACM?")
pico = serial.Serial(port= f'/dev/ACM{acmId}', baudrate=115200,timeout=None)

tmp=''
resolution = int(input("resolution"))
minSpeed = int(input("min speed:"))
maxSpeed = int(input("max speed:"))

def write(data):
    #pico.write(data)
    print(data)
if(input("manual starting speed?")):
    deg0=int(input("Motor 0:"))
    deg1=int(input("Motor 1:"))
    deg2=int(input("Motor 2:"))
else:
    deg0=10
    deg1=10
    deg2=10

while (tmp!='q'):
    tmp = input()
    if tmp == 's':
        write('s')
    elif tmp == 'l':
        write('l')
    elif tmp == 'w':
        write('w4')
    elif tmp == 'm':
        print("now in manual mode")
        while(tmp!='e'):
            tmp=input()
            write(tmp)
        print("out of manuel mode")
    elif tmp=='a':
        print("automatic mode")
            while tmp != 'q':
            
                if tmp == 's':
                    write('s')
                for a in range(minSpeed, maxSpeed, resolution):
                    for b in range(minSpeed, maxSpeed, resolution):
                        for c in range(minSpeed, maxSpeed, resolution):
                            
        

