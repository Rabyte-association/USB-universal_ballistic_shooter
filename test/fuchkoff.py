import math
from time import sleep
while not False:  
        x=int(input())
        y= int(input())
        #if abs(x)>0.15 and abs(y)>0.15:
        
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
        sleep(.1)
        print(f"motorA:{motorA}, motorB:{motorB}, motorC:{motorC}")
  
