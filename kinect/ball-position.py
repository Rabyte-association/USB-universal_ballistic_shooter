import cv2
import imutils
import numpy as np
import random

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
overlay = np.zeros([720,1280,3], dtype=np.uint8)

old_point = None
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # orange
    #low = np.array([0, 169, 164])
    #high = np.array([35, 255, 255])
    low = np.array([15, 120, 120])
    high = np.array([35, 255, 255])
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
        try:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        except:
            center = None
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.circle(mask, center, 5, (0, 0, 255), -1)
        rad = radius


    cv2.imshow("Frame", frame) # video + circle
    #print(center)
    if center == None:
        center = old_point
    if old_point == None:
        old_point = center
    if(int(rad) > 0 and int(rad) < 50):
        overlay = cv2.line(overlay, old_point, center, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), int(2))
    combined = cv2.addWeighted(frame,1,overlay,1,1)
    if center != None:
        old_point = center
    combined = cv2.flip(combined, 1)
    cv2.imshow("Result", combined) # ball shape
    print(rad)
    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == 32:
        overlay = np.zeros([720,1280,3], dtype=np.uint8)

