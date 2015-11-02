import cv2

capL = cv2.VideoCapture(1)
capR = cv2.VideoCapture(0)

while True:
    retL, frameL = capL.read()
    retR, frameR = capR.read()
    
    frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
    
    frameL = cv2.GaussianBlur(frameL,(5,5),0)

    cv2.threshold(frameL, 60, 255, cv2.THRESH_BINARY, frameL)
    cv2.threshold(frameR, 60, 255, cv2.THRESH_BINARY, frameR)

    contours, hierarchy = cv2.findContours(frameL.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    moments = [cv2.moments(cnt) for cnt in contours]
    
    centroids = [(int (round(m['m10']/m['m00'])), int(round(m['m01']/m['m00']))) for m in moments if m['m00']!=0]

    for c in centroids:
        cv2.circle(frameL,c,5,(255,0,0))

    cv2.imshow('Left', frameL)
    cv2.imshow('Right', frameR)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
capL.release()
capR.release()
cv2.destroyAllWindows()
