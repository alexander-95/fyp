import cv2
from time import sleep
cap = cv2.VideoCapture(0)

while(True):
    ret, before = cap.read()
    #before = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    cv2.imshow('before',before)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

while(True):
    ret, after = cap.read()
    #after = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(before, after)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY, diff)
    cv2.imshow('diff', diff)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
