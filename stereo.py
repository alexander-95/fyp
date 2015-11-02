import numpy as np
import cv2

cap1 = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(1)


#set resolution
cap1.set(3,640)
cap1.set(4,480)

#set resolution
cap2.set(3,640)
cap2.set(4,480)

#set the brightness
cap1.set(10, 0.7)
cap2.set(10, 0.7)

#set the saturation
cap1.set(12, 0.5)
cap2.set(12, 0.5)

#set the contrast
cap1.set(11,0.5)
cap2.set(11, 0.5)

while(True):
    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()
    diff = cv2.absdiff(frame1, frame2)
    #cv2.imshow('frame1', frame1)
    #cv2.imshow('frame2', frame2)
    cv2.imshow('diff', diff)
    #if the 'c' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
cap.release()
cv2.destroyAllWindows()
