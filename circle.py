import cv2
import numpy as np
from skimage.draw import polygon, circle
from skimage.draw import polygon

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False



while rval:

    r = len(frame)
    c = len(frame[0])
    rad = min(r,c)//8
    rr, cc = circle(r//100+10+rad, c//100+10+rad, rad)

    for i in range(len(rr)):
        for j in range(3):
            frame[rr[i],cc[i],j] -= min(100,frame[rr[i],cc[i],j])    
    
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")