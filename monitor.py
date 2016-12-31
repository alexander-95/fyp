import cv2
import numpy as np
from datetime import datetime

def findObjects(frame):
    contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_LIST,
                                           cv2.CHAIN_APPROX_NONE)
    moments = [cv2.moments(cnt) for cnt in contours]
    centroids = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00'])))
                 for m in moments if m['m00']!=0]
    if len(centroids) > 0:
        centroids.pop()
    return centroids

cap = cv2.VideoCapture()
cap.open('http://192.168.0.4:8080/video?.avi')
resolution = (int(cap.get(3)), int(cap.get(4)))
cap.set(5,10)
counter = 0
limit = 100
blur = 3

fourcc = cv2.cv.CV_FOURCC(*'XVID')
filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.avi'
video = cv2.VideoWriter(filename, fourcc, 10.0, resolution)

ret, frame1 = cap.read()
while True:
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame1, frame2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    if blur:
        diff = cv2.GaussianBlur(diff,(blur, blur),0)
    cv2.threshold(diff, 25,255, cv2.THRESH_BINARY, diff)
    centroids = findObjects(diff)

    diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
    for c in centroids:
        cv2.circle(diff,c,5,(255,255,0),2)
    #cv2.imshow('diff', diff)
    #cv2.imshow('frame', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        quit()
    if len(centroids) > 0:
        print 'recording: counter =', counter
        video.write(frame1)
        counter = 0
    elif counter < limit:
        print 'recording: counter =', counter
        video.write(frame1)
        counter+=1
    elif counter == limit:
        print 'starting new video file'
        filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.avi'
        video.release()
        video = cv2.VideoWriter(filename, fourcc, 10.0, resolution)
        counter+=1
    frame1 = frame2
cap.release()
video.release()
cv2.destroyAllWindows()
