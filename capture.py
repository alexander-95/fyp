import cv2
from time import time
cap = cv2.VideoCapture(1)

#set a new resolution
cap.set(3,640)
cap.set(4,480)

#reduce the color saturation
cap.set(12,0.5)

#change the brightness
cap.set(10,0.5)

#bump up the contrast
cap.set(11,0.5)

while(True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY, frame)
    cv2.imshow('frame', frame)
    
    #if the 'c' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite('height.png', frame)
        print "photo taken at",time()
        break

cap.release()
cv2.destroyAllWindows()
