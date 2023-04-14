import pandas as pd
import cv2

camera = cv2.VideoCapture(2)

codec = 0x47504A4D  # MJPG
camera.set(cv2.CAP_PROP_FPS, 15.0)
camera.set(cv2.CAP_PROP_FOURCC, codec)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while (1):
    retval, im = camera.read(0)
    cv2.imshow("image", im)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

camera.release()
cv2.destroyAllWindows()

