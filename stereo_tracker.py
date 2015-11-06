import cv2
from time import time

capL = cv2.VideoCapture(2)
capR = cv2.VideoCapture(1)

while True:
    retL, frameL = capL.read()
    retR, frameR = capR.read()
    
    frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
    
    frameL = cv2.GaussianBlur(frameL,(5,5),0)
    frameR = cv2.GaussianBlur(frameR,(5,5),0)

    cv2.threshold(frameL, 60, 255, cv2.THRESH_BINARY, frameL)
    cv2.threshold(frameR, 60, 255, cv2.THRESH_BINARY, frameR)

    contoursL, hierarchyL = cv2.findContours(frameL.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    momentsL = [cv2.moments(cnt) for cnt in contoursL]
    centroidsL = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in momentsL if m['m00']!=0]
    for c in centroidsL:
        cv2.circle(frameL,c,5,(255,0,0))

    contoursR, hierarchyR = cv2.findContours(frameR.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    momentsR = [cv2.moments(cnt) for cnt in contoursR]
    centroidsR = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in momentsR if m['m00']!=0]
    for c in centroidsR:
        cv2.circle(frameR,c,5,(255,0,0))
    
    cv2.imshow('Left', frameL)
    cv2.imshow('Right', frameR)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite(str(time())+'L.png', frameL)
        cv2.imwrite(str(time())+'R.png', frameR)
        break
print 'Left',centroidsL
print 'Right',centroidsR
capL.release()
capR.release()
cv2.destroyAllWindows()
