import cv2
from time import time
from time import sleep
from maths import getLocation
import numpy as np

#setup webcams
capL = cv2.VideoCapture(1)
capR = cv2.VideoCapture(2)

kernel = np.ones((5,5),np.uint8)

while True:
    #read the current frames
    retL, frameL = capL.read()
    retR, frameR = capR.read()

    #convert image to grayscale
    frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

    #smooth the image by blurring
    frameL = cv2.GaussianBlur(frameL,(5,5),0)
    frameR = cv2.GaussianBlur(frameR,(5,5),0)
    
    #threshold image
    cv2.threshold(frameL, 40, 255, cv2.THRESH_BINARY, frameL)
    cv2.threshold(frameR, 40, 255, cv2.THRESH_BINARY, frameR)
    
    frameL = cv2.morphologyEx(frameL, cv2.MORPH_CLOSE, kernel)
    frameR = cv2.morphologyEx(frameR, cv2.MORPH_CLOSE, kernel)

    #find the center of objects
    contoursL, hierarchyL = cv2.findContours(frameL.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    momentsL = [cv2.moments(cnt) for cnt in contoursL]
    centroidsL = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in momentsL if m['m00']!=0]
    if len(centroidsL)>1:
        centroidsL.pop()
    for c in centroidsL:
        cv2.circle(frameL,c,5,(255,0,0))

    contoursR, hierarchyR = cv2.findContours(frameR.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    momentsR = [cv2.moments(cnt) for cnt in contoursR]
    centroidsR = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in momentsR if m['m00']!=0]
    if len(centroidsR)>1:
        centroidsR.pop()
    for c in centroidsR:
        cv2.circle(frameR,c,5,(255,0,0))
    #print 'Left',centroidsL,'\tRight',centroidsR
    
    #get the location if an object is found
    if(len(centroidsL)==1) and (len(centroidsR)==1):
        print centroidsL[0]
        print centroidsR[0]
        print 'Location:',getLocation(centroidsL[0], centroidsR[0], 4, 80)

    #project crosshairs onto image
    frameL = cv2.cvtColor(frameL, cv2.COLOR_GRAY2BGR)
    cv2.line(frameL, (0, 240), (640, 240), (0, 0, 255))
    cv2.line(frameL, (320, 0), (320, 480), (0, 0, 255))
    
    frameR = cv2.cvtColor(frameR, cv2.COLOR_GRAY2BGR)
    cv2.line(frameR, (0, 240), (640, 240), (0, 0, 255))
    cv2.line(frameR, (320, 0), (320, 480), (0, 0, 255))
    
    cv2.imshow('Left', frameL)
    cv2.imshow('Right', frameR)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        #cv2.imwrite(str(time())+'L.png', frameL)
        #cv2.imwrite(str(time())+'R.png', frameR)
        break
print 'Left',centroidsL
print 'Right',centroidsR
capL.release()
capR.release()
cv2.destroyAllWindows()
