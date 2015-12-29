import cv2
from time import time, sleep
import numpy as np

capL = cv2.VideoCapture(0)
capR = cv2.VideoCapture(1)

#kernel for gaussian blur
kernel = np.ones((5,5),np.uint8)

ret, frame1 = capL.read()
ret, frame2 = capR.read()
ret, frame3 = capL.read()
ret, frame4 = capR.read()

frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
frame1 = cv2.GaussianBlur(frame1,(5,5),0)
frame2 = cv2.GaussianBlur(frame2,(5,5),0)
cv2.threshold(frame1, 40, 255, cv2.THRESH_BINARY, frame1)
cv2.threshold(frame2, 40, 255, cv2.THRESH_BINARY, frame2)

def findObjects(frame):
    contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    moments = [cv2.moments(cnt) for cnt in contours]
    centroids = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in moments if m['m00']!=0]
    centroids.pop()
    for c in centroids:
        cv2.circle(frame,c,5,(255,0,0))

findObjects(frame1)
findObjects(frame2)

while True:
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
    frame4 = cv2.cvtColor(frame4, cv2.COLOR_BGR2GRAY)
    
    frame3 = cv2.GaussianBlur(frame3,(5,5),0)
    frame4 = cv2.GaussianBlur(frame4,(5,5),0)
    
    cv2.threshold(frame3, 40, 255, cv2.THRESH_BINARY, frame3)
    cv2.threshold(frame4, 40, 255, cv2.THRESH_BINARY, frame4)
    
    findObjects(frame3)
    findObjects(frame4)

    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    cv2.imshow('frame3',frame3)
    cv2.imshow('frame4',frame4)
    

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
    frame1 = frame3
    frame2 = frame4
    ret, frame3 = capL.read()
    ret, frame4 = capR.read()
