#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np

cv2.namedWindow('Depth')
cv2.namedWindow('Video')
print('Press ESC in window to stop')


def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


while 1:
    depth = get_depth()
    video = get_video()
    wynik = 0.126*np.tan(depth[240][320]/2842.5+1.1863)
    index = (0,0)
    try:
        print(str(depth[240][320]) + " : " + str(wynik))
        print()
    except:
        print(None)

    minimum = 255
    for i in range(480):
        for j in range(640):
            if depth[i][j] < minimum:
                minimum = depth[i][j]
                index = (i,j)
    print(str(minimum) + " : " + str(index))
    cv2.imshow('Depth', depth)
    cv2.imshow('Video', video)
    if cv2.waitKey(10) == 27:
        break
