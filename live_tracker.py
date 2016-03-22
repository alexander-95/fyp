import cv2
from time import time, sleep
import numpy as np
from maths import getMetrics, getLocation, getPosition

#initialised variables
res = [1280, 720]
delay = 0.0
blurVal = 13
threshVal = 50
counter = 0
crosshairs_enabled = True
centroids_enabled = True
kernel = np.ones((13, 13),np.uint8)#used for image closing
t = [0, 0, 0, 0]# list of timestamps
frame = [0, 0, 0, 0]#list of images
preview = [0, 0, 0, 0]#list of preview frames
c1 = [659, 366]
c2 = [633, 332]

#set up first camera
capL = cv2.VideoCapture(2)
capL.set(3, res[0])
capL.set(4, res[1])

#set up second camera
capR = cv2.VideoCapture(1)
capR.set(3, res[0])
capR.set(4, res[1])

#take the first 4 images
for i in xrange(4):
    if i&2:#second 2 images
        ret, frame[i] = capR.read()
    else:#first 2 images
        ret, frame[i] = capL.read()
    ret, frame[i] = capL.read()
    t[i] = time()
    sleep(delay)

#find objects in an image using thresholding/blob detection
def findObjects(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (blurVal,blurVal), 0)
    cv2.threshold(frame, threshVal, 255, cv2.THRESH_BINARY, frame)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    moments = [cv2.moments(cnt) for cnt in contours]
    centroids = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in moments if m['m00']!=0]
    if len(centroids) > 0:
        centroids.pop()
    return centroids

l1 = findObjects(frame[0])
r1 = findObjects(frame[2])

while True:
    l2 = findObjects(frame[1])
    r2 = findObjects(frame[3])

    if crosshairs_enabled:#draw crosshairs
        cv2.line(frame[1], (0, c1[1]), (res[0], c1[1]), (0, 0, 255))
        cv2.line(frame[1], (c1[0], 0), (c1[0], res[1]), (0, 0, 255))
        cv2.line(frame[3], (0, c2[1]), (res[0], c2[1]), (0, 0, 255))
        cv2.line(frame[3], (c2[0], 0), (c2[0], res[1]), (0, 0, 255))

    if centroids_enabled:#highlight centroids
        for centroid in l2:
            cv2.circle(frame[1], centroid, 5, (255, 255, 0),thickness = 2)
        for centroid in r2:
            cv2.circle(frame[3], centroid, 5, (255, 255, 0),thickness = 2)

    for i in xrange(4):#generate scaled down preview images
        preview[i] = (cv2.resize(frame[i], (0,0), fx=0.5, fy=0.5))
        cv2.imshow('frame'+str(i), preview[i])

    if cv2.waitKey(1) & 0xFF == ord(' '):#save images
        for i in xrange(4):
            cv2.imwrite('frame'+str(i)+'.png', frame[i])
        print l1, l2, r1, r2, t

    #make calculations if only one object is found in the scene
    if len(l1) == 1 and len(r1) == 1 and len(l2) == 1 and len(r2) == 1:
        print
        counter+=1
        print 'interval',counter
        getPosition(l1[0], l2[0], r1[0], r2[0], t, 4, res, [105, 0, 0])

    #break out of the loop if the c key is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
    
    #update the frames for the next iteration
    frame[0] = frame[1]
    t[0] = t[1]
    l1 = l2
    frame[2] = frame[3]
    t[2] = t[3]
    r1 = r2
    ret, frame[1] = capL.read()
    t[1] = time()
    sleep(delay)
    ret, frame[3] = capR.read()
    sleep(delay)
    t[3] = time()

capL.release()
capR.release()
cv2.destroyAllWindows()
