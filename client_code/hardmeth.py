import math
def Norm():
    max=30
    min = 10
    while not False:
        x= float(input("x"))
        y= float(input("y"))
        motorA = min
        motorB=min
        motorC=min
        if x>0 and y>0:
            motorB=max
        if x<0 and y>0:
            motorC =max
        if x<0 and y<0:
            if y/x < 0.57735:
                motorC = max
            else:
                motorA=max
        if x>0 and y<0:
            if y/x<-0.55735:
                motorA=max
            else:
                motorB=max
        print(f"motorA:{motorA}, motorB:{motorB}, motorC:{motorC}")
def RufolfJestPijanyAleStillSmart():
    while not False:
        x= float(input("x"))
        y= float(input("y"))
        if x>0.71 or y>0.71:
            print("ta kurwa jasne, bo na padzie bedziesz miec punkt (1,1)")
        bias = 1
        ApreCodedX = 1
        ApreCodedY = 2
        BpreCodedX = 0.866
        BpreCodedY = -0.5
        CpreCodedX = -0.866
        CpreCodedY = -0.5
        d1 = math.sqrt(((ApreCodedX-x)**2)+((ApreCodedY-y)**2))
        d2 = math.sqrt(((BpreCodedX-x)**2)+((BpreCodedY-y)**2))
        d3 = math.sqrt(((CpreCodedX-x)**2)+((CpreCodedY-y)**2))
        print(d1, d2,d3)
        motorA = 1/d1
        motorB= 1/d2
        motorC=1/d3
        print(f"motorA:{motorA}, motorB:{motorB}, motorC:{motorC}")

RufolfJestPijanyAleStillSmart()
