import cv2
import imutils
import numpy as np
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # orange
    low = np.array([15, 120, 120])
    high = np.array([35, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # center
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


    cv2.imshow("Frame", frame) # video + circle
    print(center)
    cv2.imshow("Result", mask) # ball shape
    key = cv2.waitKey(1)
    if key == 27:
        break