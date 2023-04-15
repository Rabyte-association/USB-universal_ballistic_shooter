import numpy as np
import cv2

iB = cv2.imread('box_back.jpg')
iA = cv2.imread('box.jpg')

imgB = np.array(iB, dtype=np.float64)
imgA = np.array(iA, dtype=np.float64)

imgA /= 255.0
imgB /= 255.0
#cv2.imshow('imgA',imgA)
#cv2.imshow('imgB',imgB)
cv2.waitKey(0)

#pre-multiplication
a_channel_A = np.ones(imgA.shape, dtype=np.float64)/2.0
a_channel_B = np.ones(imgB.shape, dtype=np.float64)/2.0

imageA = imgA*a_channel_A
imageB = imgB*a_channel_B

output = (imgA * a_channel_A) + (imgB * (1-a_channel_B))

cv2.imshow('img',output)
cv2.waitKey(0)
cv2.destroyAllWindows()
