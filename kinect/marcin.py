import cv2
import freenect
import imutils
import frame_convert2
import numpy as np

#cap = cv2.VideoCapture(0)

cv2.namedWindow('Depth')
#cv2.namedWindow('Video')

def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])

def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

while True:

    frame = get_video()
    canvas = cv2.rectangle(frame.astype(np.int32), (0, 0), (2, 2), (0, 0, 0))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # orange

    depth = get_depth()
    wynik = 0.126*np.tan(depth[240][320]/2842.5+1.1863)
    index = (0,0)
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
        global br
        br = int(radius)
        M = cv2.moments(c)
        try:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        except:
            center = None
        if radius > 5:
            cv2.circle(canvas, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(canvas, center, 5, (0, 0, 255), -1)
            cv2.circle(mask, center, 5, (0, 0, 255), -1)
    try:
        print(str(depth[240][320]) + " : " + str(wynik))
        print()
    except:
        print(None)
    delx= 480/br
    deltax = int(delx)
    dely= 640/br
    deltay= int(dely)
    local_minimum = 255
    minimum = local_minimum
    for i in range(deltax):
        for j in range(deltay):
            if depth[br*i][br*j] < local_minimum:
                local_minimum = depth[i][j]
                lminx = i - br
                lminy = j - br
    for m in range(lminx, lminx+ br):
                for n in range(lminy, lminy+ br):
                     if depth[m][n] < minimum:
                          minimum = depth[m][n]
                          index = (m,n)
    print(str(minimum) + " : " + str(index))
    
    canvas = canvas.astype(np.uint8)
    
    cv2.imshow('Depth', depth)
    cv2.imshow("Frame", canvas) # video + circle
    print(center)
    key = cv2.waitKey(1)
    if key == 27:
        break