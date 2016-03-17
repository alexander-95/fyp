import cv2
from time import time, sleep
import numpy as np
from maths import getMetrics, getLocation, getPosition

#res = [1280, 720]
delay = 0.0
blurVal = 13
counter = 0
res = [640, 480]

capL = cv2.VideoCapture(1)
#capL.open('http://192.168.43.180:8081/video.mjpeg')
#capL.open('http://192.168.1.117:8081/video.mjpeg')
capL.set(3,res[0])
capL.set(4,res[1])

capR = cv2.VideoCapture(2)
#capR.open('http://192.168.43.231:8081/video.mjpeg')
#capR.open('http://192.168.1.116:8081/videp.mjpeg')
capR.set(3,res[0])
capR.set(4,res[1])

#kernel for image closing
kernel = np.ones((13,13),np.uint8)
#times for each photo
t = [0,0,0,0]

ret, frame1 = capL.read()
t[0] = time()
sleep(delay)
ret, frame2 = capR.read()
t[1] = time()
sleep(delay)
ret, frame3 = capL.read()
t[2] = time()
sleep(delay)
ret, frame4 = capR.read()
t[3] = time()
sleep(delay)

frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
frame1 = cv2.GaussianBlur(frame1,(blurVal,blurVal),0)
frame2 = cv2.GaussianBlur(frame2,(blurVal,blurVal),0)
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
    return centroids
l1 = findObjects(frame1)
r1 = findObjects(frame2)

while True:
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
    frame4 = cv2.cvtColor(frame4, cv2.COLOR_BGR2GRAY)
    
    frame3 = cv2.GaussianBlur(frame3,(blurVal,blurVal),0)
    frame4 = cv2.GaussianBlur(frame4,(blurVal,blurVal),0)
    
    cv2.threshold(frame3, 50, 255, cv2.THRESH_BINARY, frame3)
    cv2.threshold(frame4, 50, 255, cv2.THRESH_BINARY, frame4)
    
    frame3 = cv2.morphologyEx(frame3, cv2.MORPH_CLOSE, kernel)
    frame4 = cv2.morphologyEx(frame4, cv2.MORPH_CLOSE, kernel)

    l2 = findObjects(frame3)
    r2 = findObjects(frame4)
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_GRAY2BGR)
    frame4 = cv2.cvtColor(frame4, cv2.COLOR_GRAY2BGR)
    cv2.line(frame3, (0, res[1]/2), (res[0], res[1]/2), (0, 0, 255))
    cv2.line(frame3, (res[0]/2, 0), (res[0]/2, res[1]), (0, 0, 255))
    cv2.line(frame4, (0, res[1]/2), (res[0], res[1]/2), (0, 0, 255))
    cv2.line(frame4, (res[0]/2, 0), (res[0]/2, res[1]), (0, 0, 255))
    for centroid in l2:
        cv2.circle(frame3,centroid,5,(255,255,0),thickness=2)
    for centroid in r2:
        cv2.circle(frame4,centroid,5,(255,255,0),thickness=2)
    
    f1 = cv2.resize(frame1, (0,0), fx=0.5, fy=0.5) 
    f2 = cv2.resize(frame2, (0,0), fx=0.5, fy=0.5)
    f3 = cv2.resize(frame3, (0,0), fx=0.5, fy=0.5)
    f4 = cv2.resize(frame4, (0,0), fx=0.5, fy=0.5)

    cv2.imshow('frame1',f1)
    cv2.imshow('frame2',f2)
    cv2.imshow('frame3',f3)
    cv2.imshow('frame4',f4)
    
    if cv2.waitKey(1) & 0xFF == ord(' '):
        cv2.imwrite('frame1.png',frame1)
    if len(l1) == 1 and len(r1) == 1 and len(l2) == 1 and len(r2) == 1:
        print
        counter+=1
        print 'interval',counter
        getPosition(l1[0],l2[0],r1[0],r2[0],t,4,res,[85,0,0])

    #no more calculations past this point
    
    #break out of the loop if the c key is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
    #update the frames for the next iteration
    frame1 = frame3
    t[0] = t[2]
    l1 = l2
    frame2 = frame4
    t[1] = t[3]
    r1 = r2
    ret, frame3 = capL.read()
    t[2] = time()
    sleep(delay)
    ret, frame4 = capR.read()
    sleep(delay)
    t[3] = time()
