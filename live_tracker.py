import cv2
from time import time, sleep
import numpy as np
from maths import getMetrics, getLocation

capL = cv2.VideoCapture(1)
capR = cv2.VideoCapture(2)

#kernel for gaussian blur
kernel = np.ones((5,5),np.uint8)
#times for each photo
t = [0,0,0,0]

ret, frame1 = capL.read()
t[0] = time()
ret, frame2 = capR.read()
t[1] = time()
ret, frame3 = capL.read()
t[2] = time()
ret, frame4 = capR.read()
t[3] = time()

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
    if len(centroids)>1:
        centroids.pop()
    cv2.line(frame, (0, 240), (640, 240), (0, 0, 255))
    cv2.line(frame, (320, 0), (320, 480), (0, 0, 255))
    for c in centroids:
        cv2.circle(frame,c,5,(255,0,0))
    return centroids

l1 = findObjects(frame1)
r1 = findObjects(frame2)

while True:
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
    frame4 = cv2.cvtColor(frame4, cv2.COLOR_BGR2GRAY)
    
    frame3 = cv2.GaussianBlur(frame3,(5,5),0)
    frame4 = cv2.GaussianBlur(frame4,(5,5),0)
    
    cv2.threshold(frame3, 40, 255, cv2.THRESH_BINARY, frame3)
    cv2.threshold(frame4, 40, 255, cv2.THRESH_BINARY, frame4)
    
    l2 = findObjects(frame3)
    r2 = findObjects(frame4)
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_GRAY2BGR)
    frame4 = cv2.cvtColor(frame4, cv2.COLOR_GRAY2BGR)
    cv2.line(frame3, (0, 240), (640, 240), (0, 0, 255))
    cv2.line(frame3, (320, 0), (320, 480), (0, 0, 255))
    cv2.line(frame4, (0, 240), (640, 240), (0, 0, 255))
    cv2.line(frame4, (320, 0), (320, 480), (0, 0, 255))

    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    cv2.imshow('frame3',frame3)
    cv2.imshow('frame4',frame4)
    
    if len(l1) == 1 and len(r1) == 1:
        #obj = getLocation(l1[0],r1[0],4,80)
        #print 'object =',obj
        obj = getMetrics(l1[0],r1[0],l2[0],r2[0],t,4,80)
        print 'object =',obj
    

    #no more calculations past this point

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
    frame1 = frame3
    t[0] = t[2]
    l1 = l2
    frame2 = frame4
    t[1] = t[3]
    r1 = r2
    ret, frame3 = capL.read()
    t[2] = time()
    ret, frame4 = capR.read()
    t[3] = time()
