import cv2
from time import time, sleep
import numpy as np
from maths import getMetrics, getLocation, getPosition

#res = [1280,960]
res = [640, 480]
kernel = np.ones((5,5),np.uint8)

capL = cv2.VideoCapture(0)
#capL.open('http://192.168.43.180:8081/video.mjpeg')
#capL.open('http://192.168.1.117:8081/video.mjpeg')
capL.set(3,res[0])
capL.set(4,res[1])

capR = cv2.VideoCapture(2)
#capR.open('http://192.168.43.231:8081/video.mjpeg')
#capR.open('http://192.168.1.116:8081/videp.mjpeg')
capR.set(3,res[0])
capR.set(4,res[1])

#kernel for gaussian blur
kernel = np.ones((5,5),np.uint8)
#times for each photo
t = [0,0,0,0]

ret, frame1 = capL.read()
t[0] = time()
sleep(0.1)
ret, frame2 = capR.read()
t[1] = time()
sleep(0.1)
ret, frame3 = capL.read()
t[2] = time()
sleep(0.1)
ret, frame4 = capR.read()
t[3] = time()
sleep(0.1)

frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
frame1 = cv2.GaussianBlur(frame1,(9,9),0)
frame2 = cv2.GaussianBlur(frame2,(9,9),0)
cv2.threshold(frame1, 30, 255, cv2.THRESH_BINARY, frame1)
cv2.threshold(frame2, 30, 255, cv2.THRESH_BINARY, frame2)
frame1 = cv2.morphologyEx(frame1, cv2.MORPH_CLOSE, kernel)
frame2 = cv2.morphologyEx(frame2, cv2.MORPH_CLOSE, kernel)

def findObjects(frame):
    contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    moments = [cv2.moments(cnt) for cnt in contours]
    centroids = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in moments if m['m00']!=0]
    if len(centroids)>0:
        centroids.pop()
    #cv2.line(frame, (0, res[1]/2), (res[0], res[1]/2), (0, 0, 255))
    #cv2.line(frame, (res[0]/2, 0), (res[0]/2, res[1]), (0, 0, 255))
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
    
    cv2.threshold(frame3, 30, 255, cv2.THRESH_BINARY, frame3)
    cv2.threshold(frame4, 30, 255, cv2.THRESH_BINARY, frame4)
    
    l2 = findObjects(frame3)
    r2 = findObjects(frame4)
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_GRAY2BGR)
    frame4 = cv2.cvtColor(frame4, cv2.COLOR_GRAY2BGR)
    cv2.line(frame3, (0, res[1]/2), (res[0], res[1]/2), (0, 0, 255))
    cv2.line(frame3, (res[0]/2, 0), (res[0]/2, res[1]), (0, 0, 255))
    cv2.line(frame4, (0, res[1]/2), (res[0], res[1]/2), (0, 0, 255))
    cv2.line(frame4, (res[0]/2, 0), (res[0]/2, res[1]), (0, 0, 255))

    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    cv2.imshow('frame3',frame3)
    cv2.imshow('frame4',frame4)
    #print len(l1), len(r1)
    if len(l1) == 1 and len(r1) == 1 and len(l2) == 1 and len(r2) == 1:
        #obj = getLocation(l1[0],r1[0],4,80)
        #print 'object =',obj
        #obj = getMetrics(l1[0],r1[0],l2[0],r2[0],t,4,80)
        #print 'object =',obj
        getPosition(l1[0],l2[0],r1[0],r2[0],4,[640,480],[80,0,0])

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
    sleep(0.1)
    ret, frame4 = capR.read()
    t[3] = time()
    sleep(0.1)
